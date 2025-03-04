import os
import cv2
import google.generativeai as genai
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1000)
cap.set(4, 720)

# Initialize HandDetector
detector = HandDetector(
    staticMode=False,
    maxHands=1,
    modelComplexity=1,
    detectionCon=0.7,
    minTrackCon=0.5,
)

def get_hand_gesture(img):
    """Detects hand and returns finger status."""
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    return None, None

def draw_picture(info, previous_pos, canvas):
    """Handles drawing logic on the canvas."""
    if info is None:
        return previous_pos, canvas

    fingers, lmList = info
    current_pos = None

    if fingers == [0, 1, 0, 0, 0]:  # Index finger up
        current_pos = tuple(lmList[8][:2])  # Convert to tuple (x, y)
        if previous_pos:
            cv2.line(canvas, previous_pos, current_pos, (255, 0, 255), 9)
        previous_pos = current_pos

    elif fingers == [1, 1, 1, 1, 1]:  # Clear canvas
        canvas.fill(0)

    return previous_pos, canvas

def AI_part(canvas, fingers):
    """Processes the drawing using AI when required gesture is detected."""
    if fingers == [0, 1, 1, 1, 0]:  # Specific gesture for AI trigger
        pil_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))

        try:
            response = model.generate_content(["Solve this math problem.", pil_image])
            print(response.text)
        except Exception as e:
            print("AI Error:", str(e))

# Initialize variables
previous_pos = None
canvas = None

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if canvas is None:
        canvas = np.zeros_like(img)

    info = get_hand_gesture(img)
    
    if info:
        fingers, lmList = info
        previous_pos, canvas = draw_picture(info, previous_pos, canvas)
        AI_part(canvas, fingers)

    # Combine original image and drawing
    image_combined = cv2.addWeighted(img, 0.65, canvas, 0.35, 0)

    # Display windows
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", canvas)
    cv2.imshow("Image Combined", image_combined)

    if cv2.waitKey(1) == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
