import os
import time
import pandas as pd
from mistralai import Mistral
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import COL_IDEES,COL_DESCRIPTION,COL_EXPOSE_SOMMAIRE
from sentence_transformers import SentenceTransformer, util


class Embedding:
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)

    
    def prompt_encode(self,prompt):
        self.prompt_encode = self.model.encode(prompt)
    

    def classify(self, text) -> str:

        if util.cos_sim(self.prompt_encode, self.model.encode(text)) > 0.80:
            return "oui"
        else: 
            return "non"



