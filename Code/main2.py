import cv2
from fer import FER
from graph_utilities import feed_graph
from graph_utilities import update_graph
from DB_utilities import update_last_row
from DB_utilities import create_schema_and_table
from emotion_utilities import get_emotion_probabilities
from emotion_utilities import calculate_emotion_frames
from emotion_utilities import calculate_emotion_percentages
from emotion_utilities import display_emotion_percentage_table
from usability_utilities import measure_usability_by_emotion
from usability_utilities import determine_usability_by_emotion
from statistics_utilities import show_general_usability
from similarity import compute_task_usability
from DB_utilities import fetch_path_similarity

host_name = 'localhost'
database_name = 'ai385project' # you must create the schema manually
user_name = 'root'
password = '4010405'

# Replace the placeholders with your actual database credentials
conn = create_schema_and_table(host_name, database_name, user_name, password)

# Variable to store the total number of frames processed
total_frames = 0

# Load the pre-trained emotion detection model
emotion_detector = FER()

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video from the camera
cap = cv2.VideoCapture(1)

while True:

    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the face region from the frame
        face_roi = frame[y:y + h, x:x + w]

        # Detect emotions in the face region
        emotions = emotion_detector.detect_emotions(face_roi)

        if emotions:
            # Get the probabilities of happy, sad, angry, and neutral emotions
            happy_prob, sad_prob, angry_prob, neutral_prob = get_emotion_probabilities(emotions)

            # Feed data to the graph
            feed_graph(happy_prob, sad_prob, angry_prob, neutral_prob)

            # Update the number of happy, sad, angry, and neutral emotions
            number_happy_frames, number_sad_frames, number_angry_frames, number_neutral_frames = calculate_emotion_frames(happy_prob, sad_prob, angry_prob, neutral_prob)

            # Measure the usability at this time
            measure_usability_by_emotion(happy_prob, sad_prob, angry_prob, neutral_prob)

            # Display the detected emotion label near the face
            detected_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
            cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Update the graph every 10 frames
        if total_frames % 10 == 0:
            update_graph()

        # Increment the total frame count
        total_frames += 1

        # Display the frame
        cv2.imshow('Frame', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Calculate emotion percentages
        happy_percentage, sad_percentage, angry_percentage, neutral_percentage = calculate_emotion_percentages()

        # Display emotion percentages in table format
        display_emotion_percentage_table(happy_percentage, sad_percentage, angry_percentage, neutral_percentage)

        # Determine usability by emotion
        task_usability_by_emotion = determine_usability_by_emotion()

        # fetch the mouse_based_similarity from DB
        mouse_based_similarity_percentage = fetch_path_similarity(conn)

        # Release the video capture and close all windows
        cap.release()
        cv2.destroyAllWindows()

        # compute the system task based on both emotion and mouse tracking
        system_task_usability = compute_task_usability(task_usability_by_emotion, mouse_based_similarity_percentage)

        # update all usability data to DB
        update_last_row(conn, happy_percentage, sad_percentage, angry_percentage, neutral_percentage, mouse_based_similarity_percentage, system_task_usability)
        print("The following results show the number of people who found this task easy and difficult, along with the percentage:")

        # Show general usability statistics
        show_general_usability(conn)
        break

