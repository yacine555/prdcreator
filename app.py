import sys, getopt
import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from task import Task
import streamlit.components.v1 as components


load_dotenv(find_dotenv())



openaikey = os.environ.get("OPENAI_API_KEY")
if(len(openaikey) == 0):
    openaikey = st.secrets["OPENAI_API_KEY"]

LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_TRACING_V2")

if(len(LANGCHAIN_TRACING_V2) == 0):
    os.environ['LANGCHAIN_TRACING_V2'] = st.secrets["LANGCHAIN_TRACING_V2"]
    os.environ['LANGCHAIN_API_KEY'] = st.secrets["LANGCHAIN_API_KEY"]

hide_submit_text = """
<style>
.css-pxxe24 {
visibility: hidden;
}
<style>
"""

st.markdown(hide_submit_text, unsafe_allow_html=True)

components.html( """


<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ND8B1L23GB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-ND8B1L23GB');
</script>

<script>
const inputs = window.parent.document.querySelectorAll('input');
inputs.forEach(input => {
    input.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
});
                
</script>
 """,height=0)

llm = "gpt-3.5-turbo-0125"
temp = 1

if "modelID" in st.session_state:
    llm = st.session_state.modelID
    print("model:" +llm)

if "tempID" in st.session_state:
    temp = st.session_state.tempID
    print("temp:" + str(temp))

prddocument = ""
prddocument2 = ""

industry = ""
company = ""
description = ""
strategy = ""
persona = ""
problem = ""


instruction = ""
if 'prdupdateround' not in st.session_state:
    st.session_state.prdupdateround = 0

st.markdown("# Another PMday -  PRDDay tool")
st.title("Create a Product Requirement Document in minutes")
st.sidebar.markdown("# Another PMday")

text_input_container = st.container()

def validateform():

    return (
            "industryID" in st.session_state and st.session_state.industryID != "" and
            "companyID" in st.session_state and st.session_state.companyID != ""
            "descriptionID" in st.session_state and st.session_state.descriptionID != "" and
            "strategyID" in st.session_state and st.session_state.strategyID != "" and
            "personaID" in st.session_state and st.session_state.personaID != "" and
            "problemID" in st.session_state and st.session_state.problemID != ""
            )

def validateRefineform():

    return (
            "instructionID" in st.session_state and st.session_state.instructionID != ""
            )
    

def click_button_Generate_PRD():
    validform = validateform()
    st.session_state.validform = validform
    if validform:
        with st.spinner("Generating PRD..."):
            prddocument = Task.generatePRD(
                industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
            )
            st.session_state.prddoc = prddocument
            
            # st.session_state.industry = industry
            # st.session_state.company = company
            # st.session_state.description = description
            # st.session_state.strategy = strategy
            # st.session_state.persona = persona
            # st.session_state.problem = problem

            st.session_state.prdgenerated = True
            st.session_state.prdgeneratedExpended = True
            

def click_button_Update_PRD():
    validform = validateRefineform()
    st.session_state.validform = validform
    if validform:
        with st.spinner("Updating PRD..."):

            prddocref = st.session_state.prddoc
            if 'prdupdatedbool' in st.session_state:
                prddocref = st.session_state.prdDocUpdated
            prddocumentUpdated = Task.refinePRD(
                prddocref, st.session_state.instructionID, industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
            )
            st.session_state.prdDocUpdated = prddocumentUpdated
            st.session_state.prdupdatedbool = True
            st.session_state.prdgeneratedExpended = False
            st.session_state.prdupdateround += 1
        

def runstreamlit():
    # st.set_page_config(layout="wide" , page_title="Img 2 audio story", page_icon = "🚀")
    
    # openaikey = st.sidebar.text_input("Openai Key",placeholder="sk-....", key="openaikey")

    if "custom" in st.query_params:

        c = st.sidebar.container()

        c.divider()
        llm = c.selectbox(
            "Select the LLM model:",
            ("gpt-3.5-turbo-0125","gpt-3.5-turbo", "gpt-4o-2024-05-13", "gpt-4o", "gpt-3.5-turbo-1106"),key="modelID"
        )
        
        temp = c.slider(
            label="Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1, key="tempID"
        )

        c.divider()
    

if 'prdgenerated' not in st.session_state:

    if "custom" in st.query_params:
        industry = "technology company"
        company = "Veeva"
        description = "sells CRM app for drug manufacturers" 
        strategy = "Accelerate sales and commercial execution"
        persona = "sales rep"
        problem = "we want to build a solution to help pharmaceutical sales reps connect remotely with doctors"

    industry = text_input_container.text_input("Industry you work for: (e.g: technology company)", industry, placeholder="technology company", key="industryID") 
    company = text_input_container.text_input("Your company name:",company, placeholder="Mycompany", key="companyID")
    description = text_input_container.text_input("Description of your company activity:", description, placeholder="build HR softwares for mid-size companies", key="descriptionID")
    strategy = text_input_container.text_input("Your company strategy:", strategy, placeholder="Build a connected HR and Payroll Experience", key="strategyID") 
    persona = text_input_container.text_input("User persona:", persona, placeholder="Payroll manager", key="personaID") 
    problem = text_input_container.text_input("What does your feature solve:", problem, placeholder="Help payroll managers ensure pay is accurate and in compliance with local regulation.", key="problemID") 

    st.session_state.prdgeneratedExpended = True
else:
    if validateform():
        st.session_state.validform = True
        prddocument = st.session_state.prddoc
        industry = st.session_state.industryID
        company = st.session_state.companyID
        description = st.session_state.descriptionID
        strategy = st.session_state.strategyID
        persona = st.session_state.personaID
        problem = st.session_state.problemID
    
        st.sidebar.markdown("### PRD Information:")
        st.sidebar.markdown("**Industry:** " + industry)
        st.sidebar.markdown("**Company:** " + company)
        st.sidebar.markdown("**Description:** " + description)
        st.sidebar.markdown("**Strategy:** " + strategy)
        st.sidebar.markdown("**Persona:** " + persona)
        st.sidebar.markdown("**Problem:** " + problem)
        

if 'prdgenerated' not in st.session_state:
        st.button('Generate PRD', on_click=click_button_Generate_PRD)
else:
    prdDoc = st.session_state.prddoc
    st.session_state.prdavailable = True
    expander1 = st.expander("Initial PRD document Generated:", expanded=st.session_state.prdgeneratedExpended)
    expander1.write(prdDoc)
    if st.session_state.prdgeneratedExpended:
        st.success("Done Generating!")
  

if 'prdupdatedbool' in st.session_state:
        prdDocUpdated = st.session_state.prdDocUpdated
        expander2 = st.expander("Updated PRD document - round " + str(st.session_state.prdupdateround), expanded=True)
        expander2.write(prdDocUpdated)
        st.success("PRD Updated!")
        st.download_button('Download PRD', prdDocUpdated, file_name="Anotherpmday_prd_document.md")  # Defaults to 'text/plain'

if 'prdavailable' in st.session_state:
    st.markdown("#### Provide instruction for PRD refinement:")
    instruction = st.text_area("Instruction",placeholder="Refine your instruction", max_chars=1000, key="instructionID") 
    bt2 = st.button("Refine PRD", on_click=click_button_Update_PRD, key="B2")
          

if 'validform' in st.session_state:
    if not st.session_state.validform:
        st.error("All fields are required!")


def main(argv):

    opts, args = getopt.getopt(argv, "ht:", ["task="])
    #print("opts ", opts)

    runstreamlit()


if __name__ == "__main__":
    main(sys.argv[1:])
