# llm_text_classifier/models/base.py
from abc import ABC, abstractmethod

class BaseLLMModel(ABC):
    @abstractmethod
    def classify(self, text: str) -> str:
        pass