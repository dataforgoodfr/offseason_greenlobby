import os
from config import COL_IDEES,COL_DESCRIPTION,COL_EXPOSE_SOMMAIRE
import pandas as pd
import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

valid_responses = ["oui","non"]


class OpenAIModel:
    def __init__(self, model_name: str = "mistral-3b-latest"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.model_name = model_name

    """
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    """
    def classify(self, exposes_sommaires, instruct_system, temperature) -> str:
        # Instancie un client OpenAI
        try:
            with openai.OpenAI(api_key=self.api_key) as client:
                messages = [{"role": "system", "content": instruct_system}]
                for idx,message in enumerate(exposes_sommaires):
                    messages.append({
                        "role": "user",
                        "content": f"Amendement {idx+1} : {message}"
                    })
                response = client.chat.completions.create(
                    model=self.model_name,
                    n = len(messages)-1,
                    temperature= temperature,
                    messages = messages 
                )
                return [choice.message.content.strip().lower() for choice in response.choices]
        except Exception as e:
            print(f"❌ API Error : {e}")
        return ["échec API"] * len(exposes_sommaires)


    def classify_batches(self, df: pd.DataFrame, batch_size: int, prompt_template: str, delay: float, temperature) -> list:
        content_ret = []
        for start in range(0, len(df), batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]

            try:
                content = self.classify(
                    exposes_sommaires = [row[COL_EXPOSE_SOMMAIRE] for _, row in batch.iterrows()],
                    instruct_system = prompt_template.format(
                        IDEE=batch[COL_IDEES].values[0],
                        DESCRIPTION=batch[COL_DESCRIPTION].values[0]
                    ),temperature=temperature
                )
                if batch.shape[0] == len(content):
                    print(f"✅ {len(content)} results found out of {batch.shape[0]}")
                    content_ret.extend(content)
                else:
                    print(f"❌ {len(content)} results found out of {batch.shape[0]}")
                    content_ret.extend(["échec API"] * df.shape[0])
            
            except Exception as e:
                print(f"Erreur API: {e}")
                return content_ret.extend(["échec API"] * df.shape[0])

        print(f"✅ {len(content_ret)} results found out of {len(df)}")
        return content_ret

