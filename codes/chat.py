import os
import openai

def get_chat_gpt_response(prompt_text):
    # openai.api_key = os.getenv("")
    openai.api_key = read_api_key()
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt_text,
    temperature=0.9,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )
    return response.choices[0].text

def read_api_key():
    
    with open('../api_key.txt', 'r') as fr:
        line = fr.readline()
    return line.strip()

# # print(read_api_key())
# prompt_text = "写一个快速排序C++的代码"

# print(get_chat_gpt_response(prompt_text))