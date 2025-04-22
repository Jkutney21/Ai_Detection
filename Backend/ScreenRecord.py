import os
import cv2
import spacy
import mss
import numpy as np
import pytesseract
import asyncio
import base64
import time
import sys
import psutil
from pytesseract import Output
import websockets
from websockets.exceptions import ConnectionClosed


# Global bounding_box (can be modified by user input)
bounding_box = None
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jkutn\AppData\Local\Tesseract-OCR\tesseract.exe'

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Control variables
processing_lock = asyncio.Lock()
last_process_time = 0
DEBOUNCE_SECONDS = 3
CAPTURE_INTERVAL = 0.1


def preprocess_image_function(img):
    """Improve OCR accuracy with image processing"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def is_question_sentence(sent):
    """Determine if a spaCy sentence is likely a question.
       Checks if the sentence ends with '?' or starts with an interrogative word.
    """
    interrogatives = {"what", "when", "where", "who", "whom", "whose", "why", "how"}
    text = sent.text.strip()
    if text.endswith("?"):
        return True
    # Check if the first token is an interrogative word (ignoring punctuation)
    first_token = next((token for token in sent if not token.is_punct), None)
    if first_token and first_token.text.lower() in interrogatives:
        return True
    return False

def is_option_sentence(sent):
    """Determine if a sentence looks like an answer option.
       Checks if the sentence starts with a letter (A-D) optionally followed by punctuation.
    """
    # Remove leading punctuation tokens and check first word
    tokens = [token for token in sent if not token.is_punct]
    if tokens and tokens[0].text in ["A", "B", "C", "D"]:
        return True
    return False

def parse_qa_nlp(doc):
    """Parse the OCR'd text (already processed by spaCy) to extract QA pairs.
       Group sentences identified as questions with their following option sentences.
    """
    qa_pairs = []
    current_q = None
    current_options = []

    for sent in doc.sents:
        if is_question_sentence(sent):
            if current_q is not None:
                qa_pairs.append((current_q, current_options))
            current_q = sent.text.strip()
            current_options = []
        elif is_option_sentence(sent):
            current_options.append(sent.text.strip())
    if current_q is not None:
        qa_pairs.append((current_q, current_options))
    return qa_pairs

async def screen_capture(websocket):
    global last_process_time
    print("WebSocket connection established")
    
    # Ensure the directory exists
    os.makedirs('./text', exist_ok=True)
    
    try:
        # Initialize mss with error handling
        try:
            sct = mss.mss()  # Initialize screen capture once
        except Exception as e:
            print(f"Error initializing mss: {e}")
            return  # Exit if screen capture fails
        
        while True:
            try:
                async with processing_lock:
                    # Screen capture and processing
                    sct_img = sct.grab(bounding_box)
                    img = np.array(sct_img)
                    processed_img = preprocess_image_function(img)
                    
                    # OCR processing
                    data = pytesseract.image_to_data(
                        processed_img, 
                        output_type=Output.DICT,
                        config='--psm 11'
                    )
                    
                    # Text reconstruction from OCR output
                    text_lines = []
                    prev_top = None
                    for i in range(len(data['text'])):
                        # Check OCR confidence level
                        if int(data['conf'][i]) > 60:
                            line = data['text'][i]
                            top = data['top'][i]
                            if prev_top is not None and (top - prev_top) > 20:
                                text_lines.append("\n")
                            text_lines.append(line + " ")
                            prev_top = top
                    full_text = "".join(text_lines).strip()
                    
                    # Process text using spaCy NLP
                    doc = nlp(full_text)

                    # Debounce check
                    if (time.time() - last_process_time) < DEBOUNCE_SECONDS:
                        await asyncio.sleep(CAPTURE_INTERVAL)
                        continue

                    # Process QA pairs using NLP-based parsing
                    qa_pairs = parse_qa_nlp(doc)
                    
                    with open('./text/logs.txt', 'a') as log_file, \
                            open('./text/queries.txt', 'a') as query_file:
                        
                        log_file.write(f"\n{full_text}\n---\n")
                        
                        for question, options in qa_pairs:
                            # Example handling for True/False questions (if needed)
                            if question.strip().lower() in {"true", "false"}:
                                query_file.write(f"True/False: {question}\n")
                                await trigger_google_search(question, query_file)
                                last_process_time = time.time()
                                continue
                            
                            if question and options:
                                query_entry = f"Question: {question}\nOptions:\n"
                                query_entry += "\n".join([f"  {opt}" for opt in options])
                                query_file.write(f"{query_entry}\n")
                                await trigger_google_search(question, query_file)
                                for opt in options:
                                    await trigger_google_search(f"{question} {opt}", query_file)

                    last_process_time = time.time()

                    # Send frame with connection check
                    try:
                        _, buffer = cv2.imencode('.png', img)
                        await websocket.send(base64.b64encode(buffer).decode('utf-8'))
                    except ConnectionClosed:
                        print("Client disconnected during send")
                        break

                    await asyncio.sleep(CAPTURE_INTERVAL)

            except ConnectionClosed:
                print("Client disconnected gracefully")
                break
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        await asyncio.sleep(1)


async def trigger_google_search(query, log_file):
    """Helper function to handle Google searches"""
    sanitized_query = query.replace('\n', ' ').strip()  # Remove line breaks and extra spaces
    print(f"Searching for: {sanitized_query}")
    try:
        # Execute the Google search using subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable, './google.py', sanitized_query.lower(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the process to finish and capture the output and error (if any)
        stdout, stderr = await process.communicate()

        # Log the results or error to the log file
        if process.returncode == 0:
            log_file.write(f"Results for '{sanitized_query}':\n{stdout.decode()}\n")
        else:
            log_file.write(f"Error for '{sanitized_query}': {stderr.decode()}\n")

    except Exception as e:
        # Log the error message if subprocess creation or communication fails
        print(f"Search error: {e}")
        log_file.write(f"Search error for '{sanitized_query}': {str(e)}\n")


def kill_process_on_port(port):
    """Kill process running on specified port"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Get the network connections using the new net_connections() method
                connections = proc.net_connections(kind='inet')
                for conn in connections:
                    if conn.laddr.port == port:
                        print(f"Killing process {proc.pid} ({proc.name()})")
                        try:
                            # Try graceful termination first
                            proc.terminate()
                            proc.wait(timeout=3)  # Wait for process to terminate
                        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                            # If process doesn't terminate, force kill
                            try:
                                proc.kill()
                            except psutil.NoSuchProcess:
                                pass  # Process already terminated
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error killing processes: {str(e)}")

