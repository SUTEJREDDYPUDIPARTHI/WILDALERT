WILDALERT: Smart Wildlife Detection and IoT-Integrated Deterrence System

🔍 Project Overview

WILDALERT is a smart wildlife detection and deterrence system that uses YOLOv8 for real-time animal recognition and Arduino-based IoT hardware to send SMS alerts and trigger sound-based deterrents. Built with a Streamlit web interface, it enables secure monitoring through image, video, or live webcam inputs. This system provides a cost-effective, non-lethal, and automated solution to reduce human-wildlife conflicts.

🧠 Technologies Used

- YOLOv8 (Ultralytics) – For fast and accurate animal detection
- Streamlit – User friendly web-based interface
- OpenCV + CVZone – For image, video and Live processing
- SQLite – Lightweight database for login system
- Arduino (DFPlayer + GSM + LCD) – For hardware-based deterrence, Sound Deterrence, and Alert Messages via SMS, Display Detected Animal Name.

📦 Dataset

The YOLOv8 model is trained on a custom wildlife dataset from Roboflow:
[WildVision Dataset – Roboflow](https://universe.roboflow.com/jivesh-kalra-qlq2g/wildvision/dataset/5)

📸 Hardware Integration

Hardware Setup![Hardware Integration](https://github.com/user-attachments/assets/38ac17b6-bf11-4ccc-a4bd-ea5162395f0e)

Hardware Components:
- GSM SIM800L
- 16x2 LCD
- Arduino Uno 328
- Speaker & Power Source
- Breadboard

⚙️ How to Run the App

1. Install Requirements
pip install -r requirements.txt

2. Run Streamlit App
streamlit run final.py

3. Upload image/video or enable webcam to detect wildlife.
Upon detection of specific animals, the system:
- Diaplays Animal name
- Sends SMS using GSM module
- Plays a sound through speaker

🙏 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Roboflow for Dataset Hosting](https://roboflow.com/)
- [Streamlit Community](https://streamlit.io/)
- [OpenAI](https://openai.com/) for help and support
