import streamlit as st
import cv2
import numpy as np
from image_enhancement import image_enhancement
from PIL import Image

st.title("📸 Selective Image Enhancement with Streamlit")

uploaded = st.file_uploader("Upload an Image", type=['png', 'jpg', 'jpeg'])
if not uploaded:
    st.stop()

# Convert PIL image to OpenCV BGR
img = np.array(Image.open(uploaded).convert('RGB'))
bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Initialize the image enhancement engine
ie = image_enhancement.IE(bgr, color_space='HSV')

# Enhancement method choices
method = st.selectbox("Enhancement Method", [
    "Global HE (GHE)",
    "Brightness Preserving HE (BBHE)",
    "Brightness Preserving HE with Maximum Entropy (BPHEME)",
    "Range Limited Bi-Histogram Equalization (RLBHE)",
    "Quantized BBHE (QBHE)",
    "Adaptive Gamma Color‑Preserving (AGCCPF)"
])

# Additional parameter inputs if needed
bins = None
alpha = None
if method == "Quantized BBHE (QBHE)":
    bins = st.slider("Number of Gray Levels (QBHE)", min_value=2, max_value=256, value=128)
elif method == "Adaptive Gamma Color‑Preserving (AGCCPF)":
    alpha = st.slider("Alpha (AGCCPF)", min_value=0.0, max_value=5.0, value=1.0)

# Apply selected enhancement
if method == "Global HE (GHE)":
    out = ie.GHE()
elif method == "Brightness Preserving HE (BBHE)":
    out = ie.BBHE()
elif method == "Brightness Preserving HE with Maximum Entropy (BPHEME)":
    out = ie.BPHEME()
elif method == "Range Limited Bi-Histogram Equalization (RLBHE)":
    out = ie.RLBHE()
elif method == "Quantized BBHE (QBHE)":
    out = ie.QBHE(bins)
elif method == "Adaptive Gamma Color‑Preserving (AGCCPF)":
    out = ie.AGCCPF(alpha)
else:
    out = bgr  # Fallback to original image

# Convert result to RGB for display
enhanced = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)

# Display original and enhanced images
col1, col2 = st.columns(2)
with col1:
    st.image(img, caption="Original Image", use_column_width=True)
with col2:
    st.image(enhanced, caption="Enhanced Image", use_column_width=True)