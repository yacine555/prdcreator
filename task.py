import requests
import os
import json
import sys, getopt
import config
import torch

from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class Task:

    @staticmethod
    def generatePRD(industry, company, description, strategy, persona, problem, modelname="gpt-3.5-turbo", temp=1):
        """
        Huggingface task to generate a PRD based on some company input
        Use Longchain prompt template with OpenAI LLM

        :param scenario: text scenario to generate story (string)
        :return: text story (string)
        """
        print("Exemple PRD -  Call LLM with a Lonchain prompt tempate: \n")

        aiPromptTempalte  = """
        You are an expert product manager for a {industry} and your role is to write Product Requirements Documents;
        You work for {company}, it is a company that {description};
        The company strategy is to serve the commercial and sales organization of drug manufacturers {strategy};
        """

        human_template = """
        Propose a product requirement document  for the user persona {persona};
        The problem the app solves is that {problem};
        
        Propose a PRD using this document template:
        
        CONTENT: The contents of a PRD
            Title: Give this project a distinct name and a code name.
            Change History: Describe each important change to the PRD, including who changed it, when they changed it, and what they changed.
            Overview: Briefly, what is this project about?  Why are you doing it?
            Success Metrics: What are the success metrics that indicate you're achieving your internal goals for the project?
            Messaging: What's the product messaging marketing will use to describe this product to customers, both new and existing?
            Timeline/Release Planning: What's the overall schedule you're working towards?
            Personas: Who are the target personas for this product, and which is the key persona? For each persona, explain the benefits.
            Persona objectives: These are full stories about how various personas will use the product in context.
            User Stories/Features/Requirements: These are the distinct, prioritized features along with a short explanation as to why this feature is important. Add at least six user stories. Use the framework template: As a 'user persona', I want to 'action', so that I can get 'benefits'. Rank them.
            Not in Scope: list some ideas that you do not usually develop as a version 1 and why. 
            Designs: Include any needed early sketches, and throughout the project, link to the actual designs once they're available.
            Open Issues: List at least 3 key factors you still need to figure out?
            Other Considerations: This is a catch-all for anything else, such as if you make a key decision to remove or add to the project's scope.
        """

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", aiPromptTempalte),
            ("user", human_template)
        ])

        llm=ChatOpenAI(model_name=modelname, temperature=temp)
        output_parser = StrOutputParser()

        chain = chat_prompt | llm | output_parser

        prd = chain.invoke({"industry":industry,"company":company,"description":description, "strategy":strategy, "persona":persona,"problem":problem})

        return prd



    @staticmethod
    def refinePRD(prdDocument, instruction, industry, company, description, strategy, persona, problem, modelname="gpt-3.5-turbo", temp=1):
        """
        Huggingface task to refine a PRD based on some company input
        Use Longchain prompt template with OpenAI LLM

        :param prdDocument: previsously generated socument (string)
        :return: refined PRD (string)
        """
        print("Refine PRD -  Call LLM with a Lonchain prompt tempate: \n")

        aiPromptTempalte  = """
        You are an expert product manager for a {industry} and your role is to write Product Requirements Documents;
        You work for {company}, it is a company that {description};
        The company strategy is to serve the commercial and sales organization of drug manufacturers {strategy};
        """

        human_template = """
        Update the PRD Document provided below by folowing this instruction: {instruction};
        
        PRD Document: {prdDocument} 
        """

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", aiPromptTempalte),
                ("human", human_template),
            ]
        )

        llm = LLMChain(
            llm=ChatOpenAI(model_name=modelname, temperature=temp),
            prompt=chat_prompt,
            verbose=True,
        )

        prd = llm.predict(prdDocument=prdDocument, instruction=instruction, industry=industry, company=company, description=description, strategy=strategy, persona=persona,problem=problem)

        return prd
