import openai

openai.api_base = "http://119.188.113.120:1180/v1"
openai.api_key = "none"
response = openai.ChatCompletion.create(
    model="/data/shared/Qwen/Qwen-Chat",
    messages=[
        {"role": "user", "content": "一斤棉花和一斤铁哪个重"}
    ],
    stream=False,
    temperature=0,
    stop=["<|endoftext|>", "<|im_end|>", "<|eot_id|>"]
    # You can add custom stop words here, e.g., stop=["Observation:"] for ReAct prompting.
)
print(response.choices[0].message.content)
