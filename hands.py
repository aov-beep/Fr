
import cv2
import mediapipe as mp

# Ініціалізація MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Камера
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # BGR -> RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Обробка кадру
    result = hands.process(img_rgb)

    # Якщо знайдені руки
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Hands", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC для виходу
        break

cap.release()
cv2.destroyAllWindows()

