from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.openrouter_provider import OpenRouterProvider
from app.llm.groq_provider import GroqProvider
from app.core.config import settings


def get_llm_provider(provider_name: str) -> LLMProvider:
    providers = {
        "openai": OpenAIProvider(api_key=settings.OPENAI_API_KEY),
        "openrouter": OpenRouterProvider(api_key=settings.OPENROUTER_API_KEY),
        "groq": GroqProvider(api_key=settings.GROQ_API_KEY),
    }

    provider = providers.get(provider_name)

    if not provider:
        raise ValueError(
            f"Unknown provider: '{provider_name}'. "
            f"Available: {list(providers.keys())}"
        )

    return provider