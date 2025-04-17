import streamlit as st
from passlib.hash import pbkdf2_sha256
from ultralytics import YOLO
import cv2
import math
import cvzone
import tempfile
import numpy as np
import base64
import serial
import time
import sqlite3
from geopy.geocoders import Nominatim


def home_page():
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            color: black;
        }
        .big{
            font-size:50px !important;
            color: Red;
                }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='big'>Welcome to the Wild Animal Detection", unsafe_allow_html=True)
    st.markdown("<div class='big-font'>This application uses advanced YOLOV8 techniques to detect Wild animal in images, videos, and live webcams.</div>", unsafe_allow_html=True)
    st.markdown("<div class='big-font'>Please login or signup to use the system.</div>", unsafe_allow_html=True)


def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


def create_table(conn):
    """ Create a table for storing user data """
    try:
        sql = '''CREATE TABLE IF NOT EXISTS users (
                    username text PRIMARY KEY,
                    password text NOT NULL
                 );'''
        conn.execute(sql)
    except Exception as e:
        print(e)


def create_detection_table(conn):
    """ Create a table to store detection data """
    try:
        sql = '''CREATE TABLE IF NOT EXISTS detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal_name TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    location TEXT
                 );'''
        conn.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)


def insert_detection(animal_name, location, conn):
    """ Insert detection information into the database """
    try:
        sql = ''' INSERT INTO detections(animal_name, location)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (animal_name, location))
        conn.commit()
    except Exception as e:
        print(e)


def set_background_image(image_file):
    with open(image_file, "rb") as file:
        base64_image = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def get_location():
    """ Function to get location information (example with geopy) """
    geolocator = Nominatim(user_agent="wild_alert")
    location = geolocator.geocode("current location")  # Use a more accurate method in real-world scenario
    if location:
        return f"{location.latitude}, {location.longitude}"
    return "Unknown Location"


# Initialize session state for user authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# User database simulation (in-memory)
users = {}

# Initialize session state for user data if not already present
if 'users' not in st.session_state:
    st.session_state['users'] = {}

def signup(username, password, conn):
    """ Sign up a new user """
    try:
        hashed_password = pbkdf2_sha256.hash(password)
        sql = ''' INSERT INTO users(username,password)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (username, hashed_password))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def login(username, password):
    if username in st.session_state['users'] and pbkdf2_sha256.verify(password, st.session_state['users'][username]):
        st.session_state['logged_in'] = True
        return True
    return False


# Initialize database connection
db_file = 'your_database.db'
conn = create_connection(db_file)
create_table(conn)
create_detection_table(conn)


def signup_form():
    with st.form("signup"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Signup")

        if submit:
            if signup(username, password, conn):  # Assuming signup() returns True on success
                st.success("Signup successful! Please login.")
                st.session_state['page'] = 'Login'  # Redirect to login page
            else:
                st.error("Username already exists or an error occurred.")


def validate_login(username, password, conn):
    """ Validate login credentials """
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        user_data = cur.fetchone()
        if user_data:
            stored_password = user_data[0]
            return pbkdf2_sha256.verify(password, stored_password)
        return False
    except Exception as e:
        print(e)
        return False


def login_form():
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if validate_login(username, password, conn):
                st.session_state['logged_in'] = True  # Set logged_in to True
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or password.")


def send_command_to_arduino(command):
    try:
        with serial.Serial('COM6', 9600, timeout=1) as ser:
            time.sleep(2)  # Allow time for Arduino to initialize
            print("Sending command to Arduino:", command)
            ser.write(command.encode())  # Send command
            response = ser.readline().decode().strip()  # Read response
            print("Response from Arduino:", response)
    except serial.SerialException as e:
        print(f"Error in serial communication: {e}")


# Main app for pothole detection
def main_app():
    # Load YOLO model
    model = YOLO('best.pt')
    st.title('Wild Animal Detection')

    # Add options for user input: Image, Video, or Live Stream
    input_option = st.radio("Choose input type", ('Image', 'Video', 'Live Stream'))

    # Logout button
    if st.button('Logout'):
        st.session_state['logged_in'] = False

    def process_frame(frame):
        frame = cv2.resize(frame, (640, 480))
        result = model(frame, stream=True)

        for info in result:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                if confidence > 50:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

                    detected_animal = model.names[Class]
                    location = get_location()
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Store detection in the database
                    insert_detection(detected_animal, location, conn)

                    # Add timestamp and location to the frame display
                    cvzone.putTextRect(frame, f'{detected_animal} {confidence}%', [x1 + 8, y1 + 100], scale=1.5, thickness=2)

                    if detected_animal == "bear":
                        send_command_to_arduino("E")
                    elif detected_animal == "cat":
                        send_command_to_arduino("E")
                    # Add logic for other animals...

        return frame

    # Handling different input options
    if input_option == 'Image':
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png","webp"])
        if uploaded_file is not None:
            image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
            processed_image = process_frame(image)
            st.image(processed_image, channels="BGR", use_column_width=True)

    elif input_option == 'Video':
        uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi","webm"])
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(uploaded_file.read())
            cap = cv2.VideoCapture(tfile.name)
            frameST = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                processed_frame = process_frame(frame)
                frameST.image(processed_frame, channels="BGR", use_column_width=True)

            cap.release()

    elif input_option == 'Live Stream':
        st.write("Live Stream from Webcam")

        # Streamlit components for displaying webcam feed and processed frames
        frame_window = st.image([])
        frame_processed = st.image([])

        # Start capturing from the webcam
        cap = cv2.VideoCapture(0)  # 0 is typically the default webcam

        frame_count = 0  # Counter for unique button key

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Process the frame
            processed_frame = process_frame(frame)  # Display the processed frames
            frame_processed.image(processed_frame, channels='BGR')

            # Break the loop if necessary, using a unique key for the button
            if st.button('Stop Streaming', key=f'stop_button_{frame_count}'):
                break

            frame_count += 1

        cap.release()


def dashboard_page(conn):
    """ Display previous detections in a dashboard """
    st.title("Detection Dashboard")
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT animal_name, timestamp, location FROM detections ORDER BY timestamp DESC")
        rows = cur.fetchall()
        if rows:
            st.write("### Previous Detections")
            for row in rows:
                animal_name, timestamp, location = row
                st.write(f"**Animal:** {animal_name} | **Time:** {timestamp} | **Location:** {location}")
        else:
            st.write("No detections yet.")
    except Exception as e:
        print(e)
        st.write("Error retrieving data from the database.")


if 'page' not in st.session_state:
    st.session_state['page'] = 'Home' 

# App routing
if not st.session_state.get('logged_in'): 
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose an option", ["Home", "Login", "Signup"], index=["Home", "Login", "Signup"].index(st.session_state['page']))

    if option == "Home":
        home_page()
    elif option == "Signup":
        signup_form()
    else: 
        login_form()
else:
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose an option", ["Home", "Dashboard", "Logout"], index=["Home", "Dashboard", "Logout"].index(st.session_state['page']))

    if option == "Home":
        main_app()
    elif option == "Dashboard":
        dashboard_page(conn)
    else: 
        st.session_state['logged_in'] = False
