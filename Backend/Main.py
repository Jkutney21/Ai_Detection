import subprocess
import sys
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_cors import CORS
from collections import deque
import psutil
import signal
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

TEXT_FOLDER = './text'

def ensure_files_exist():
    """Ensure that logs.txt, query.txt, google.txt, gpt.txt, and text.txt exist in the 'text' folder"""
    
    # Ensure that the 'text' folder exists
    os.makedirs(TEXT_FOLDER, exist_ok=True)
    
    # List of the file names
    files = ['logs.txt', 'query.txt', 'google.txt', 'gpt.txt', 'text.txt']
    
    # Create files if they don't exist
    for file in files:
        file_path = os.path.join(TEXT_FOLDER, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass  # Create the file if it doesn't exist
    
    # Now let's add content to 'text.txt' if it doesn't already have content
    text_file_path = os.path.join(TEXT_FOLDER, 'text.txt')
    if os.path.exists(text_file_path) and os.stat(text_file_path).st_size == 0:
        with open(text_file_path, 'w') as text_file:
            text_file.write("This is the initial content in the text file.\n")  # Add initial content




app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Flag to track the screen capture state
capture = False
screen_record_process = None
def kill_process_tree(pid):
    """Kill a process and all its child processes"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass
    except Exception as e:
        print(f"Error killing process tree: {e}")


screenSize = {"top": 150, "left": 250, "width": 1500, "height": 400}

@app.route('/capture', methods=['GET', 'POST'])
def start_capture():
    global capture, screen_record_process, screenSize  # Ensure global scope

    if request.method == 'GET':
        return jsonify({"status": str(capture).lower()})

    elif request.method == 'POST':
        try:
            if not capture:
                # Start capture
                capture = True
                
                # Prepare the command to run the ScreenRecord.py script
                command = [sys.executable, './ScreenRecord.py']

                
                # If screenSize is set, append bounding box values
                if screenSize:
                    # Ensure the bounding box is in the correct format (key=value)
                    command.extend([
                        f"top={screenSize['top']}", f"left={screenSize['left']}",
                        f"width={screenSize['width']}", f"height={screenSize['height']}"
                    ])

                # Start the subprocess
                screen_record_process = subprocess.Popen(
                    command,
                    start_new_session=True  # Important for process group killing
                )

                return jsonify({
                    "status": "true",
                    "message": "Capture started",
                    "bounding_box": screenSize
                })
            else:
                # Stop capture
                capture = False
                if screen_record_process:
                    # Kill the entire process tree
                    kill_process_tree(screen_record_process.pid)

                    # Double-check termination
                    try:
                        screen_record_process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        os.kill(screen_record_process.pid, signal.SIGKILL)

                    screen_record_process = None
                return jsonify({"status": "false", "message": "Capture stopped"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "Unsupported HTTP method"}), 405



@app.route('/Logs', methods=['GET'])
def get_logs():
    try:
        # Define how many lines you want to fetch
        num_lines = 10  # Change this number to however many lines you need

        # Read the last `num_lines` from the log file
        with open('./text/logs.txt', 'r') as log_file:
            # Use deque to get the last `num_lines` lines
            logs = deque(log_file, maxlen=num_lines)

        # Convert the deque object into a list of strings (logs)
        logs = ''.join(logs)

        return jsonify({"status": "Success", "logs": logs})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})
    
@app.route('/google', methods=['GET',"POST"])
def get_google():
    try:
        # Define how many lines you want to fetch
        num_lines = 1  # Change this number to however many lines you need

        # Read the last `num_lines` from the log file
        with open('./text/google.txt', 'r') as log_file:
            # Use deque to get the last `num_lines` lines
            logs = deque(log_file, maxlen=num_lines)

        # Convert the deque object into a list of strings (logs)
        logs = ''.join(logs)

        return jsonify({"status": "Success", "google": logs})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})
    


screenSize = None

@app.route('/size', methods=["POST"])
def change_post():
    
    global screenSize, screen_record_process  # Ensure these are accessible inside the function

    try:
        # Extract bounding box parameters from the request
        data = request.json
        
        if "capture" in data and data["capture"]:  # If 'capture' is True
            bounding_box = {
                "top": data.get("top"),
                "left": data.get("left"),
                "width": data.get("width"),
                "height": data.get("height")
            }

            # Ensure all values exist
            if None in bounding_box.values():
                return jsonify({"status": "Error", "message": "Missing bounding box parameters"}), 400

            # Kill the existing screen recording process if running
            if screen_record_process:
                kill_process_tree(screen_record_process.pid)
                try:
                    screen_record_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.kill(screen_record_process.pid, signal.SIGKILL)  # Force kill if needed
                screen_record_process = None  # Reset process variable

            # Start a new subprocess with the bounding box values
            screen_record_process = subprocess.Popen(
                ["python3", "ScreenRecord.py",
                 str(bounding_box["top"]), str(bounding_box["left"]),
                 str(bounding_box["width"]), str(bounding_box["height"])],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            return jsonify({"status": "Success", "bounding_box": bounding_box})

        else:
            # If "capture" is false or not set, just store screenSize
            screenSize = data
            return jsonify({"status": "Success", "screenSize": screenSize})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500


def main():
    try:
        ensure_files_exist()
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(jsonify({"status": "Error", "message": str(e)}))
    

if __name__ == '__main__':
    main()

