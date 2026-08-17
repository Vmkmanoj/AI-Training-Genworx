from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class ModelResponse:
    content: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency: float


@dataclass
class StreamChunk:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class ModelInterface(ABC):

    @abstractmethod
    def generate(
        self,
        messages: Any,
        temperature: float = 0.1,
    ) -> ModelResponse:
        pass
