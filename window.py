import PySimpleGUI as sg
import os, sys, signal

IMPOSTOR_FILE_PATH = "media/Impostor.png"
TWERK_FILE_PATH = "media/among-us-twerk.gif"

layout = [ [sg.Text("Smart Ubiquitous Speaker", key='-bold-', justification='center')],[sg.Image(IMPOSTOR_FILE_PATH, key="-image-")] ]
window = sg.Window('Window Title', layout)

def handle_sigusr1():
  window["-image-"].update(IMPOSTOR_FILE_PATH)

def handle_sigusr2():
  window["-image-"].update(TWERK_FILE_PATH)

def main():
  ppid = str(sys.argv[1])
  print(f"This process id: {os.getpid()}")
  print(f"Parent process id: {ppid}")

  sg.theme('DarkAmber')   # Add a touch of color
  # All the stuff inside your window.

  # Event Loop to process "events" and get the "values" of the inputs
  while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
          break
      print('You entered ', values[0])

  window.close()

signal.signal(signal.SIGUSR1, handle_sigusr1)
signal.signal(signal.SIGUSR2, handle_sigusr2)
main()