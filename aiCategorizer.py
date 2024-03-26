from openai import OpenAI
import time
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SYSTEM_ROLE = \
    "You will be provided a code change description. Indicate if this change is evolution or maintenance."
    # "You are a helpful assistant."
    # "You are a researcher that is trying to learn how regex engine repositories change over time and how they shift between evolution mode and maintenance mode"
USER_PROMPT = \
    "92. Implement PCRE2_INFO_HASBACKSLASHC."
    # "94. Support offset_limit in JIT." # Should reply with 'Evolution'
    # "Hello!"
    # "Can you take a look at the re2 regex engine (https://github.com/google/re2) and categorize it's releases into evolution or maintenon mode"

# Enter your api key here
client = OpenAI()

completion = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="ft:gpt-3.5-turbo-1106:personal:changelog-pcre2:95whKLu9",
    messages=[
        {"role": "system", "content": SYSTEM_ROLE},
        {"role": "user", "content": USER_PROMPT}
    ]
)

print(completion.choices[0].message)