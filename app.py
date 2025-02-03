import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import json
import os
import re

# Initialize Vertex AI
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = "us-central1"  # Change to your location
vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_analysis(transcript_json):
    """
    Generates user stories, epics, ambiguity analysis, problem statement, and success criteria
    from a JSON transcript using Vertex AI's Gemini Pro model.

    Args:
      transcript_json (str): A JSON string of the transcript.

    Returns:
      dict: A dictionary containing the generated user stories, epics,
            ambiguity analysis, problem statement, and success criteria.
    """

    model = GenerativeModel("gemini-pro")

    prompt = f"""
    You are a expert product manager, who is an expert at understanding business needs and breaking them down to engineering.
    Given the following transcript in JSON format:
    
    {transcript_json}
    
    Analyze the transcript and provide the following outputs:
    1. **User Stories:** Create a series of user stories in the format: "As a [user persona], I want [goal], so that [benefit]".
    2. **Epics:** Create a series of Epics. Each user story should be assigned to an Epic.
    3. **Ambiguity Analysis:** Identify any user stories that you feel are ambiguous and require further user feedback or clarification. Clearly indicate why human review is required.
    4. **Problem Statement:** Generate a simple problem statement for the initiative that encompasses all user stories and provides an executive summary of the problem being solved.
    5. **Success Criteria:** Generate a single success criteria statement for the initiative. Ensure that this criteria is SMART (Specific, Measurable, Achievable, Relevant, Time-bound) and define how it could be measured.
    
    Please provide the response in plain text format, with clear sections for each output and clear titles to easily identify each section such as User Stories:, Epics: ,Ambiguity Analysis:, Problem Statement:, Success Criteria:
    """

    response = model.generate_content(
        contents=prompt,
        generation_config={
            "max_output_tokens": 8192, # Increased limit to handle longer responses
            "temperature": 0.2
        }
    )
    
    # Parse the plain text response
    text_output = response.text
    
    sections = {}
    
    # Regex to split the text into sections
    section_matches = re.split(r'(User Stories:|Epics:|Ambiguity Analysis:|Problem Statement:|Success Criteria:)', text_output)

    current_section = None
    for item in section_matches:
      item = item.strip()
      if item in ["User Stories:", "Epics:", "Ambiguity Analysis:", "Problem Statement:", "Success Criteria:"]:
        current_section = item.replace(":","").lower().replace(" ","_")
        sections[current_section] = []
      elif current_section:
        sections[current_section].append(item)


    for key in sections.keys():
      sections[key] = "\n".join(sections[key]).strip()
      
    return sections



# --- Streamlit UI ---
st.title("Transcript Analyzer with Gemini Pro")

transcript_input = st.text_area("Enter Transcript JSON here", height=200)

if st.button("Analyze Transcript"):
    if transcript_input:
        try:
           transcript_json = json.loads(transcript_input)
           with st.spinner("Analyzing transcript with Gemini Pro..."):
                analysis_results = generate_analysis(json.dumps(transcript_json))

           if "error" in analysis_results:
            st.error(f"Error: {analysis_results['error']}")
           else:
                st.subheader("Analysis Results")

                st.subheader("User Stories:")
                st.write(analysis_results.get("user_stories",""))

                st.subheader("Epics:")
                st.write(analysis_results.get("epics",""))

                st.subheader("Ambiguity Analysis:")
                st.write(analysis_results.get("ambiguity_analysis",""))

                st.subheader("Problem Statement:")
                st.write(analysis_results.get("problem_statement",""))

                st.subheader("Success Criteria:")
                st.write(analysis_results.get("success_criteria",""))
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please provide valid JSON.")


    else:
        st.warning("Please enter a transcript JSON.")