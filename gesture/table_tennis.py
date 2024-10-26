import cv2
import mediapipe as mp
import pyautogui  # For simulating mouse movements and clicks

# Initialize Mediapipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Variables to track thumb position
thumb_up = False
right_button_pressed = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for natural hand movement direction
    image = cv2.flip(image, 1)

    # Convert the image color to RGB for Mediapipe processing
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect hand landmarks
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the thumb tip position (landmark index 4)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

            thumb_x = int(thumb_tip.x * image.shape[1])
            thumb_y = int(thumb_tip.y * image.shape[0])

            # Define a threshold for thumb position detection
            thumb_threshold = 0.05  # Adjust as necessary

            # Check if the thumb is up or down
            if thumb_tip.y < thumb_base.y - thumb_threshold:  # Thumb is up
                thumb_up = True
                right_button_pressed = False  # Release right button
                # Map thumb position to screen dimensions
                mapped_x = thumb_x * (screen_width / image.shape[1])
                mapped_y = thumb_y * (screen_height / image.shape[0])
                # Move the mouse cursor
                pyautogui.moveTo(mapped_x, mapped_y)
                print("Moving mouse to:", (mapped_x, mapped_y))
            elif thumb_tip.y >= thumb_base.y + thumb_threshold:  # Thumb is down
                thumb_up = False
                # Simulate mouse right button press
                if not right_button_pressed:  # Check if not already pressed
                    pyautogui.mouseDown(button='right')
                    right_button_pressed = True
                    print("Pressing right mouse button")
                # Still allow cursor movement based on thumb position
                mapped_x = thumb_x * (screen_width / image.shape[1])
                mapped_y = thumb_y * (screen_height / image.shape[0])
                pyautogui.moveTo(mapped_x, mapped_y)
                print("Moving mouse to:", (mapped_x, mapped_y))
            else:
                # If the thumb is neutral, release the right button
                if right_button_pressed:
                    pyautogui.mouseUp(button='right')
                    right_button_pressed = False
                    print("Releasing right mouse button")

            # Draw landmarks for visualization (optional)
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the resulting frame
    cv2.imshow('Thumb Gesture Control', image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

















# import cv2
# import mediapipe as mp
# import pyautogui  # For simulating mouse movements

# # Initialize Mediapipe for face detection and landmark tracking
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.7)

# # Start capturing video from the webcam
# cap = cv2.VideoCapture(0)

# # Screen dimensions
# screen_width, screen_height = pyautogui.size()

# # Variables to track head movement
# prev_head_y = None

# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         break

#     # Flip the image horizontally for natural movement
#     image = cv2.flip(image, 1)

#     # Convert the image color to RGB for Mediapipe processing
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Process the image and detect face landmarks
#     results = face_mesh.process(image_rgb)

#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             # Get the position of the nose (landmark index 1)
#             nose_y = face_landmarks.landmark[1].y

#             # Map the nose position to screen height
#             mapped_y = int(nose_y * image.shape[0])
#             # Invert the Y-axis for screen movement
#             mapped_y = screen_height - mapped_y

#             # Move the mouse cursor based on head movement
#             if prev_head_y is not None:
#                 # Calculate movement direction
#                 if nose_y < prev_head_y - 0.02:  # Head tilted up
#                     pyautogui.move(0, -10)  # Move mouse up
#                     print("Head tilting up, moving mouse up")
#                 elif nose_y > prev_head_y + 0.02:  # Head tilted down
#                     pyautogui.move(0, 10)  # Move mouse down
#                     print("Head tilting down, moving mouse down")

#             # Update previous head position
#             prev_head_y = nose_y

#             # Draw landmarks for visualization (optional)
#             mp.solutions.drawing_utils.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

#     # Display the resulting frame
#     cv2.imshow('Head Gesture Control', image)

#     # Exit on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the capture and close windows
# cap.release()
# cv2.destroyAllWindows()


