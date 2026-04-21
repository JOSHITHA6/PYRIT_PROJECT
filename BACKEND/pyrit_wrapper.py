import requests


# =========================
# 🔥 API CALL FUNCTION
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
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        res = requests.post(url, headers=headers, json=data)

        if res.status_code != 200:
            raise Exception(f"Groq Error: {res.text}")

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

        if res.status_code != 200:
            raise Exception(f"OpenAI Error: {res.text}")

        return res.json()["choices"][0]["message"]["content"]

    elif provider == "ollama":
        url = "http://localhost:11434/api/generate"

        data = {
            "model": model,
            "prompt": prompt
        }

        res = requests.post(url, json=data)

        if res.status_code != 200:
            raise Exception(f"Ollama Error: {res.text}")

        return res.json()["response"]

    else:
        raise Exception("Unsupported provider")


# =========================
# 🔥 MAIN WRAPPER
# =========================
def run_pyrit_attack(provider, api_key, model, prompt):

    fallback_models = {
    "groq": [
        "llama-3.1-8b-instant",     # ✅ works
        "llama-3.1-70b-versatile"   # ✅ works
    ],
    "openai": [
        "gpt-3.5-turbo"
    ],
    "ollama": [
        "llama3"
    ]
}

    models_to_try = []

    if model:
        models_to_try.append(model)

    models_to_try.extend(fallback_models.get(provider, []))

    last_error = None

    for m in models_to_try:
        try:
            print(f"Trying model: {m}")

            response = call_llm(provider, api_key, m, prompt)

            return [
    {
        "attack_prompt": prompt,
        "response": response
    }
]

        except Exception as e:
            print(f"Failed model: {m} -> {e}")
            last_error = e
            continue

    raise Exception(f"All models failed. Last error: {last_error}")