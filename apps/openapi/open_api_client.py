from openai import OpenAI
from dotenv import load_dotenv
import os
from .price_list import PRICE_LIST

load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=API_KEY)

class OpenAIHelper:
    
    @staticmethod
    def correct_prompt(prompt: str) -> str:
        if prompt and isinstance(prompt, str):
            prompt = prompt.strip().split(".")
            prompt = "\n".join(prompt)
        return prompt

    @staticmethod
    def calculate_openai_cost(prompt_tokens: int, completion_tokens: int, model: str = "gpt-4o") -> float:
        model_prices = PRICE_LIST.get(model, PRICE_LIST["gpt-4o"])
        prompt_price = model_prices["prompt"]
        completion_price = model_prices["completion"]
        return round(
            prompt_tokens * prompt_price + completion_tokens * completion_price, 6
        )

    @staticmethod
    def ask_openai(prompts: str, model: str = "gpt-4o") -> dict:
        messages = [{"role": "user", "content": prompts}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        print()
        print("response ", response)
        print()
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        content = response.choices[0].message.content
        formatted_content = OpenAIHelper.correct_prompt(content)

        cost = OpenAIHelper.calculate_openai_cost(prompt_tokens, completion_tokens, model)

        return {
            "content": formatted_content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost,
        }
 
