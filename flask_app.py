import os

import cv2
import google.generativeai as genai
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1000)
cap.set(4, 720)

# Initialize Hand Detector
detector = HandDetector(
    staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5
)

previous_pos = None
canvas = None
ai_response_text = "Waiting for gesture..."


def get_hand_gesture(img):
    """Detect hand gestures and return fingers status."""
    hands, img = detector.findHands(img, draw=True, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    return None, None


def draw_picture(info, previous_pos, canvas):
    """Draw on canvas using index finger."""
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:  # Drawing mode
        current_pos = lmList[8][0:2]
        if previous_pos is None:
            previous_pos = current_pos
        else:
            cv2.line(canvas, tuple(current_pos), tuple(previous_pos), (255, 0, 255), 9)
    elif fingers == [1, 1, 1, 1, 1]:  # Clear canvas
        canvas = np.zeros_like(canvas)
    return current_pos, canvas


def AI_part(canvas, fingers):
    """AI response for drawn content."""
    global ai_response_text
    if fingers == [0, 1, 1, 1, 0]:  # AI Analysis Mode
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this maths problem.", pil_image])

        # Debugging print statement
        print("AI Response:", response.text)  # Check if AI is returning text

        ai_response_text = response.text
        return response.text
    return None


def generate_frames():
    """Process webcam frames and return output."""
    global previous_pos, canvas
    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        if canvas is None:
            canvas = np.zeros_like(img)

        info = get_hand_gesture(img)
        if info:
            fingers, lmList = info
            previous_pos, canvas = draw_picture(info, previous_pos, canvas)
            AI_part(canvas, fingers)

        image_combined = cv2.addWeighted(img, 0.65, canvas, 0.35, 0)
        _, buffer = cv2.imencode(".jpg", image_combined)
        frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/get_ai_response")
def get_ai_response():
    """API to fetch AI analysis text."""
    print("Sending AI Response to Frontend:", ai_response_text)  # Debugging print
    return jsonify({"response": ai_response_text})


@app.route("/video_feed")
def video_feed():
    """Route for video streaming."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/get_ai_response")
def get_ai_response():
    """API to fetch AI analysis text."""
    return jsonify({"response": ai_response_text})


if __name__ == "__main__":
    app.run(debug=True)
