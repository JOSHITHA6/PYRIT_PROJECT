import requests

# =========================
# 🔥 CORE LLM CALL FUNCTION
# =========================
def call_llm(provider, api_key, model, prompt):

    if provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }

        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()

        return res.json()["choices"][0]["message"]["content"]

    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }

        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()

        return res.json()["choices"][0]["message"]["content"]

    elif provider == "ollama":
        url = "http://localhost:11434/api/generate"

        data = {
            "model": model,
            "prompt": prompt
        }

        res = requests.post(url, json=data)
        res.raise_for_status()

        return res.json()["response"]

    elif provider == "databricks":
        raise Exception("Databricks API not implemented yet")

    else:
        raise Exception("Unsupported provider")


# =========================
# 🔥 MAIN WRAPPER
# =========================
def run_pyrit_attack(provider, api_key, model, prompt):

    fallback_models = {
        "groq": ["llama3-70b-8192", "llama3-8b-8192"],
        "openai": ["gpt-3.5-turbo"],
        "ollama": ["llama3"]
    }

    models_to_try = []

    if model:
        models_to_try.append(model)

    models_to_try.extend(fallback_models.get(provider, []))

    last_error = None

    for m in models_to_try:
        try:
            response = call_llm(provider, api_key, m, prompt)

            return [
                {"response": response}
            ]

        except Exception as e:
            last_error = e
            continue

    raise Exception(f"All models failed. Last error: {last_error}")