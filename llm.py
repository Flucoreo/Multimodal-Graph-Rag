from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="dummy-key"
)

def get_chat_completion(prompt, model="google/gemma-3-12b"):

    user_message = {"role": "user", "content": prompt}

    # Calling the ChatCompletion API
    res = client.chat.completions.create(
       model=model,
       messages=[user_message],
   )

    # Returning the extracted response
    return res.choices[0].message.content

response = get_chat_completion("What is the tallest building in the world?!")

print(response)
