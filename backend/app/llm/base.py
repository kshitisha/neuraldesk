from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator
@dataclass
class ChatMessage:
    role: str
    content: str
@dataclass
class LLMConfig:
    model: str
    temperature: float
    system_prompt: str
    provider: str
@dataclass
class ChatResponse:
    content: str
    input_tokens: int
    output_tokens: int
    model: str
class LLMProvider(ABC):
    """abstract interface — every provider must implement these three methods.
    business logic only ever talks to this interface, never to a
    concrete provider directly. Swapping OpenAI for anything else
    means implementing this class and updating the factory. Nothing else changes.
    """

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        config: LLMConfig,
    ) -> ChatResponse:
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[ChatMessage],
        config: LLMConfig,
    ) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        ...