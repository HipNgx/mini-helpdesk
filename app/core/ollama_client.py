from urllib.parse import urlparse
from ollama import Client
from core.config import settings

class OllamaLLM:
    def __init__(self):
        self.cloud = urlparse(settings.ollama_host).hostname == "ollama.com"
        headers = {"Authorization": f"Bearer {settings.ollama_api_key}"} if settings.ollama_api_key else {}
        self.client = Client(host=settings.ollama_host, headers=headers, timeout=60)

    def chat_stream(self, model, messages):
        for chunk in self.client.chat(model=model, messages=messages, stream=True):
            if chunk.message.content:
                yield chunk.message.content

    def chat_json(self, model, messages, schema):
        kwargs = {} if self.cloud else {"format": schema}
        response = self.client.chat(model=model, messages=messages, stream=False,
                                    options={"temperature": 0}, **kwargs)
        return response.message.content or ""
