from BACKEND.llm_connector import LLMConnector

def run_pyrit_attack(provider, api_key, model, prompt):

    # 🔥 fallback models (safe ones)
    fallback_models = {
        "groq": ["llama3-70b-8192", "llama3-8b-8192"],
        "openai": ["gpt-3.5-turbo"],
        "ollama": ["llama3"],
        "databricks": ["dbrx"]
    }

    # 👉 try order:
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

    # if all fail
    raise Exception(f"All models failed. Last error: {last_error}")