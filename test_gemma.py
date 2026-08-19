

from ollama import chat


response = chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": "Hello Gemma! Introduce yourself in one sentence."
        }
    ]
)


print(response["message"]["content"])