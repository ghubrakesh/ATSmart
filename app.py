import os
import json
import google.generativeai as genai
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def pdf_to_text(resume):
    reader=pdf.PdfReader(resume)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

prompt = """Hey Act Like a skilled or very experience ATS(Application Tracking System)
        with a deep understanding of tech field,software engineering,data science ,data analyst
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide 
        best assistance for improving thr resumes. Assign the percentage Matching based 
        on Jd and
        the missing keywords with high accuracy
        resume:{text}
        description:{jd}

        I want the response in one single string having the structure
        {"JD Match":"%", "MissingKeywords:[]", "Profile Summary":""}
    """

st.title(":orange[ATS]mart")
st.header("Get suggestion to improve your resume ATS", divider='rainbow')
jd = st.text_area("paste the Job Description")
resume = st.file_uploader("Upload your resume", type="pdf", help="Please upload the resume in pdf format")

submit = st.button("Submit")

if submit:
    if resume is not None:
        text = pdf_to_text(resume)
        response = get_gemini_response(prompt)

        response_dict = json.loads(response)

        jd_match = response_dict.get("JD Match", "")
        missing_keywords = response_dict.get("MissingKeywords", [])
        profile_summary = response_dict.get("Profile Summary", "")

        st.subheader(f"Job Description Match: {jd_match}")
        st.subheader("Missing Keywords:")
        st.write(missing_keywords)
        st.subheader("Profile Summary:")
        st.write(profile_summary) 

copyright_text = "&copy; 2023 ghubrakesh"
st.markdown(f'<p style="text-align:center; margin-top: 20px;">{copyright_text}</p>', unsafe_allow_html=True)
