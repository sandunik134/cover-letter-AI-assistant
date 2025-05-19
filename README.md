# cover-letter-AI-assistant
"AI assistant that generates customised cover letters" Next Steps
Features listcaptures the core functionality of your Cover Letter AI Assistant project, which uses Streamlit and LangChain to help users create professional cover letters by extracting information from their resumes and job descriptions.

Cover Letter AI Assistant
This project creates an AI agent that helps users generate customised cover letters based on their resume information and job descriptions. It uses Streamlit for the user interface and Hugging Face's language models for text generation.
Features

Extract key information from resume text using regex patterns
Generate personalized cover letters based on resume and job details
User-friendly interface with Streamlit
Download the generated cover letter as a text file

Requirements

Python 3.8 or higher
Hugging Face API key

Installation

Clone this repository
Install dependencies:
pip install -r requirements.txt

Create a .env file with your Hugging Face API key:
HUGGINGFACE_API_KEY=your_api_key_here


Usage

Run the application:
streamlit run app.py

Open your browser and go to http://localhost:8501
Enter your Hugging Face API key in the sidebar
Paste your resume text and click "Extract Information"
Enter the job details (company name, position, job description)
Click "Generate Cover Letter"
Go to the "Generated Cover Letter" tab to view and download your cover letter

Getting a Hugging Face API Key

Visit https://huggingface.co/ and create an account
Go to your profile → Settings → Access Tokens
Create a new token (select "read" access)
Copy this token - this is your API key

Project Structure

app.py: Main application file
requirements.txt: Dependencies
.env: For storing your API key (not committed to GitHub)
README.md: Project documentation

Notes

The application uses Mistral-7B-Instruct model from Hugging Face
The regex patterns for information extraction are designed for typical resume formats
Adjust the model parameters in the code to customize the generation style and length
