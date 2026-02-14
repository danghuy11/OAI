#check credit at
#https://platform.openai.com/settings/organization/billing/overview

import requests
import json

# init client using OPENAI_API_KEY env var
with open('api-key.txt','r') as f:
    OPENAI_API_KEY = f.read()

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

def chatgpt (question):
    data = {
        "model": "gpt-3.5-turbo",   # or a newer model you have access to
        "messages": [
            {
                "role": "system", 
                "content": (
                    "Ty si asistent. Užívateľ ukazuje objekt a pomenúva ho. "
                    "Ak pýta sa či sa ukazovaný objekt nazýva tak a tak, odpovedz jedným slovom - názvom objektu. "
                    "Inak vráť prázdny reťazec."
                )
            },
            {
                "role": "user",
                "content": "Je toto kačička?"
            },
            {
                "role": "assistant",
                "content": "kačička"
            },
            {
                "role": "user",
                "content": "Koľko je hodín?"
            },
            {
                "role": "assistant",
                "content": ""
            },        
            {
                "role": "user", 
                "content": question
            }
        ],
        "max_tokens": 100,
        "temperature": 0.0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        return ""
        
if __name__ == "__main__":
    name = chatgpt("Je toto tiež psíček, do čerta?")
    print(name)
