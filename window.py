import PySimpleGUI as sg
import os, sys, signal
import dotenv
import threading
from multiprocessing.connection import Client, Listener

# REFACTOR THIS FILE SO THAT ALL INSTRUCTIONS STAY IN FUNCTIONS
# MAIN SHOULD CONTAIN ALL OF THIS CODE EXCEPT FOR CONSTANTS
# THEN PASS IN APPROPRIATE ARGUMENTS WHEN CREATING THREADS

PASSIVE_LISTENING_ICON = "media/passive_listening.png"
ACTIVE_LISTENING_ICON = "media/active_listening.png"
TWERK_FILE_PATH = "media/among-us-twerk.gif"

def handle_updates(main_to_window_conn, window):
   while True:
      update = main_to_window_conn.recv()
      if update == "passive": window["-image-"].Update(PASSIVE_LISTENING_ICON)
      elif update == "active": window["-image-"].Update(ACTIVE_LISTENING_ICON)
      

def create_window(window, window_to_main_conn, ppid):
  sg.theme('DarkAmber')   # Add a touch of color
  # All the stuff inside your window.

  # Event Loop to process "events" and get the "values" of the inputs
  while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
          os.kill(ppid, signal.SIGTERM) # change to send signal to exit, need to close parent process before closing this process
          # window_to_main_conn.send("close")
          window.close()
          sys.exit()

def main():
  ppid = int(sys.argv[1])

  layout = [ [sg.Text("Smart Ubiquitous Speaker", key='-bold-', justification='center')],[sg.Image(PASSIVE_LISTENING_ICON, key="-image-")], [sg.Button('Quit')] ]
  window = sg.Window('S(mart) U(biquitous) S(peaker)', layout)

  window_address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
  main_address = ('localhost', 6001)

  window_to_main_conn = Client(main_address, authkey=b"%s" % dotenv.dotenv_values()['MAIN_LISTENER_KEY'].encode())

  window_listener = Listener(window_address, authkey=b"%b" % dotenv.dotenv_values()['WINDOW_LISTENER_KEY'].encode())
  main_to_window_conn = window_listener.accept()

  window_thread = threading.Thread(target=create_window, args=(window, window_to_main_conn, ppid,))
  update_thread = threading.Thread(target=handle_updates, args=(main_to_window_conn, window,))
  window_thread.start()
  update_thread.start()
  

main()