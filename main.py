# Libraries required for basic operation
import speech_recognition
import openai
import dotenv

# Libraries required for spawning listening and GUI subprocesses
import os
import signal
from subprocess import Popen

from enum import Enum

ACTIVATE_KEY = "hey there"
STOP_KEY = "hey stop"
def main():
    speech_recognizer = speech_recognition.Recognizer() # Initialize speech recognizer

    openai.api_key = dotenv.dotenv_values()['OPEN_API_KEY'] # Configure OpenAI API key

    # Enums handling state of speaker
    # PASSIVE_LISTENING - Speaker is listening for ACTIVATE_KEY in transcribed speech
    # ACTIVE_LISTENING - Speaker is listening for next speech prompt to send to OpenAI API
    # SPEAKER - Speaker spawns speak subprocess and plays audio
    State = Enum('State', ['PASSIVE_LISTENING', 'ACTIVE_LISTENING', 'SPEAKING']) 

    # Initial state starts at passive listening
    current_state = State.PASSIVE_LISTENING

    current_speaking_text = "" # Text sent to text to speech process
    speaking_PID = None # Text to speech process ID

    # Spawn UI window
    window_PID = Popen(["Scripts/python", "window.py", str(os.getpid())]).pid
    print(f"Window process id {window_PID}")

    while True:
        print("Current state:", current_state.name)

        # Obtain microphone audio data is state is passive listening or active listening
        if current_state == State.PASSIVE_LISTENING or current_state == State.ACTIVE_LISTENING:
            try:
                with speech_recognition.Microphone() as mic:
                    speech_recognizer.adjust_for_ambient_noise(mic) # Establishes ambient noise level
                    audio = speech_recognizer.listen(mic)
    
                    user_prompt_text = speech_recognizer.recognize_google(audio)

                    print("text:", user_prompt_text)

                    # If ACTIVATE_KEY is heard, kill any speaking process and switch to ACTIVE_LISTENING state 
                    if current_state == State.PASSIVE_LISTENING and ACTIVATE_KEY in user_prompt_text:
                        if speaking_PID: os.kill(speaking_PID, signal.SIGTERM)
                        current_state = State.ACTIVE_LISTENING

                    # If STOP_KEY is heard, kill any speaking process, state remains PASSIVE_LISTENING
                    elif current_state == State.PASSIVE_LISTENING and STOP_KEY in user_prompt_text:
                        if speaking_PID: os.kill(speaking_PID, signal.SIGTERM)

                    # If state is ACTIVE_LISTENING, send next prompt to OpenAI API, then switch to speaking state
                    elif current_state == State.ACTIVE_LISTENING:
                        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{user_prompt_text}"}])
                        print(completion.choices[0].message.content)
                        current_speaking_text = completion.choices[0].message.content
                        current_state = State.SPEAKING

            
            except Exception as e:
                print("I couldn't recognize that, speak again")
                current_state = State.PASSIVE_LISTENING
        
        # If state is SPEAKING, spawn speaking subprocess, 
        elif current_state == State.SPEAKING:
            print("creating subprocess...")
            speaking_proc = Popen(["Scripts/python", "speak.py", current_speaking_text])
            speaking_PID = speaking_proc.pid
            # speaking_proc.send_signal(signal.SIGUSR2)
            print(speaking_PID)
            current_speaking_text = ""
            current_state = State.PASSIVE_LISTENING

if __name__ == "__main__":
    main()