import streamlit as st
import re
from transformers import pipeline
from ddgs import DDGS

st.set_page_config(
    page_title="Shanu AI",
    page_icon="🤖"
)

st.title("🤖 Shanu AI")
st.write("My Personal AI Assistant")

@st.cache_resource
def load_ai():
    return pipeline(
        "text-generation",
        model="HuggingFaceTB/SmolLM2-360M-Instruct"
    )

ai = load_ai()

def web_search(question):
    try:
        results = DDGS().text(question, max_results=3)

        if not results:
            return ""

        info = []
        for item in results:
            info.append(
                item.get("body", "")
            )

        return "\n".join(info)

    except:
        return ""

def calculate(question):
    try:
        expression = question
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")

        for word in ["कितना है", "कितना", "का उत्तर", "उत्तर", "है"]:
            expression = expression.replace(word, "")

        expression = expression.replace("?", "").strip()

        if re.fullmatch(r"[0-9+\-*/().\s]+", expression):
            return eval(
                expression,
                {"__builtins__": None},
                {}
            )
    except:
        pass

    return None

def ask_shanu(question):
    result = calculate(question)

    if result is not None:
        return f"उत्तर: {result} 🧮"

    web_info = web_search(question)

    prompt = f"""
You are Shanu AI, a helpful AI assistant.
Answer clearly and simply.
Use the information below when useful.

Internet information:
{web_info}

User question:
{question}

Answer:
"""

    try:
        output = ai(
            prompt,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.5
        )

        answer = output[0]["generated_text"]

        if "Answer:" in answer:
            answer = answer.split("Answer:", 1)[-1]

        return answer.strip()

    except Exception as e:
        return "माफ़ करना, अभी उत्तर देने में समस्या आ रही है। 🤖"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Shanu AI से कुछ पूछें...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    answer = ask_shanu(question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
