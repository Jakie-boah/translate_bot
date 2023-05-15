# -*- coding: utf-8 -*-
import openai
from config import openai_api_key
openai.api_key = openai_api_key


async def translate(lang, message):
    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=f"Translate into {lang} language:\n\n{message}\n\n",
        temperature=0.3,
        max_tokens=1000,
        top_p=1.0,

    )
    return response
#
# print(translate('EN', 'Привет'))