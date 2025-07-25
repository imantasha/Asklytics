
#  Asklytics – GenAI-Powered Data Insights with Groq + LLaMA 3

**Asklytics** lets you upload a CSV and ask data questions in plain English. It uses **Groq’s ultra-fast LLaMA 3** to generate and run `pandas` + `matplotlib` code, giving instant answers and visualizations — no coding needed.

---

##  Features

- Upload your own CSV file
- Ask natural language questions like:
  - *"What is the average profit by region?"*
  - *"Show a chart of monthly sales trends"*
- Get:
  -  Python code (auto-generated)
  -  Result tables or charts (auto-executed)

---

##  Powered By

-  LLaMA 3 (70B) via [Groq API](https://console.groq.com/)
-  Gradio for the UI
-  Pandas + Matplotlib for analysis/visualization

---

##  Installation

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/asklytics.git
cd asklytics
install Dependencies
pip install -r requirements.txt
Set up your .env file:

Create a .env file in the root directory with:

GROQ_API_KEY=your_actual_groq_api_key_here

 Run the App
python insightbot_groq.py
