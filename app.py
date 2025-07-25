import os
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import openai

# Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Configure OpenAI client to point to Groq API
openai.api_key = groq_api_key
openai.api_base = "https://api.groq.com/openai/v1"
model = "llama3-70b-8192"

# Function to get code from Groq
def ask_with_groq(df, question):
    prompt = f"""
You are a helpful data analyst. Given the following DataFrame (first 10 rows):

{df.head(10).to_string(index=False)}

Write Python pandas code to answer this question:
"{question}"

Guidelines:
- Assign your final result to a variable named `result`
- If a chart is needed, assign the figure to `fig` using matplotlib/seaborn
- Do not print or explain anything, return only code
"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("❌ Groq API ERROR:", e)
        return None

# Function to run code and display results
def handle_query(file, question):
    try:
        df = pd.read_csv(file.name)
    except Exception as e:
        return f"❌ Error loading CSV: {e}", None

    code = ask_with_groq(df, question)

    if code is None:
        return "❌ Error: Could not generate code from Groq API.", None

    # ✅ Remove markdown formatting if Groq includes ```python or ```
    code = code.replace("```python", "").replace("```", "").strip()

    local_vars = {"df": df, "plt": plt}
    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", "✅ Code executed, but `result` not defined.")
        fig = local_vars.get("fig", None)
    except Exception as e:
        result = f"❌ Error executing code: {e}"
        fig = None

    output_text = f"🔍 Question: {question}\n\n📜 Generated Code:\n```python\n{code}\n```\n\n📊 Result:\n{result}"
    return output_text, fig

# Launch Gradio app
gr.Interface(
    fn=handle_query,
    inputs=[
        gr.File(label="Upload your CSV file"),
        gr.Textbox(label="Ask a question", placeholder="e.g. What is the average sales per region?")
    ],
    outputs=[
        gr.Textbox(label="Answer & Code", lines=12),
        gr.Plot(label="Chart (if any)")
    ],
    title="📊 InsightBot (Powered by Groq + LLaMA 3)",
    description="Upload a CSV and ask data questions in plain English. The app will analyze and visualize using LLaMA 3 via Groq API."
).launch()
