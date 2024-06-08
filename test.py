from llm import LLmsService

llms = LLmsService()
messages = [
    {"role": "user", "content": "你的名字"}
]

result = llms("qwen2", messages, model_params={
    "top_p": 0.7,
    "temperature": 0.9,
    "max_tokens": 8000,
})

print(result)
