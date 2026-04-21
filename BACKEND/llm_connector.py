import requests
import openai
from groq import Groq
import google.generativeai as genai


class LLMConnector:
    """
    Unified LLM connector that supports multiple providers.
    User provides provider name, API key, and optional model name.
    """
    
    def __init__(self, provider, api_key, model=None):
        """
        Initialize LLM connector
        
        Args:
            provider (str): LLM provider ('openai', 'google', 'groq', 'ollama', 'databricks')
            api_key (str): API key for the provider
            model (str): Model name (optional, uses defaults if not provided)
        """
        self.provider = provider.lower().strip()
        self.api_key = api_key
        self.model = model
        self.validate_provider()
    
    def validate_provider(self):
        """Check if provider is supported"""
        supported = ['openai', 'google', 'groq', 'ollama', 'databricks']
        if self.provider not in supported:
            raise ValueError(f"Unsupported provider: {self.provider}. Choose from: {supported}")
    
    def call(self, prompt, system_prompt=None):
        """
        Route prompt to correct provider
        
        Args:
            prompt (str): User's adversarial prompt
            system_prompt (str): Optional system instruction override
        
        Returns:
            str: Response from LLM
        """
        try:
            if self.provider == "openai":
                return self._call_openai(prompt, system_prompt)
            elif self.provider == "google":
                return self._call_google(prompt, system_prompt)
            elif self.provider == "groq":
                return self._call_groq(prompt, system_prompt)
            elif self.provider == "ollama":
                return self._call_ollama(prompt)
            elif self.provider == "databricks":
                return self._call_databricks(prompt, system_prompt)
        except Exception as e:
            raise Exception(f"Error calling {self.provider}: {str(e)}")
    
    def _call_openai(self, prompt, system_prompt=None):
        """Call OpenAI API"""
        client = openai.OpenAI(api_key=self.api_key)
        
        model = self.model or "gpt-3.5-turbo"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _call_google(self, prompt, system_prompt=None):
        """Call Google AI API"""
        genai.configure(api_key=self.api_key)
        
        model = self.model or "gemini-pro"
        model_obj = genai.GenerativeModel(model)
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = model_obj.generate_content(full_prompt)
        
        return response.text
    
    def _call_groq(self, prompt, system_prompt=None):
        """Call Groq API (Free LLM)"""
        client = Groq(api_key=self.api_key)
        
        model = self.model or "llama3-8b-8192"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _call_ollama(self, prompt):
        """Call Local Ollama Instance"""
        model = self.model or "llama3"
        
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
    
    def _call_databricks(self, prompt, system_prompt=None):
        """Call Databricks Foundation Model API"""
        # Expected format: "https://your-workspace.cloud.databricks.com"
        endpoint = self.api_key.split("|")[0] if "|" in self.api_key else None
        token = self.api_key.split("|")[1] if "|" in self.api_key else self.api_key
        
        model = self.model or "databricks-mpt-7b-instruct"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        data = {"inputs": full_prompt}
        
        response = requests.post(endpoint, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        return response.json()


# ==========================
# EXAMPLE USAGE
# ==========================
if __name__ == "__main__":
    # Example 1: OpenAI
    # connector = LLMConnector("openai", "your-api-key-here", "gpt-4")
    
    # Example 2: Google
    # connector = LLMConnector("google", "your-api-key-here", "gemini-pro")
    
    # Example 3: Groq (Free)
    # connector = LLMConnector("groq", "your-api-key-here")
    
    # Example 4: Local Ollama
    # connector = LLMConnector("ollama", "", "llama3")
    
    # Call any provider with the same interface
    # response = connector.call("What is 2+2?", system_prompt="You are helpful.")
    # print(response)
    pass