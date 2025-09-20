import xlwings as xw
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="your_api_key_here")

def chatgpt(prompt):
    """Send prompt to ChatGPT and return the response"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4.1-mini" if you prefer
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@xw.func
def ask_gpt(prompt):
    """Excel UDF: =ask_gpt("Write a haiku about Excel")"""
    try:
        return chatgpt(prompt)
    except Exception as e:
        return f"Error: {e}"
