import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_API_KEY"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
# SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses,
#  so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner.
#    Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
# """


@textbase.chatbot("Personalized chatbot 1901")
def on_message(message_history: List[Message], state: dict = None):
    SYSTEM_PROMPT = ["You are a Joke Generator", "You are a Song Recommender"]
    joke_list = [
        'What is the occasion for the joke (party, festival, chit chat with friends, etc.)?',
        'What is your current mood (happy, sad, frustrated, etc.)?',
        'What is the tone of the joke that you are looking for (funny, angry, sad, suspense, etc.)?',
        'What is your favorite joke about a specific subject (e.g., animals, food, work, etc.)?'
    ]
    music_list = [
        'What genre of music do you enjoy the most? (pop, classical, rock, etc.)',
        'Do you play any musical instruments? (guitar, piano, drums, etc.)',
        'What song always gets stuck in your head when you hear it? (e.g., "Happy" by Pharrell Williams, "Bohemian Rhapsody" by Queen, "Imagine" by John Lennon, etc.)',
        'What\'s the last song you listened to?',
        'Do you prefer private albums or movie songs?',
        'What\'s your current mood? (happy, sad, frustrated, etc.)',
        'Purpose of your music? (e.g., to relax, to dance, to think)',
        'Do you prefer listening to music alone or with friends?',
    ]
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    if state is None or "counter" not in state:
        state = {"counter": 0, "service": 0, "question_counter": 0, "in_menu": True}
    else:
        state["counter"] += 1

    if state["in_menu"]:
        if state["counter"] == 0:
            bot_response = f"""
            Welcome to Your Entertainment Personalized Chatbot-1901!!
            Here are some of the things I can do for you:                                                     
            I am still under development, but I am learning new things every day. I am excited to help you with your entertainment needs. How can I assist you today?
            Please type the number corresponding to your preferred option and press Enter:
            1. For Joke Generator
            2. For Music Recommender
            """
            state["in_menu"] = False
    else:
        # Handle the personalized assistant state here
        user_input = message_history[-1].content.lower()
        if state["service"] == 0:
            # Choose the service based on user input
            state["service"] = int(user_input)

        if "exit" in user_input:
            # If the user wants to exit, return to the main menu
            bot_response = f"""
            Use Another Service, the preferred options and press Enter:
            1. For Joke Generator
            2. For Music Recommender,
            But I am excited to help you with your entertainment preferences.How can I assist you today?
            """
            state = {"counter": 0, "service": 0, "question_counter": 0, "in_menu": False}
            # Reset the state to go back to the menu
        elif state["service"] == 1:
            if state["question_counter"] < len(joke_list):
                # Provide the next question from the joke list
                bot_response = joke_list[state["question_counter"]]
                state["question_counter"] += 1
            else:
                # If all joke questions are asked, use GPT-3.5 Turbo to generate the joke
                bot_response = models.OpenAI.generate(
                    system_prompt=SYSTEM_PROMPT[0] + "Please provide an emoji based on the mood of the joke. 😄🤔😂",
                    message_history=message_history,
                    model="gpt-3.5-turbo",
                )
        elif state["service"] == 2:
                if state["question_counter"] < len(music_list):
                    # Provide the next question from the music list
                    bot_response = music_list[state["question_counter"]]
                    state["question_counter"] += 1
                else:
                    # If all music questions are asked, use GPT-3.5 Turbo to recommend music
                    bot_response = models.OpenAI.generate(
                        system_prompt=SYSTEM_PROMPT[1]+"give emoji wherever required and 👭 or 🚶‍♂️",
                        message_history=message_history,
                        model="gpt-3.5-turbo",
                    )
        else:
            # If the user doesn't want music, return to the main menu
            bot_response = f"""
            You selected an invalid service,
            But I am excited to help you with your entertainment preferences. How can I assist you today?
            Please type the number corresponding to your preferred option and press Enter:
            1. For Joke Generator
            2. For Music Recommender
            """
            state["in_menu"] = False

    return bot_response, state
