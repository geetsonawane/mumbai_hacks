import cv2
import mediapipe as mp
import pyautogui  # For simulating key presses

# Initialize MediaPipe pose solution
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize the video capture from the webcam
cap = cv2.VideoCapture(0)

# Set video resolution (if needed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Variables to track key press state
right_pressed = False
left_pressed = False

# Set up the MediaPipe Pose model
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video")
            break

        # Convert the BGR image to RGB as MediaPipe uses RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Perform pose detection
        results = pose.process(image)

        # Convert the image color back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Check if pose landmarks are detected
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get the y-coordinates of the shoulders
            left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y

            # Print the coordinates for debugging
            print(f"Left Shoulder Y: {left_shoulder_y}, Right Shoulder Y: {right_shoulder_y}")

            # Draw landmarks and connections on the image
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Define a threshold to detect significant movement
            threshold = 0.05  # Adjust this value for sensitivity

            # If right shoulder is higher than left shoulder, press and hold right arrow key
            if right_shoulder_y < left_shoulder_y - threshold:
                if not right_pressed:
                    pyautogui.keyDown('right')  # Simulate pressing and holding the right arrow key
                    right_pressed = True
                    left_pressed = False  # Ensure the left key is not pressed
                    pyautogui.keyUp('left')  # Release the left key if it was pressed
                print("Right shoulder up - Holding Right Arrow Key")

            # If left shoulder is higher than right shoulder, press and hold left arrow key
            elif left_shoulder_y < right_shoulder_y - threshold:
                if not left_pressed:
                    pyautogui.keyDown('left')  # Simulate pressing and holding the left arrow key
                    left_pressed = True
                    right_pressed = False  # Ensure the right key is not pressed
                    pyautogui.keyUp('right')  # Release the right key if it was pressed
                print("Left shoulder up - Holding Left Arrow Key")

            # If shoulders are straight, release both arrow keys
            else:
                if left_pressed:
                    pyautogui.keyUp('left')  # Release the left arrow key
                    left_pressed = False
                if right_pressed:
                    pyautogui.keyUp('right')  # Release the right arrow key
                    right_pressed = False
                print("Shoulders neutral - No movement")

        else:
            print("No pose landmarks detected")  # Useful for debugging if pose detection is failing

        # Display the image in a window
        cv2.imshow('Shoulder Movement Detection', image)

        # Break loop on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

