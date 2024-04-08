import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = '''You are a youtube video summarizer.Take the transcript provided and give the 
            gist of the video, covering all important points. Answer in point form '''

def fetch_transcript_details(youtube_video_url):
    try:
        video_url=youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_url)

        transcript =""
        for i in transcript_text:
            transcript+=" "+i["text"]
        return transcript
    except Exception as e:
        raise e

def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

def notes_to_pdf(notes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=notes)
    pdf_file = "notes.pdf"
    pdf.output(pdf_file)
    return pdf_file

def get_session_state():
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False
    if "summary" not in st.session_state:
        st.session_state.summary = ""

st.title("YT videos to Notes converter")
yt_link = st.text_input("Enter url of the YouTube video")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

get_session_state()

if st.button("Get Notes"):
    transcript_text=fetch_transcript_details(yt_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

        st.session_state.button_clicked = True
        st.session_state.summary = summary

if st.session_state.button_clicked:
    if st.button("Download Notes as PDF"):
        pdf_file = notes_to_pdf(st.session_state.summary)
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()
        st.download_button(label="Click here to download PDF", data=pdf_data, file_name="notes.pdf", mime="application/pdf")