def parse_arguments():
    """Parse command-line arguments passed in sys.argv"""
    arguments = {}
    try:
        for arg in sys.argv[1:]:
            # Expect arguments in the format 'key=value'
            key, value = arg.split('=')
            arguments[key] = int(value)  # Convert values to integers
    except ValueError:
        print("Error: Invalid argument format. Expected 'key=value' with an integer value.")
        sys.exit(1)  # Exit the program if the arguments are malformed
    return arguments

async def main():
    port = 5001
    kill_process_on_port(port)  # Kill any process using the specified port
    
    try:
        print("Starting WebSocket server on port", port)  # Debug message
        async with websockets.serve(screen_capture, "localhost", port):
            await asyncio.Future()  # Run forever
    except Exception as e:
        print(f"Error starting WebSocket server: {e}")  # Debugging error message


if __name__ == '__main__':
    
    try:
        if len(sys.argv) > 1:
            # Parse arguments if provided
            arguments = parse_arguments()

            # Print out the parsed arguments for debugging
            print(f"Parsed arguments: {arguments}")
    
            # Use the parsed arguments (height, left, top, width) for further logic
            height = arguments.get("height", 400)  # Default to 400 if not found
            left = arguments.get("left", 250)      # Default to 250 if not found
            top = arguments.get("top", 150)        # Default to 150 if not found
            width = arguments.get("width", 1500)   # Default to 1500 if not found

            # Now assign to bounding_box
            
            bounding_box = {
                "top": top,
                "left": left,
                "width": width,
                "height": height
            }
            print(f"Bounding Box: {bounding_box}")

        else:
            # Default bounding box values if no command-line arguments are provided
            
            bounding_box = {"top": 150, "left": 250, "width": 1500, "height": 400}
            print(f"Default Bounding Box: {bounding_box}")

        asyncio.run(main())
    except Exception as e:
        print(f"Unexpected Error: {e}")