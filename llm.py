import asyncio
from openai import OpenAI
from typing import List, Optional

model_config = {
    "qwen2": {
        "api_key": "sk-hxodxgdwkhbyvzuwckftccatvknuholbaakrwlxtekmtwsvc",
        "base_url": "https://api.siliconflow.cn/v1",
        "name": "alibaba/Qwen2-72B-Instruct"
    },
    "doubao": {
        "api_key": "1393337e-4ea3-410c-9a28-e161a416e72b",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "name": "ep-20240607041327-6lxj8"
    },
    "glm-4": {
        "api_key": "b2a08be2c777db7eabd5e47bb981c454.qZ8rvUHqWMz4OiX6",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "name": "glm-4"
    },
}


class LLmsService:
    def __init__(self, model, model_params) -> None:
        self.model = model
        self.model_params = model_params
    

    def post_openai(self, messages):
        api_key = model_config[self.model]["api_key"]
        base_url = model_config[self.model]["base_url"]
        model_name = model_config[self.model]["name"]
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
           **self.model_params

        )
        return completion.choices[0].message.content

    def __call__(self, messages):
        return self.post_openai(messages)


if __name__ == '__main__':
    model_params={
        "top_p": 0.7,
        "temperature": 0.9,
        'max_tokens': 8000,
    }
    llm = LLmsService("glm-4", model_params=model_params)
    messages = [
        {"role": "user", "content": "who a u"}]
    res = llm(messages)
    print(res)