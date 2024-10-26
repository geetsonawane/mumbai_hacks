import cv2
import mediapipe as mp
import math
import keyboard  # Or consider using pyautogui for cross-platform
import traceback

# Initialize Mediapipe Hand class and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# It shows small points and coordinates on the tip of fingers
def show_landmarks(landmark, frame, width, height):
    if landmark:
        coords = (int(landmark.x * width), int(landmark.y * height))
        if coords:
            frame = cv2.circle(frame, coords, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(coords), (coords[0] + 10, coords[1] + 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return frame

# Function to press/release gas or brake based on hand openness
def control_keys(hand_type, openness_ratio, frame):
    if hand_type == 'Right':  # Right hand controls gas
        if openness_ratio and openness_ratio >= 0.35:  # Open palm
            keyboard.press("right")
            cv2.putText(frame, "GAS", (40, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        else:
            keyboard.release("right")
    elif hand_type == 'Left':  # Left hand controls brake
        if openness_ratio and openness_ratio >= 0.35:  # Open palm
            keyboard.press("left")
            cv2.putText(frame, "BRAKE", (40, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        else:
            keyboard.release("left")

# Calculate the openness of the hand based on fingertip positions
def calculate_openness(landmarks, width, height):
    if landmarks:
        thumb = landmarks[mp_hands.HandLandmark.THUMB_TIP]
        index = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky = landmarks[mp_hands.HandLandmark.PINKY_TIP]
        wrist = landmarks[mp_hands.HandLandmark.WRIST]
        
        fingertips = [thumb, index, middle, ring, pinky]
        centroid_x = sum([f.x for f in fingertips]) / 5
        centroid_y = sum([f.y for f in fingertips]) / 5

        # Convert centroid to pixel coordinates
        centroid_coords = (int(centroid_x * width), int(centroid_y * height))
        
        if centroid_coords:
            distances = []
            for f in fingertips:
                f_coords = (int(f.x * width), int(f.y * height))
                distance = math.dist(f_coords, centroid_coords)
                distances.append(distance)
            avg_dist = sum(distances) / len(distances)
            wrist_coords = (int(wrist.x * width), int(wrist.y * height))
            wrist_to_centroid = math.dist(centroid_coords, wrist_coords)
            if wrist_to_centroid != 0:
                return avg_dist / wrist_to_centroid
    return None

# Main function to run the video stream and gesture detection
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # Flip the frame horizontally for mirrored view
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Get handedness (Left/Right)
                    hand_type = results.multi_handedness[idx].classification[0].label

                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Calculate openness
                    openness_ratio = calculate_openness(hand_landmarks.landmark, width, height)

                    # Control keys based on openness
                    control_keys(hand_type, openness_ratio, frame)
            
            cv2.imshow('Gesture Controller', frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Escape key to exit
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        traceback.print_exc()
