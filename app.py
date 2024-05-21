import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType


st.set_page_config(
    page_title="FAST API Converter",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE",type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("FAST API Converter👩🏼‍💻")
st.sidebar.markdown("## Welcome to the FAST API Converter!")
st.sidebar.markdown("This App Harnesses power of Lyzr Automata to Convert your Python function to Fast API. You Need to input Your Python Function and this app convert your Python function in working API.")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def lyrics_writer(code_snippet):
    python_agent = Agent(
        prompt_persona="You Are Expert Python developer who is expert in building fast api",
        role="Fast API Expert",
    )

    fastapi_task = Task(
        name="fats api converter",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=python_agent,
        log_output=True,
        instructions=f"""Your Are an Expert Python Developer.Your task is to convert given code into Fast API.
        Follow below instructions:
        1/ NLP check:
        Compile this code
        If error:
            resolve error
            return resolved code
        else:
            return entered code
            
        convert code into fast api
        2/ Do not write anything apart from code
        Code: {code_snippet}
        
        """,
    )

    output = LinearSyncPipeline(
        name="Generate FastAPI",
        completion_message="FastAPI Converted!",
        tasks=[
            fastapi_task
        ],
    ).run()
    return output[0]['task_output']


code = st.text_area("Enter Code", height=300)

if st.button("Convert"):
    solution = lyrics_writer(code)
    st.markdown(solution)
