import streamlit as st
import google.generativeai as genai
import json

# Setup the page layout
st.set_page_config(page_title="LinkedIn Profile Analyzer", page_icon="📈", layout="wide")

st.title("📈 LinkedIn Profile Analyzer & Optimizer")
st.markdown("Paste your LinkedIn profile text below, and our AI will score it and generate ready-to-use content tailored to your industry.")

# Sidebar for API Key (For testing purposes)
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.markdown("[Get your free API key here](https://aistudio.google.com/app/apikey)")

# Main Input Section
target_industry = st.text_input("What is your Target Industry or Job Title? (e.g., Customer Success, FinTech, Legal)")
profile_text = st.text_area("Paste your LinkedIn Profile Text here:", height=200)

if st.button("Analyze Profile", type="primary"):
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
    elif not target_industry or not profile_text:
        st.warning("Please provide both your target industry and profile text.")
    else:
        with st.spinner("Analyzing your profile... This takes a few seconds."):
            try:
                # Configure the Gemini API
                genai.configure(api_key=api_key)
                
                # We use Gemini 1.5 Pro for complex structured output
                model = genai.GenerativeModel('gemini-1.5-pro') 
                
                # The Master Prompt
                prompt = f"""
                You are an elite executive recruiter. Analyze this LinkedIn profile text.
                Target Industry: {target_industry}
                Raw Profile Text: {profile_text}
                
                Return a strict JSON object with this exact structure:
                {{
                  "overall_score": 7.5,
                  "executive_summary": "One sentence summary.",
                  "feedback": {{
                    "headline": "Critique of headline",
                    "about_section": "Critique of about section",
                    "experience": "Critique of experience"
                  }},
                  "copy_paste_content": {{
                    "headline_options": ["Option 1", "Option 2", "Option 3"],
                    "about_section_rewrite": "A 3-paragraph rewritten about section in the first person."
                  }}
                }}
                Do not include any markdown formatting like ```json in the output, just the raw JSON text.
                """
                
                response = model.generate_content(prompt)
                
                # Parse the JSON response
                result = json.loads(response.text)
                
                # --- DASHBOARD UI ---
                st.divider()
                st.header(f"Overall Score: {result['overall_score']} / 10")
                st.write(result['executive_summary'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔍 Section Breakdown")
                    st.info(f"**Headline:** {result['feedback']['headline']}")
                    st.warning(f"**About Section:** {result['feedback']['about_section']}")
                    st.success(f"**Experience:** {result['feedback']['experience']}")
                
                with col2:
                    st.subheader("✨ Ready-to-Use Copy-Paste Content")
                    st.write("**Headline Options:**")
                    for option in result['copy_paste_content']['headline_options']:
                        st.code(option, language="text")
                        
                    st.write("**New About Section:**")
                    st.code(result['copy_paste_content']['about_section_rewrite'], language="text")

            except Exception as e:
                st.error(f"An error occurred: {e}. Please ensure your text is clean and try again.")
              
