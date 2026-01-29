import cv2
import mediapipe as mp
import numpy as np
import joblib
from device.ble_discovery import discover
from device.wifi_transfer import send
from security.crypto import encrypt
from Crypto.Random import get_random_bytes

# Load gesture model
model = joblib.load("gesture/gesture_model.pkl")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

key = get_random_bytes(32)

def extract_features(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if not result.multi_hand_landmarks:
        return None

    features = []
    for p in result.multi_hand_landmarks[0].landmark:
        features.extend([p.x, p.y, p.z])

    return np.array(features)

cap = cv2.VideoCapture(0)

print("System started — perform TRANSFER gesture")

while True:
    ret, frame = cap.read()

    features = extract_features(frame)
    if features is not None:
        gesture = model.predict([features])[0]

        if gesture == "TRANSFER":
            print("Gesture detected — discovering device")
            ip = discover()

            data = b"Hello from hand gesture transfer"
            encrypted = encrypt(data, key)

            send(ip, encrypted)
            print("Data sent securely")
            break

    cv2.imshow("Hand Transfer", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
