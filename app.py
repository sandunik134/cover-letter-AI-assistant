import streamlit as st
import os
from dotenv import load_dotenv
import re
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Cover Letter AI Assistant", layout="wide")

# Application title
st.title("Cover Letter AI Assistant")

# Sidebar for API configuration
with st.sidebar:
    st.header("API Configuration")
    huggingface_api_key = st.text_input("Enter your Hugging Face API Key", type="password")
    
    if huggingface_api_key:
        os.environ["HUGGINGFACE_API_KEY"] = huggingface_api_key
        st.success("API Key saved!")

# Function to extract information from resume text
def extract_information(resume_text):
    # Extract name (assuming the first line contains the name)
    name_match = re.search(r'^(.+?)$', resume_text, re.MULTILINE)
    name = name_match.group(1) if name_match else ""
    
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text)
    email = email_match.group(0) if email_match else ""
    
    # Extract phone number
    phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text)
    phone = phone_match.group(0) if phone_match else ""
    
    # Extract skills (looking for keywords after "Skills:" or similar)
    skills_match = re.search(r'Skills:?\s*(.+?)(?=\n\n|\n[A-Z]|$)', resume_text, re.IGNORECASE | re.DOTALL)
    skills = skills_match.group(1).strip() if skills_match else ""
    
    # Extract experience (looking for years of experience)
    experience_match = re.search(r'(\d+)\s+years?\s+.+?experience', resume_text, re.IGNORECASE)
    experience = experience_match.group(0) if experience_match else ""
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "experience": experience
    }

# Function to generate cover letter
def generate_cover_letter(resume_info, company_name, position, job_description):
    # Initialize Hugging Face model
    try:
        llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.7,
            max_new_tokens=500,  # Use max_new_tokens instead of max_length
            huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_KEY")
        )
        
        # Create prompt template for cover letter generation
        template = """
        You are a professional cover letter writer. Create a compelling cover letter for {name} applying for the {position} position at {company_name}.
        
        About the candidate:
        - Skills: {skills}
        - Experience: {experience}
        - Email: {email}
        - Phone: {phone}
        
        About the job:
        {job_description}
        
        Write a formal and professional cover letter that highlights how the candidate's skills and experience make them a good fit for this position.
        
        Cover Letter:
        """
        
        prompt = PromptTemplate(
            input_variables=["name", "email", "phone", "skills", "experience", "company_name", "position", "job_description"],
            template=template
        )
        
        # Initialize memory
        memory = ConversationBufferMemory(input_key="input", memory_key="chat_history")
        
        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt, memory=memory)
        
        # Run the chain
        result = chain.run({
            "name": resume_info["name"],
            "email": resume_info["email"],
            "phone": resume_info["phone"],
            "skills": resume_info["skills"],
            "experience": resume_info["experience"],
            "company_name": company_name,
            "position": position,
            "job_description": job_description
        })
        
        return result
    
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

# Create tabs for different sections
tab1, tab2 = st.tabs(["Input Information", "Generated Cover Letter"])

# Store state
if "resume_info" not in st.session_state:
    st.session_state.resume_info = {}
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

# Tab 1: Input Information
with tab1:
    st.header("Resume Information")
    st.write("Paste your resume text below:")
    
    resume_text = st.text_area("Resume Text", height=200, 
                              placeholder="Name: Jane Smith\nEmail: jane.smith@example.com\nPhone: 555-123-4567\nSkills: Python, Machine Learning, Data Analysis\nExperience: 4 years as Data Analyst")
    
    if st.button("Extract Information"):
        st.session_state.resume_info = extract_information(resume_text)
        st.success("Information extracted!")
    
    # Display extracted information
    if st.session_state.resume_info:
        st.subheader("Extracted Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Name", value=st.session_state.resume_info.get("name", ""), key="name")
            st.text_input("Email", value=st.session_state.resume_info.get("email", ""), key="email")
            st.text_input("Phone", value=st.session_state.resume_info.get("phone", ""), key="phone")
        
        with col2:
            st.text_area("Skills", value=st.session_state.resume_info.get("skills", ""), key="skills")
            st.text_input("Experience", value=st.session_state.resume_info.get("experience", ""), key="experience")
    
    # Job Information
    st.header("Job Information")
    company_name = st.text_input("Company Name")
    position = st.text_input("Position")
    job_description = st.text_area("Job Description", height=150)
    
    if st.button("Generate Cover Letter"):
        if not huggingface_api_key:
            st.error("Please enter your Hugging Face API Key in the sidebar.")
        elif not st.session_state.resume_info:
            st.error("Please extract resume information first.")
        elif not company_name or not position or not job_description:
            st.error("Please fill in all job information fields.")
        else:
            with st.spinner("Generating cover letter..."):
                # Update session state with form inputs
                for key in ["name", "email", "phone", "skills", "experience"]:
                    st.session_state.resume_info[key] = st.session_state[key]
                
                st.session_state.cover_letter = generate_cover_letter(
                    st.session_state.resume_info, 
                    company_name, 
                    position, 
                    job_description
                )
                st.success("Cover letter generated! Go to the 'Generated Cover Letter' tab to view it.")

# Tab 2: Generated Cover Letter
with tab2:
    st.header("Generated Cover Letter")
    
    if st.session_state.cover_letter:
        st.markdown(st.session_state.cover_letter)
        
        # Download button
        st.download_button(
            label="Download Cover Letter",
            data=st.session_state.cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )
    else:
        st.info("No cover letter generated yet. Go to the 'Input Information' tab to create one.")