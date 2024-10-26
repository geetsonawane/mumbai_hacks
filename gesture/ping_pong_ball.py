import cv2
import mediapipe as mp
import keyboard  # For key presses

# Initialize Mediapipe for face tracking
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Variables to detect head movement
neutral_y = None  # This will be set as the "center" position
move_threshold = 20  # Sensitivity for detecting head movement

# Flags to track key states
is_up_pressed = False
is_down_pressed = False

def control_paddle_based_on_head_movement(head_y):
    global neutral_y, is_up_pressed, is_down_pressed
    
    # If neutral_y is not set, set it to the initial head position
    if neutral_y is None:
        neutral_y = head_y
        print("Setting neutral position at:", neutral_y)
        return
    
    # Calculate the difference between the current y and the neutral y position
    diff_y = head_y - neutral_y
    
    # If head moves up (above the neutral position), press and hold the "up" key
    if diff_y < -move_threshold and not is_up_pressed:
        keyboard.press('up')  # Keep the "up" key pressed
        is_up_pressed = True  # Mark that "up" is pressed
        if is_down_pressed:   # Release "down" if it's pressed
            keyboard.release('down')
            is_down_pressed = False
            print("Released 'down' key")

        print("Pressed 'up' key")

    # If head moves down (below the neutral position), press and hold the "down" key
    elif diff_y > move_threshold and not is_down_pressed:
        keyboard.press('down')  # Keep the "down" key pressed
        is_down_pressed = True  # Mark that "down" is pressed
        if is_up_pressed:       # Release "up" if it's pressed
            keyboard.release('up')
            is_up_pressed = False
            print("Released 'up' key")

        print("Pressed 'down' key")
    
    # If head returns to the neutral position, release both keys
    if -move_threshold <= diff_y <= move_threshold:
        if is_up_pressed:
            keyboard.release('up')
            is_up_pressed = False
            print("Released 'up' key")
        if is_down_pressed:
            keyboard.release('down')
            is_down_pressed = False
            print("Released 'down' key")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for natural head movement direction
    image = cv2.flip(image, 1)

    # Convert the image color to RGB for Mediapipe processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect face landmarks
    result = face_mesh.process(image_rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Get the y-coordinate of the nose tip (landmark index 1)
            nose_tip = face_landmarks.landmark[1]
            head_y = int(nose_tip.y * image.shape[0])  # Convert relative to absolute y-coordinate

            # Call the function to control the paddle based on head movement
            control_paddle_based_on_head_movement(head_y)

            # Optionally draw the face mesh on the screen (for debugging)
            mp_drawing.draw_landmarks(
                image, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS
            )

    # Display the resulting frame (for debugging)
    cv2.imshow('Head Tracker', image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()



