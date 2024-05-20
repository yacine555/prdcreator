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


hide_submit_text = """
<style>
.css-pxxe24 {
visibility: hidden;
}
<style>
"""

st.markdown(hide_submit_text, unsafe_allow_html=True)


components.html( """
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

text_input_container = st.container()

if 'prdgenerated' not in st.session_state:
    industry = text_input_container.text_input("Industry you work for: (e.g: technology company)","technology company",placeholder="technology company", key="industryID") 
    company = text_input_container.text_input("Your company name:","veeva", placeholder="Mycompany", key="companyID")
    description = text_input_container.text_input("Description of your company activity:","sells CRM app for drug manufacturers" ,placeholder="build HR softwares for mid-size companies", key="descriptionID")
    strategy = text_input_container.text_input("Your company strategy:","Accelerate sales and commercial execution", placeholder="Build a connected HR and Payroll Experience", key="strategyID") 
    persona = text_input_container.text_input("User persona:","sales rep", placeholder="Payroll manager", key="personaID") 
    problem = text_input_container.text_input("What does your feature solve:","we want to build a solution to help pharmaceutical sales reps connect remotely with doctors", placeholder="Help payroll managers ensure pay is accurate and in compliance with local regulation.", key="problemID") 

    st.sidebar.markdown("# Another PMday")
    st.session_state.prdgeneratedExpended = True
else:
    prddocument = st.session_state.prddoc
    industry = st.session_state.industry
    company = st.session_state.company
    description = st.session_state.description
    strategy = st.session_state.strategy
    persona = st.session_state.persona
    problem = st.session_state.problem
    
    st.sidebar.markdown("# Another PMday")
    st.sidebar.markdown("### PRD Information:")
    st.sidebar.markdown("**Industry:** " + industry)
    st.sidebar.markdown("**Company:** " + company)
    st.sidebar.markdown("**Description:** " + description)
    st.sidebar.markdown("**Strategy:** " + strategy)
    st.sidebar.markdown("**Persona:** " + persona)
    st.sidebar.markdown("**Problem:** " + problem)


def click_button_Generate_PRD():
    with st.spinner("Generating PRD..."):
        prddocument = Task.generatePRD(
            industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
        )
        st.session_state.prddoc = prddocument
        
        st.session_state.industry = industry
        st.session_state.company = company
        st.session_state.description = description
        st.session_state.strategy = strategy
        st.session_state.persona = persona
        st.session_state.problem = problem

        st.session_state.prdgenerated = True
        st.session_state.prdgeneratedExpended = True


def click_button_Update_PRD():
    print("industry: " + industry)
    print("instr3: " + st.session_state.instructionID)
    with st.spinner("Updating PRD..."):
        prddocument2 = Task.refinePRD(
            st.session_state.prddoc, st.session_state.instructionID, industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
        )
        st.session_state.prddoc2 = prddocument2
        st.session_state.prdupdated = True
        st.session_state.prdgeneratedExpended = False
        st.session_state.prdupdateround += 1
        

def runstreamlit():
    # st.set_page_config(layout="wide" , page_title="Img 2 audio story", page_icon = "🚀")
    
    # openaikey = st.sidebar.text_input("Openai Key",placeholder="sk-....", key="openaikey")

    
    # # Add a selectbox to the sidebar:
    # llm = st.sidebar.selectbox(
    #     "Select the LLM model:",
    #     ("gpt-3.5-turbo-0125","gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-3.5-turbo-1106"),
    # )

    
    # temp = st.sidebar.slider(
    #     label="Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1
    # )

    text_container = st.container()

    if 'prdavailable' in st.session_state:
        st.markdown("#### Provide instruction for PRD refinement:")
        instruction = st.text_area("","Add more user stories",placeholder="Refine your instruction", max_chars=1000, key="instructionID") 
        bt2 = st.button("Refine PRD", on_click=click_button_Update_PRD, key="B2")
            


if 'prdgenerated' not in st.session_state:
        st.session_state.prdgenerated = False
        st.button('Generate PRD', on_click=click_button_Generate_PRD)
else:
    prdDoc = st.session_state.prddoc
    st.session_state.prdavailable = True
    expander1 = st.expander("Initial PRD document Generated:", expanded=st.session_state.prdgeneratedExpended)
    expander1.write(prdDoc)
    if st.session_state.prdgeneratedExpended:
        st.success("Done Generating!")
  

if 'prdupdated' in st.session_state:
        prdDoc2 = st.session_state.prddoc2
        expander2 = st.expander("Updated PRD document - round " + str(st.session_state.prdupdateround), expanded=True)
        expander2.write(prdDoc2)
        st.success("PRD Updated!")


def main(argv):

    opts, args = getopt.getopt(argv, "ht:", ["task="])
    print("opts ", opts)

    runstreamlit()


if __name__ == "__main__":
    main(sys.argv[1:])
