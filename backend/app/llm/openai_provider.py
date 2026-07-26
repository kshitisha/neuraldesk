from typing import AsyncIterator
from openai import AsyncOpenAI
from app.llm.base import LLMProvider, ChatMessage, LLMConfig, ChatResponse
from app.core.exceptions import LLMException
import logging
logger = logging.getLogger(__name__)
class OpenAIProvider(LLMProvider):
    """uses OpenAI Chat Completions API with async streaming.
    conversation history is managed in our own DB — we send the full
    history on every request which gives us full control over
    context windowing and costs."""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    def _build_messages(
        self, messages: list[ChatMessage], system_prompt: str
    ) -> list[dict]:
        result = []
        if system_prompt:
            result.append({"role": "system", "content": system_prompt})
        result.extend(
            {"role": msg.role, "content": msg.content} for msg in messages)
        return result

    async def chat(
        self,
        messages: list[ChatMessage],
        config: LLMConfig,
    ) -> ChatResponse:
        try:
            response = await self.client.chat.completions.create(
                model=config.model,
                messages=self._build_messages(messages, config.system_prompt),
                temperature=config.temperature,
            )
            return ChatResponse(
                content=response.choices[0].message.content or "",
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                model=response.model,
            )
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise LLMException(f"OpenAI error: {str(e)}")

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        config: LLMConfig,
    ) -> AsyncIterator[str]:
        try:
            stream = await self.client.chat.completions.create(
                model=config.model,
                messages=self._build_messages(messages, config.system_prompt),
                temperature=config.temperature,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise LLMException(f"OpenAI streaming error: {str(e)}")

    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False