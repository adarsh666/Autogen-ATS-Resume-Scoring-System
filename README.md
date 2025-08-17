# Professional ATS Resume Scoring System (Streamlit + AutoGen)

## 📌 Objective
Build a comprehensive Applicant Tracking System (ATS) resume scoring solution using Microsoft AutoGen that provides consistent scoring, improvement recommendations, and professional visualizations.

---

## 🏗️ System Architecture

### Core Components
1. **Resume Processing Agent**
   - Parse resumes in multiple formats (PDF, DOCX, TXT)
   - Extract key information (skills, experience, education, etc.)
   - Convert to standardized JSON format

2. **Database Agent**
   - Stores Parsed resume data in Mongodb

3. **ATS Scoring Agent**
   - Implement consistent scoring algorithm
   - Maintain scoring consistency across multiple runs
   - Generate numerical scores with detailed breakdowns

4. **Job Description Analysis Agent**
   - Parse and analyze job descriptions from vector store
   - Identify key requirements and qualifications
   - Create matching criteria for resume evaluation

5. **Improvement Recommendation Agent**
   - Compare resume against job requirements
   - Generate specific improvement suggestions
   - Provide actionable feedback for score enhancement

6. **Visualization Team**
   - Create professional charts and graphs
   - Generate comparison visualizations
   - Produce exportable reports
   - Team consist of 2 agents: `Visualization Agent` and `Code Executor Agent`

---

## ⚙️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/adarsh666/Autogen-ATS-Resume-Scoring-System.git
cd Autogen-ATS-Resume-Scoring-System
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- **Windows**
  ```bash
  venv\Scripts\activate
  ```
- **Linux / Mac**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Before starting, ensure **Docker Desktop** (or Docker Engine) is running, since the AutoGen code executor agent requires Docker to execute code safely.

To start the Streamlit app:
```bash
streamlit run app.py
```

---

## 📂 Sidebar Navigation
The Streamlit application sidebar contains the following options:
1. **Add Job Description to Vector Store**
   - (`Add job description to vector store.py`)
   - Allows uploading and processing job descriptions.

2. **View Resume Database**
   - (`View resume database`)
   - View, search, and manage stored resumes.

---

## 📊 Features
- Resume parsing & structured data extraction
- Consistent ATS-style scoring
- Detailed breakdown of skills, experience, education
- Job description parsing & matching
- Personalized improvement recommendations
- Professional visualizations (charts & comparison reports)