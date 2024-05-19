import sys, getopt
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from task import Task


load_dotenv(find_dotenv())

st.markdown("# PMDAY PRD DEMO")
st.sidebar.markdown("# Main")


def runstreamlit():
    # st.set_page_config(layout="wide" , page_title="Img 2 audio story", page_icon = "🚀")
    st.title("Create a PRD in a  minute")

    openaikey = st.sidebar.text_input("Openai Key",placeholder="sk-....", key="openaikey")

    llm = "gpt-3.5-turbo-0125"
    # # Add a selectbox to the sidebar:
    # llm = st.sidebar.selectbox(
    #     "Select the LLM model:",
    #     ("gpt-3.5-turbo-0125","gpt-3.5-turbo", "gpt-4-1106-preview", "gpt-3.5-turbo-1106"),
    # )

    temp = 1
    # temp = st.sidebar.slider(
    #     label="Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1
    # )


    industry = st.text_input("Industry you work for: (e.g: technology company)","technology company",placeholder="technology company", key="industry") 
    company = st.text_input("Name of your company: (e.g: www.veeva.com)","www.veeva.com", placeholder="www.veeva.com", key="company")
    description = st.text_input("Description of your company: (e.g: sells CRM app for drug manufacturers)","sells CRM app for drug manufacturers" ,placeholder="sells CRM app for drug manufacturers", key="description")
    strategy = st.text_input("Strategy of your company:(e.g: serve the commercial and sales organization of drug manufacturers)","serve the commercial and sales organization of drug manufacturers", placeholder="serve the commercial and sales organization of drug manufacturers", key="strategy") 
    persona = st.text_input("User persona:(e.g: sales rep)","sales rep", placeholder="sales rep", key="persona") 
    problem = st.text_input("What is what the product solve:(e.g: we want to build a solution to help pharmaceutical sales reps connect remotely with doctors. This an additional feature)","we want to build a solution to help pharmaceutical sales reps connect remotely with doctors. This an additional feature", placeholder="we want to build a solution to help pharmaceutical sales reps connect remotely with doctors. This an additional feature.", key="problem") 

    prddocument = ""


    if 'PRD' not in st.session_state:
        expander = st.expander("PRD document")
        if st.button("Generate PRD", key="B1"):
            with st.spinner("Generating PRD..."):
                prddocument = Task.generatePRD(
                    industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
                )
                
                expander.write(prddocument)
                # with st.expander("PRD document"):
                #     st.write(prddocument)

                st.session_state['PRD'] = prddocument

            st.success("Done!")

    if 'PRD' in st.session_state:
        expander2 = st.expander("PRD document updated ")
        instruction = st.text_input("PRD modif instruction: (e.g: add one more user case)","add one more user case",placeholder="add one more user case", key="instruction") 
        bt2 = st.button("Update PRD", key="B2")
        
        if bt2:
            with st.spinner("Update PRD..."):
                prddocument2 = Task.refinePRD(
                    st.session_state['PRD'], instruction, industry, company, description, strategy, persona, problem, openaikey, modelname=llm, temp=temp
                )
            expander2.write(prddocument2)
            st.success("Updated!")




def main(argv):
    print("Run main PRDs ")

    opts, args = getopt.getopt(argv, "ht:", ["task="])
    print("opts ", opts)

    runstreamlit()


if __name__ == "__main__":
    main(sys.argv[1:])
