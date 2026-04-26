import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ----------------------------
# Your class (unchanged)
# ----------------------------
class SnapchatFiltersTasks:
    def __init__(self, model_path='face_landmarker.task'):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=True,
            num_faces=1)
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def overlay_png(self, frame, overlay, x, y, w, h):
        if w <= 0 or h <= 0:
            return frame

        overlay_resized = cv2.resize(overlay, (int(w), int(h)))

        h_img, w_img = frame.shape[:2]
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(w_img, x + int(w))
        y2 = min(h_img, y + int(h))

        overlay_x1 = 0 if x >= 0 else -x
        overlay_y1 = 0 if y >= 0 else -y
        overlay_x2 = overlay_x1 + (x2 - x1)
        overlay_y2 = overlay_y1 + (y2 - y1)

        if x2 <= x1 or y2 <= y1:
            return frame

        overlay_chunk = overlay_resized[overlay_y1:overlay_y2, overlay_x1:overlay_x2]

        alpha = overlay_chunk[:, :, 3] / 255.0
        inv_alpha = 1.0 - alpha

        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha * overlay_chunk[:, :, c] +
                inv_alpha * frame[y1:y2, x1:x2, c]
            )

        return frame

    def apply_filters(self, frame, glasses, moustache, ears=None):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = self.detector.detect(mp_image)

        if result.face_landmarks:
            for face_landmarks in result.face_landmarks:
                h, w, _ = frame.shape

                # 😎 Sunglasses
                left_eye = face_landmarks[33]
                right_eye = face_landmarks[263]

                lx, ly = int(left_eye.x * w), int(left_eye.y * h)
                rx, ry = int(right_eye.x * w), int(right_eye.y * h)

                glass_w = int(1.4 * abs(rx - lx))
                glass_h = int(glass_w * glasses.shape[0] / glasses.shape[1])

                gx = int((lx + rx) / 2 - glass_w / 2)
                gy = int((ly + ry) / 2 - glass_h / 2)

                frame = self.overlay_png(frame, glasses, gx, gy, glass_w, glass_h)

                # 👨 Moustache
                nose = face_landmarks[1]
                mouth_left = face_landmarks[61]
                mouth_right = face_landmarks[291]

                nx, ny = int(nose.x * w), int(nose.y * h)
                mlx = int(mouth_left.x * w)
                mrx = int(mouth_right.x * w)

                mous_w = int(1.3 * abs(mrx - mlx))
                mous_h = int(mous_w * moustache.shape[0] / moustache.shape[1])

                mx = int((mlx + mrx) / 2 - mous_w / 2)
                my = int(ny + 5)

                frame = self.overlay_png(frame, moustache, mx, my, mous_w, mous_h)

        return frame

def draw_face_regions(frame, face_landmarks):
    img = frame.copy()
    h, w, _ = img.shape

    def get_box(indices, color):
        pts = np.array([[int(face_landmarks[i].x * w),
                         int(face_landmarks[i].y * h)] for i in indices])
        x, y, bw, bh = cv2.boundingRect(pts)
        cv2.rectangle(img, (x, y), (x + bw, y + bh), color, 2)

    # ----------------------------
    # Region definitions (MediaPipe 468)
    # ----------------------------
    LEFT_EYE = [33, 133, 160, 159, 158, 157, 173]
    RIGHT_EYE = [362, 263, 387, 386, 385, 384, 398]
    LEFT_EYEBROW = [70, 63, 105, 66, 107]
    RIGHT_EYEBROW = [336, 296, 334, 293, 300]
    NOSE = [1, 2, 98, 327]
    LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
    FACE = list(range(0, 468))

    # ----------------------------
    # Draw rectangles
    # ----------------------------
    get_box(LEFT_EYE, (255, 0, 0))       # Blue
    get_box(RIGHT_EYE, (255, 0, 0))
    get_box(LEFT_EYEBROW, (0, 255, 0))   # Green
    get_box(RIGHT_EYEBROW, (0, 255, 0))
    get_box(NOSE, (0, 255, 255))         # Yellow
    get_box(LIPS, (255, 0, 255))         # Magenta
    get_box(FACE, (0, 0, 255))           # Red

    return img
    

# ----------------------------
# MAIN (Single Image)
# ----------------------------
import matplotlib.pyplot as plt

# ----------------------------
# Load model
# ----------------------------
filter_app = SnapchatFiltersTasks('models/face_landmarker.task')

# ----------------------------
# Load images
# ----------------------------
frame = cv2.imread('images/me.png')
glasses = cv2.imread('images/sunglass.png', cv2.IMREAD_UNCHANGED)
moustache = cv2.imread('images/moustache.png', cv2.IMREAD_UNCHANGED)

if frame is None:
    raise ValueError("Image not found")

# ----------------------------
# Detect landmarks ONCE
# ----------------------------
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
result = filter_app.detector.detect(mp_image)

# ----------------------------
# 1. Original
# ----------------------------
original = frame.copy()

# ----------------------------
# 2. Landmarks visualization
# ----------------------------
landmark_vis = frame.copy()

if result.face_landmarks:
    for face_landmarks in result.face_landmarks:
        landmark_vis = draw_face_regions(landmark_vis, face_landmarks)

# ----------------------------
# 3. Filtered output
# ----------------------------
output = filter_app.apply_filters(frame.copy(), glasses, moustache)

# ----------------------------
# Plot side-by-side
# ----------------------------
plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(landmark_vis, cv2.COLOR_BGR2RGB))
plt.title("Detected Face Regions")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.title("Snapchat-style Filters Applied")
plt.axis('off')

plt.tight_layout()
plt.show()