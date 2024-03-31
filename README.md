# YT Video to Notes Converter

This project is a simple web application built with Streamlit that allows users to convert YouTube video transcripts into summarized notes. It utilizes Google's generative AI model to generate concise notes based on the transcript of the provided video.

## Features

- Extracts transcript from YouTube videos.
- Generates summarized notes from the extracted transcript.
- Converts the generated notes into a downloadable PDF.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VanshikWaghela/YTvideo_to_Notes.git
   ```

2. Navigate to the project directory:

   ```bash
   cd YTvideo_to_Notes
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Enter the URL of the YouTube video in the text input provided.
3. Click on the "Get Notes" button to extract the transcript and generate summarized notes.
4. Click on the "Download Notes as PDF" button to download the generated notes in PDF format.

## Dependencies

- Streamlit
- dotenv
- google-generativeai
- youtube-transcript-api
- PyPDF2

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements or features you'd like to add.
