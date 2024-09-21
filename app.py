import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Please act as a highly proficient Applicant Tracking System (ATS) with expertise in the fields of technology, software engineering, data science, data analysis, and big data engineering. Your primary task is to analyze resumes based on a provided job description. 
You should:
1. Evaluate the resume's relevance to the job description considering the competitive nature of the current job market.
2. Identify missing keywords and skills that are crucial for the job.
3. Provide actionable suggestions for improving the resume's match to the job description.
4. Assign a percentage match based on how well the resume aligns with the job description, highlighting specific areas of improvement with high precision.

resume:{text}
description:{jd}

I want the response in one single string having the structure

    "JD Match":"%",
    "MissingKeywords:[]",
    "Profile Summary":"" 

"""

## streamlit app
st.title("ATS checker")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)