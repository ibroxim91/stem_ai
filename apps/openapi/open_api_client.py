from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPEN_API_KEY")

client = OpenAI(api_key=API_KEY)

def ask_openai(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
    )
    print()
    print(response.choices[0].message.content)
    print()
    return #response['choices'][0]['message']['content']


p = "Dasturlashni qaysi tildan boshlagan ma'qul?"

r = ask_openai(p)

print(r)