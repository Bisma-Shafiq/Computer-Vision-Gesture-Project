# Computer Vision Maths Gesture Project
📌 Overview
The Computer Vision Maths Gesture Project is an AI-powered application that uses MediaPipe and OpenCV to detect hand gestures, enabling users to draw mathematical symbols or problems in the air. The system then leverages Google Gemini AI to recognize and solve the mathematical expressions in real-time.

# 🚀 Features
 ✔️ Real-Time Hand Gesture Detection – Uses MediaPipe and cvzone for accurate tracking.
✔️ AI-Powered Math Solver – Converts hand-drawn equations into text and solves them using Google Gemini AI.
 ✔️ Drawing Interface – Allows users to draw mathematical symbols using finger gestures.
✔️ Gesture-Based Commands – Supports clearing the canvas, drawing, and triggering AI processing with hand gestures.
✔️ Seamless Integration – Built with OpenCV, Flask, and Streamlit for easy deployment and UI interaction.

# 🏗 Tech Stack
🔹 Programming Language: Python

🔹 Computer Vision: OpenCV, MediaPipe, cvzone

🔹 Machine Learning & AI: Google Gemini AI

🔹 Backend: Flask

🔹 Frontend: Streamlit

🔹 Environment Management: Python-dotenv

🔹 Data Processing: NumPy, Pandas

# ⚡ Installation & Setup

1️- Clone the Repository

git clone https://github.com/your-username/Computer-Vision-Maths-Gesture-Project.git
cd Computer-Vision-Maths-Gesture-Project

2️- Create and Activate a Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Requirements
pip install -r requirements.txt

# API Key
Set Up API Key (Google Gemini AI)

Create a .env file in the project root and add:

GOOGLE_API_KEY=your_api_key_here

# 🎯 Usage Guide
1️⃣ Run the script and ensure your webcam is active.

2️⃣ Perform gestures to draw symbols (index finger up for drawing).

3️⃣ AI Processing Trigger: Hold up three fingers ([0, 1, 1, 1, 0]) to let AI solve the equation.

4️⃣ Clear Canvas: Show all five fingers ([1, 1, 1, 1, 1]).

# 🛠 Troubleshooting
❌ DLL Load Failed (MediaPipe Error)?

Ensure Python 3.7 - 3.10 is installed.
Install Microsoft Visual C++ Redistributable here.

pip uninstall mediapipe -y

pip install mediapipe --no-cache-dir

# ❌ Google Gemini API Not Working?

Check if .env contains the correct API key.

Ensure you have access to the Gemini API via Google Cloud.


