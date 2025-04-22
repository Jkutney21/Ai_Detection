import mss

try:
    with mss.mss() as sct:
        sct.shot(output="screenshot.png")
        print("Screenshot saved successfully!")
except Exception as e:
    print(f"Error with mss: {e}")