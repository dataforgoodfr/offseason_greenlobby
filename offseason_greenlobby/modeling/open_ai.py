import os
import time
import pandas as pd
import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import COL_IDEES,COL_DESCRIPTION,COL_EXPOSE_SOMMAIRE


class OpenAIModel:
    def __init__(self, model_name):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.model_name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def classify(self, prompt: str, temperature) -> str:
        try:
            with openai.OpenAI(api_key=self.api_key) as openai_model:
                response = openai_model.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ API Error {e}")
        return ["échec API"]




    def classify_batches(self, df: pd.DataFrame, batch_size: int, prompt_template: str, delay: float, temperature) -> list:
        content_ret = []
        for start in range(0, len(df), batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]
            for _, row in batch.iterrows():
                try:
                    prompt = prompt_template.format(
                        IDEE=row[COL_IDEES],
                        DESCRIPTION=row[COL_DESCRIPTION],
                        EXPOSE_SOMMAIRE=row[COL_EXPOSE_SOMMAIRE],
                    )
                    response = self.classify(prompt,temperature)

                    if batch.shape[0] == len(response):
                        print(f"✅ {len(response)} results found out of {batch.shape[0]}")
                        print("Response:",response)

                        content_ret.extend(response)
                    else:
                        print(f"❌ {len(response)} results found out of {batch.shape[0]}")
                        print("Response:",response)

                        content_ret.extend(["échec API"] * df.shape[0])
                except Exception as e:
                    print(f"Erreur API: {e}")
                    return content_ret.extend(["échec API"] * df.shape[0])

        print(f"✅ {len(content_ret)} results found out of {len(df)}")
        return content_ret

