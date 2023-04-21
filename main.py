# Libraries required for basic operation
import speech_recognition
import openai
import dotenv
import threading

# Libraries required for spawning listening and GUI subprocesses
import os
import signal
from subprocess import Popen

from enum import Enum

from multiprocessing.connection import Client, Listener

ACTIVATE_KEY = "hey there"
SHUTDOWN_KEY = "hey shut down"

# Enums represent state of speaker
# PASSIVE_LISTENING - Speaker is listening for ACTIVATE_KEY in transcribed speech
# ACTIVE_LISTENING - Speaker is listening for next speech prompt to send to OpenAI API
# SPEAKER - Speaker spawns speaking subprocess and plays audio
State = Enum('State', ['PASSIVE_LISTENING', 'ACTIVE_LISTENING', 'SPEAKING']) 

def handle_updates():
	pass

def activate_speaker():
	pass

def main():
	speech_recognizer = speech_recognition.Recognizer() # Initialize speech recognizer

	openai.api_key = dotenv.dotenv_values()['OPEN_AI_API_KEY'] # Configure OpenAI API key

	# Initial state starts at passive listening
	current_state = State.PASSIVE_LISTENING

	current_speaking_text = "" # Text sent to text to speech process
	speaking_PID = None # Text to speech process ID

	# Addresses for bi-directional IPC
	window_address = ('localhost', 6000)
	main_address = ('localhost', 6001)

	# Set up listener on main application
	main_listener = Listener(main_address, authkey=b"%s" % dotenv.dotenv_values()['MAIN_LISTENER_KEY'].encode())

	# Spawn UI window
	window_PID = Popen(["venv/Scripts/python", "window.py", str(os.getpid())]).pid

	# Receive connection from window application
	window_to_main_conn = main_listener.accept()

	# Connect to listener on window application
	main_to_window_conn = Client(window_address, authkey=b"%b" % dotenv.dotenv_values()['WINDOW_LISTENER_KEY'].encode())


	while True:
		print("Current state:", current_state.name)

		# Obtain microphone audio data is state is passive listening or active listening
		if current_state == State.PASSIVE_LISTENING or current_state == State.ACTIVE_LISTENING:
			try:
				with speech_recognition.Microphone() as mic:
					speech_recognizer.adjust_for_ambient_noise(mic) # Establishes ambient noise level
					audio = speech_recognizer.listen(mic, phrase_time_limit=5)
					# print(audio.frame_data)
	
					user_prompt_text = speech_recognizer.recognize_google(audio)

					print("text:", user_prompt_text)

					# This if statement only executes if speech exception is not thrown from listen function
					# If audio is heard, kill current speaking process
					if current_state == State.PASSIVE_LISTENING:
						try:
							if speaking_PID: 
								os.kill(speaking_PID, signal.SIGTERM)
								speaking_PID = None
						except WindowsError as e:
							pass
						
						# Only switch to ACTIVE_LISTENING state if ACTIVATE_KEY is in the user prompt
						if ACTIVATE_KEY in user_prompt_text: 
							current_state = State.ACTIVE_LISTENING
							main_to_window_conn.send("active")
						elif SHUTDOWN_KEY in user_prompt_text:
							try:
								os.kill(window_PID, signal.SIGTERM)
								return
							except WindowsError as e:
								pass

					# If state is ACTIVE_LISTENING, send next prompt to OpenAI API, then switch to speaking state
					elif current_state == State.ACTIVE_LISTENING:
						completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": f"{user_prompt_text}"}])
						print(completion.choices[0].message.content)
						current_speaking_text = completion.choices[0].message.content
						current_state = State.SPEAKING

			except Exception as e:
				print("I couldn't recognize that, speak again")
				current_state = State.PASSIVE_LISTENING
		
		# If state is SPEAKING, spawn speaking subprocess, 
		elif current_state == State.SPEAKING:
			print("creating tts subprocess...")
			speaking_proc = Popen(["venv/Scripts/python", "speak.py", current_speaking_text])
			speaking_PID = speaking_proc.pid
			current_speaking_text = ""
			current_state = State.PASSIVE_LISTENING

if __name__ == "__main__":
	main()