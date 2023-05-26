from typing import List

import openai

from django.conf import settings
from .models import ChatMessage

openai.api_key = settings.OPENAI_KEY
openai.proxy = settings.OPENAI_PROXY


def ask_with_completion(message: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=1000,
        temperature=0,
    )
    print(response)
    return response.choices[0].text.strip()


def ask_with_chat_completion(chat_history: List[ChatMessage], message):
    msgs = [
        {"role": "system", "content": "You are an AI chatbot"}
    ]
    for item in chat_history:
        msgs.append({"role": "user", "content": item.message})
        msgs.append({"role": "assistant", "content": item.response})
    msgs.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


