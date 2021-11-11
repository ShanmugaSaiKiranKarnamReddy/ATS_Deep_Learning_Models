# Appication Ranking System Using Neural Networks
Neural Network Resume Ranking System
Ranks resume in three methods: Text matching using TF-IDF, Keyword matching using predefined list of words, RNN and Ma-LSTM. All programs and models except TF-IDF are inclined towards resumes and job postings under the domain of Computer science.
Workflow:
  1. 2 Inputs in web application (1JD in pdf format and any number of resumes in pdf and image formats)
  2. Orchestrator program that rejects the incorrect extention 
  3. Duplicate detection
  4. Detects the extention and redirects to the respective programs by orchestrator.
  5. Validation: Pdf and word files are validated using resume parser, image files passes through OCR and validated using text matching.
  6. Text extraction: 1. OCR for image resumes. 2. Pdfminer3 for JD and pdf resumes. 
  7. Text matching using TF-IDF
  8. Keyword matching with predefined list of words
  9. MaLSTM model
  10. 4 Outputs: resumes after ranking


# Running the App for testing the models
We need 2 application to run in your local machine
1. A flask application
2. A react application

Requirement: Python 3.5 ~ 3.8(strictly). NodeJs

Steps:
1. Clone the project
2. Backend:
3. Open app2.0/backend in the terminal. Run: pip3 install -r requirements.txt
4. Python3 index.py
5. Frontend:
6. Open app2.0/frontend in the terminal. Run: npm install
7. npm start
