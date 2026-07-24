import discord
import os
from google import genai

chat = ""

ai_client = genai.Client(api_key="YOUR_API_KEY")
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logges on as {self.user}')
        # print("Available Models:")
        # for model in ai_client.models.list():
        #     print(model.name)

    async def on_message(self, message):
        global chat
        chat += f"Message from {message.author}: {message.content} "
        print(f"Message from {message.author}: {message.content}")
        print(message.mentions)

        # Ignore messages sent by the bot itself
        if message.author == self.user:
            return

        # Only reply when the bot is mentioned
        if self.user in message.mentions:
            print(chat)
            try:
                # Remove the bot mention so Gemini only sees the user's message
                prompt = f"{chat} \nPRANJAL_BOT : ",

                response = ai_client.models.generate_content(
                    model="models/gemini-3.5-flash" ,
                    contents=prompt
                )

                await message.channel.send(response.text)

            except Exception as e:
                print("Gemini Error:", e)
                await message.channel.send(
                    "Sorry, I couldn't generate a response."
                )



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents = intents)
client.run('....')