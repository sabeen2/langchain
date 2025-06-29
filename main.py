## Integrate out code OpenAI API

import os
from typing import cast
from constants import openai_api_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import streamlit as st

from langchain.memory import ConversationBufferMemory

# Initialize OpenAI API key from constant
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")
os.environ["OPENAI_API_KEY"] = cast(str, openai_api_key)  # Cast to str to satisfy type checker

# streamlit framework  
st.title("Celebrity Search Engines")

# create a text input box for the user to enter their prompt
input_text = st.text_input("Search for the celebrity you want to know more about")

#Prompt Template
first_input_prompt = PromptTemplate(
    input_variables=["name"],
    template="Tell me about celebrity {name}",
)

# Memory
person_memory = ConversationBufferMemory(input_key="name", memory_key="chat_history")
birth_year_memory = ConversationBufferMemory(input_key="person", memory_key="chat_history")
events_memory = ConversationBufferMemory(input_key="birth_year", memory_key="events_history")


## OPENAI LLMS
llm = OpenAI(temperature=0.8)
chain = LLMChain(llm=llm, prompt=first_input_prompt, verbose=True, output_key="person", memory=person_memory)

#Prompt Template
second_input_prompt = PromptTemplate(
    input_variables=["person"],
    template="When was {person} born?",
) 

chain2 = LLMChain(llm=llm, prompt=second_input_prompt, verbose=True, output_key="birth_year", memory=birth_year_memory)

third_input_prompt = PromptTemplate(
    input_variables=["birth_year"],
    template="Mention 5 major events around the world in the year {birth_year}?",
)

chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key="events", memory=events_memory)

parent_chain = SequentialChain(
    chains=[chain, chain2, chain3],
    input_variables=["name"],
    output_variables=["person", "birth_year", "events"],
    verbose=True
)

if input_text:
    st.write(parent_chain({"name": input_text}))

    with st.expander("Person Name"):
        st.info(person_memory.buffer)

    with st.expander("Events"):
        st.info(events_memory.buffer)

 
