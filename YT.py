import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import PyPDF2
import base64

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
    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfFileWriter()

    # Create a new PDF page
    pdf_page = PyPDF2.pdf.PageObject.create_text_page(notes)

    # Add the page to the PDF writer
    pdf_writer.add_page(pdf_page)

    # Specify the output file name
    output_pdf = "notes.pdf"

    # Write the PDF to the output file
    with open(output_pdf, "wb") as f:
        pdf_writer.write(f)

    return output_pdf

st.title("YT videos to Notes converter")
yt_link = st.text_input("Enter url of the YouTube video")

if yt_link:
    video_id = yt_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Notes"):
    transcript_text=fetch_transcript_details(yt_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes:")
        st.write(summary)

        if st.button("Download Notes as PDF"):
            pdf_file = notes_to_pdf(summary)
            with open(pdf_file, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="notes.pdf">Download notes as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
