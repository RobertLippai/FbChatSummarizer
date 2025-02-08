import os

from openai import OpenAI

from user_data_manager import user_data_manager


client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url= os.getenv("AI_ENDPOINT_URL")
)

model_name = os.getenv("AI_MODEL_NAME")

async def summarize_conversation(messages):
    content = ""
    for message in messages:
        name = user_data_manager.get_user_name_cache(message.author)
        content += f"{name}: {message.text}\n"

    prompt = f"""
    Please generate a summary of the following conversation.
    The summary should be clear, concise, and capture the key points, making it easy for someone who hasn't read the conversation to quickly understand the important topics and participate. 

    Important: The summary **must** be in the **same language** as the conversation. Do not translate or change the language.
    
    Conversation: {content}
    """

    print(content)

    formatted_messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Please summarize the conversation above."}
    ]
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=formatted_messages
        )
        generated_summary = response.choices[0].message.content
        print(generated_summary)

        return generated_summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None
