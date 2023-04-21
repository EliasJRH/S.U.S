# The S.U.S
The Smart Ubiquitous Speaker is a smart speaker that leverages GPT3.5 to complete audio prompts, similar to a Google Home or Amazon Alexa. This was also my submission for Hack The Hill '23. Enjoy poking around the codebase and finding the weird and janky solutions I had to come up with within 48 hours :D.

# Setup/Installation
1. Clone the repository

`git clone https://github.com/EliasJRH/S.U.S.git`

2. Change directory into the repository

`cd S.U.S`

3. Setup a virtual environment

`python3 -m venv venv`

4. Activate the virtual environment

If on Windows:
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\activate
```

If on Mac/Linux:
```bash
source venv/bin/activate
```

5. Install the requirements

`pip install -r requirements.txt`

6. Run the program

`python main.py`

*Note: In order to run the program, you will need to have a GPT3 API key. You can get one [here](https://beta.openai.com/). Once you have the key, create a file called `.env` in the root directory of the project and add the following line:

`OPENAI_API_KEY=YOUR_API_KEY`

This program requires access to a microphone.