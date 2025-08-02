import streamlit as st
import requests
from paddleocr import PaddleOCR
from PIL import Image
import tempfile
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="AI Medical Prescription Verifier", layout="centered")

# Initialize PaddleOCR once
@st.cache_resource
def load_ocr():
    return PaddleOCR(use_angle_cls=True, lang='en')

ocr = load_ocr()

st.title("💊 AI Medical Prescription Verifier")
st.markdown("""
This app checks:
- **Drug interactions**
- **Age-specific dosage recommendations**
- **AI-generated medical explanations**
""")

# -----------------------------
# Input Mode
# -----------------------------
input_mode = st.radio("Choose Input Mode", ["📝 Manual Text", "🖼️ Prescription Image"])
user_input = ""

if input_mode == "📝 Manual Text":
    user_input = st.text_area("Enter drug names (comma-separated)", "")
else:
    uploaded_file = st.file_uploader("Upload a Prescription Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded_file.read())
            image_path = tmp.name

        st.image(Image.open(image_path), caption="Uploaded Prescription", use_column_width=True)
        st.info("🔍 Extracting drug names using OCR...")
        result = ocr.ocr(image_path, cls=True)

        extracted_text = " ".join([line[1][0] for block in result for line in block])
        user_input = extracted_text.strip()

        if user_input:
            st.success("Extracted Text from Prescription:")
            st.write(user_input)
        else:
            st.warning("⚠️ No text detected. Try a clearer prescription image.")

        # Clean temp file
        os.remove(image_path)

# -----------------------------
# Age input
# -----------------------------
age = st.number_input("Enter Patient's Age", min_value=0, max_value=120, value=30)

# -----------------------------
# Backend URL for Hugging Face
# -----------------------------
BACKEND_URL = "http://127.0.0.1:7860"

# -----------------------------
# Analyze Prescription
# -----------------------------
if st.button("Analyze Prescription"):
    if not user_input.strip():
        st.warning("⚠️ Please enter or extract some drug names.")
    else:
        with st.spinner("Analyzing prescription..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    json={"input_text": user_input, "age": age}
                )
                if response.status_code == 200:
                    result = response.json()

                    # Show input drugs
                    st.subheader("✅ Input Drugs")
                    st.write(", ".join(result["input_drugs"]) if result["input_drugs"] else "None found")

                    # Show interactions
                    st.subheader("⚠️ Drug Interactions")
                    if result["interactions"]:
                        for interaction in result["interactions"]:
                            st.error(f"{interaction['drug1']} × {interaction['drug2']}: {interaction['interaction']}")
                    else:
                        st.success("No harmful interactions detected.")

                    # Show dosage info
                    st.subheader("💊 Recommended Dosage & Frequency")
                    dosage_info = result.get("dosage_info", {})
                    if dosage_info:
                        for drug, dosage in dosage_info.items():
                            if dosage:
                                st.info(f"**{drug}** → {dosage['dosage']} ({dosage['frequency']})")
                            else:
                                st.write(f"No dosage info available for {drug}.")
                    else:
                        st.write("No dosage recommendations available.")

                    # Show model summary
                    st.subheader("🧠 AI Model Summary")
                    st.markdown(result.get("model_summary", "No summary generated."))

                else:
                    st.error(f"❌ Backend error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running. Please start FastAPI server in the same Space.")

# Divider
st.markdown("---")

# -----------------------------
# Hugging Face AI Q&A Section
# -----------------------------
st.header("🧠 Ask a Medical Question")

with st.form("ask_form"):
    prompt = st.text_area("Ask a question (e.g., Is it safe to take Paracetamol with Ibuprofen?)")
    submitted = st.form_submit_button("Ask AI")

if submitted:
    if not prompt.strip():
        st.warning("⚠️ Please enter a valid question.")
    else:
        with st.spinner("Generating answer using Hugging Face model..."):
            try:
                response = requests.post(f"{BACKEND_URL}/explain", json={"prompt": prompt})
                if response.status_code == 200:
                    answer = response.json().get("response", "No answer found.")
                    st.success("🤖 AI Response:")
                    st.markdown(answer)
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Failed to contact backend: {e}")
