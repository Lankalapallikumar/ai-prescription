from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from fuzzywuzzy import process
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import os

# -----------------------------
# Load Hugging Face Token
# -----------------------------
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise RuntimeError("❌ HF_TOKEN not found. Please add it as a secret in Hugging Face Spaces.")

# -----------------------------
# Load Granite 3.3-2B model
# -----------------------------
model_path = "ibm-granite/granite-3.3-2b-instruct"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"⏳ Loading model on {device}...")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    token=HF_TOKEN,
    device_map="auto",
    torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
)
tokenizer = AutoTokenizer.from_pretrained(model_path, token=HF_TOKEN)

# -----------------------------
# Load datasets
# -----------------------------
if not os.path.exists("db_drug_interactions.csv"):
    raise RuntimeError("db_drug_interactions.csv not found!")
if not os.path.exists("age_dosage_data.csv"):
    raise RuntimeError("age_dosage_data.csv not found!")

df_interactions = pd.read_csv("db_drug_interactions.csv")
df_dosage = pd.read_csv("age_dosage_data.csv")

df_interactions.columns = df_interactions.columns.str.strip()
df_dosage.columns = df_dosage.columns.str.strip()

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DrugInput(BaseModel):
    input_text: str
    age: int

# -----------------------------
# Helper Functions
# -----------------------------
def match_drug_name(drug, drug_list):
    match, score = process.extractOne(drug, drug_list)
    return match if score > 80 else None

def check_interactions(drugs):
    found_interactions = []
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            d1 = match_drug_name(drugs[i], df_interactions["Drug 1"].tolist())
            d2 = match_drug_name(drugs[j], df_interactions["Drug 2"].tolist())
            if d1 and d2:
                match = df_interactions[
                    ((df_interactions["Drug 1"] == d1) & (df_interactions["Drug 2"] == d2)) |
                    ((df_interactions["Drug 1"] == d2) & (df_interactions["Drug 2"] == d1))
                ]
                if not match.empty:
                    found_interactions.append({
                        "drug1": d1,
                        "drug2": d2,
                        "interaction": match.iloc[0]["Interaction Description"]
                    })
    return found_interactions

def get_dosage(drug, age):
    for _, row in df_dosage.iterrows():
        age_group = row["Age Group"].lower()
        if (
            ("infant" in age_group and age <= 2) or
            ("child" in age_group and 2 < age <= 12) or
            ("adult" in age_group and 13 <= age <= 60) or
            ("senior" in age_group and age > 60)
        ):
            if drug.lower() == row["Drug"].lower():
                return {
                    "dosage": row["Dosage"],
                    "frequency": row["Frequency"]
                }
    return None

def generate_summary(drugs):
    conv = [
        {
            "role": "user",
            "content": f"Analyze the interactions and safety of these drugs: {', '.join(drugs)}. Provide a short, clear medical summary with any warnings."
        }
    ]

    inputs = tokenizer.apply_chat_template(
        conv,
        return_tensors="pt",
        add_generation_prompt=True,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    set_seed(42)
    output = model.generate(**inputs, max_new_tokens=512)
    prediction = tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return prediction

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/analyze")
async def analyze_drugs(data: DrugInput):
    try:
        drugs = [d.strip() for d in data.input_text.split(",") if d.strip()]
        if not drugs:
            raise HTTPException(status_code=400, detail="No valid drugs found.")

        interactions = check_interactions(drugs)
        dosages = {drug: get_dosage(drug, data.age) for drug in drugs}
        model_summary = generate_summary(drugs)

        return {
            "input_drugs": drugs,
            "interactions": interactions,
            "dosage_info": dosages,
            "model_summary": model_summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
