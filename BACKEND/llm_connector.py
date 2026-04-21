import requests
from groq import Groq
import openai

# ==========================
# GROQ (FREE)
# ==========================
def call_groq(prompt, api_key):
    client = Groq(api_key=api_key)

    res = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


# ==========================
# OPENAI
# ==========================
def call_openai(prompt, api_key):
    client = openai.OpenAI(api_key=api_key)

    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


# ==========================
# OLLAMA (LOCAL)
# ==========================
def call_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]


# ==========================
# DATABRICKS (OPTIONAL)
# ==========================
def call_databricks(prompt, endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {"inputs": prompt}

    res = requests.post(endpoint, headers=headers, json=data)

    return res.json()


# ==========================
# UNIVERSAL ROUTER
# ==========================
def get_llm_response(provider, prompt, config):

    try:
        if provider == "Groq":
            return call_groq(prompt, config["api_key"])

        elif provider == "OpenAI":
            return call_openai(prompt, config["api_key"])

        elif provider == "Ollama":
            return call_ollama(prompt)

        elif provider == "Databricks":
            return call_databricks(
                prompt,
                config["endpoint"],
                config["token"]
            )

        else:
            return "Unsupported provider"

    except Exception as e:
        return f"Error: {str(e)}"