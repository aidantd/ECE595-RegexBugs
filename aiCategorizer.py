from openai import OpenAI
import time

# Enter your api key here
client = OpenAI(api_key="")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a researcher that is trying to learn how regex engine repositories change over time and how they shift between evolution mode and maintenance mode"},
        {"role": "user", "content": "Can you take a look at the re2 regex engine (https://github.com/google/re2) and categorize it's releases into evolution or maintenon mode"}
    ]
)

print(completion.choices[0].message)