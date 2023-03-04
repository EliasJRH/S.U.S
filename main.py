import speech_recognition
import pyttsx3
import openai
import dotenv
from enum import Enum

speech_recognizer = speech_recognition.Recognizer()

tts_engine = pyttsx3.init() # object creation

openai.api_key = dotenv.dotenv_values()['OPEN_API_KEY']

State = Enum('State', ['PASSIVE_LISTENING', 'ACTIVE_LISTENING', 'SPEAKING'])

ACTIVATE_KEY = "hey there"

current_state = State.PASSIVE_LISTENING

current_speaking_text = ""

while True:
    print("Current state:", current_state.name)

    if current_state == State.PASSIVE_LISTENING or current_state == State.ACTIVE_LISTENING:
        try:
            with speech_recognition.Microphone() as mic:
                speech_recognizer.adjust_for_ambient_noise(mic)
                audio = speech_recognizer.listen(mic)

                user_prompt_text = speech_recognizer.recognize_google(audio)

                print("text:", user_prompt_text)
                if current_state == State.PASSIVE_LISTENING and user_prompt_text == ACTIVATE_KEY:
                    tts_engine.stop()
                    current_state = State.ACTIVE_LISTENING

                elif current_state == State.ACTIVE_LISTENING:
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{user_prompt_text}"}])
                    print(completion.choices[0].message.content)
                    current_speaking_text = completion.choices[0].message.content
                    current_state = State.SPEAKING
        
        except Exception as e:
            print("I couldn't recognize that, speak again")
            current_state = State.PASSIVE_LISTENING
    
    elif current_state == State.SPEAKING:
        tts_engine.say(current_speaking_text)
        tts_engine.runAndWait()
        current_speaking_text = ""
        current_state = State.PASSIVE_LISTENING
        