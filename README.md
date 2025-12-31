========================================================
MedinX – Post-Prescription Safety Intelligence Platform
========================================================

Because safety doesn’t end when the doctor writes a prescription.


--------------------------------------------------------
1. PROJECT OVERVIEW
--------------------------------------------------------

MedinX is a post-prescription safety intelligence system that helps patients
identify potential risks after receiving a doctor’s prescription.

The system extracts prescription data using OCR and NLP techniques, analyzes:
- Drug–Drug interactions
- Food–Drug risks
- Age-based safety considerations

It is designed as a safety-support tool and does NOT diagnose diseases,
change dosage, or replace doctors.


--------------------------------------------------------
2. PROBLEM STATEMENT
--------------------------------------------------------

Even when prescriptions are correct:
- Patients may unknowingly take conflicting medicines
- Food habits can reduce drug effectiveness
- Age-related dosage risks are often ignored
- No safety tool exists after leaving the clinic

MedinX addresses this **post-care safety gap** using AI and rule-based analysis.


--------------------------------------------------------
3. WHAT MEDINX DOES
--------------------------------------------------------

MedinX provides:
- OCR-based prescription extraction
- Drug–Drug interaction detection
- Age-based dosage risk awareness
- Backend processing with structured outputs
- Ethical, non-diagnostic safety alerts

MedinX does NOT:
- Diagnose medical conditions
- Prescribe medicines
- Modify dosage
- Replace healthcare professionals


--------------------------------------------------------
4. FILE STRUCTURE & PURPOSE
--------------------------------------------------------

Project Files:

1. app.py
   - Main application entry point
   - Handles user input and triggers backend logic
   - Integrates OCR, interaction checks, and output display

2. backend.py
   - Core business logic
   - Loads CSV medical datasets
   - Performs drug–drug interaction analysis
   - Handles age-based safety rules

3. ocr.py
   - Extracts text from prescription images
   - Converts image input into readable prescription text
   - Acts as the first step in the pipeline

4. age_dosage_data.csv
   - Contains age-wise dosage safety information
   - Used to warn about age-related risks
   - DOES NOT modify prescribed dosage

5. db_drug_interactions.csv
   - Contains known drug–drug interaction data
   - Used for rule-based safety checks

6. requirements.txt
   - Lists Python dependencies required to run the project


--------------------------------------------------------
5. SYSTEM ARCHITECTURE
--------------------------------------------------------

Execution Flow:

Prescription Image/Text
        |
        v
   ocr.py
(Text Extraction)
        |
        v
   app.py
(Application Controller)
        |
        v
   backend.py
(Safety Analysis Engine)
        |
        v
Structured Safety Output


--------------------------------------------------------
6. OCR MODULE (ocr.py)
--------------------------------------------------------

Purpose:
- Converts prescription images into text

Process:
- Takes image input
- Applies OCR
- Outputs raw prescription text

Limitations:
- OCR accuracy depends on image quality
- No medical interpretation is performed


--------------------------------------------------------
7. BACKEND SAFETY ENGINE (backend.py)
--------------------------------------------------------

Responsibilities:
- Reads drug interaction data from CSV
- Matches extracted medicine names
- Detects possible drug–drug interactions
- Checks age-based dosage safety
- Generates safety warnings

Important:
- Backend does NOT change dosage
- Backend does NOT suggest new medicines
- Backend only flags potential risks


--------------------------------------------------------
8. APPLICATION CONTROLLER (app.py)
--------------------------------------------------------

Purpose:
- Connects OCR and backend modules
- Handles user input (image/text)
- Displays results to the user

Acts as:
- Execution coordinator
- Interface between user and logic


--------------------------------------------------------
9. DATASETS USED
--------------------------------------------------------

age_dosage_data.csv:
- Used to identify age-related risk conditions
- Example: pediatric or elderly warnings

db_drug_interactions.csv:
- Contains known drug conflict pairs
- Used for rule-based interaction detection

Both datasets are:
- Static
- Non-predictive
- Safety-oriented


--------------------------------------------------------
10. INSTALLATION & SETUP
--------------------------------------------------------

Step 1: Clone Repository
git clone https://github.com/your-username/MedinX.git
cd MedinX

Step 2: Create Virtual Environment
python -m venv venv

Activate:
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt


--------------------------------------------------------
11. RUNNING THE PROJECT
--------------------------------------------------------

Option 1: Run Main Application
python app.py

Option 2: Run Backend Logic Separately (Testing)
python backend.py

OCR Module Test:
python ocr.py


--------------------------------------------------------
12. SAMPLE INPUT
--------------------------------------------------------

Prescription Image OR Extracted Text:

Patient Age: 65
Medicines:
Aspirin
Ibuprofen


--------------------------------------------------------
13. EXPECTED OUTPUT
--------------------------------------------------------

{
  "extracted_medicines": ["Aspirin", "Ibuprofen"],
  "drug_drug_interactions": [
      "Aspirin and Ibuprofen may increase bleeding risk"
  ],
  "age_based_warning": "Elderly patients require monitoring",
  "safety_alert": true
}


--------------------------------------------------------
14. ETHICAL DESIGN PRINCIPLES
--------------------------------------------------------

- No diagnosis
- No dosage modification
- No treatment recommendation
- Rule-based safety checks only
- Human decision remains final authority


--------------------------------------------------------
15. LIMITATIONS
--------------------------------------------------------

- Depends on OCR accuracy
- Limited to available interaction data
- Not a clinical decision system


--------------------------------------------------------
16. FUTURE IMPROVEMENTS
--------------------------------------------------------

- Improved OCR accuracy
- Food–drug interaction extension
- Mentor escalation integration
- Web-based UI
- Verified medical database integration


--------------------------------------------------------
17. AUTHOR
--------------------------------------------------------

Lankalapalli Kumar
B.Tech – Data Science
Focus: AI, Healthcare Safety, Ethical AI


--------------------------------------------------------
18. DISCLAIMER
--------------------------------------------------------

This project is intended only for educational and safety-support purposes.
It does NOT provide medical advice or diagnosis.
Always consult a licensed medical professional.

========================================================
END OF README
========================================================
