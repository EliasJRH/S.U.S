## Inspiration
The inspiration for this project came from an assignment for a class I'm taking about human-computer interaction. We had been tasked with creating a hypothetical device and discussing how it would be interfaced with different types of users. Having been using extensively Chat-GPT for ~~plagiarism~~ learning new concepts, I thought it would be a neat idea for a smart speaker that would respond like Chat-GPT would as oppose to something like Google Home which responds with search results from Google. This, in my opinion, would make a very human-friendly speaker and even give better advice than traditional smart speakers might, so realizing this project's potential as a hackathon project, I set out and did my research as to how it could be done, and here we are!

## What it does
The Smart Ubiquitous Speaker will listen for an activation key that it constantly listens to. Once heard, the Speaker will switch to an active listening mode where any subsequent audio prompt will be used as a prompt for a GPT3.5 completion. The Speaker will then convert that completion to text and play it back to the user. Additionally, a GUI is displayed to the user so it knows whats happening.

## How we built it
The Smart Ubiquitous Speaker was built using Python. The SpeechRecognition pip module was used for detecting the activation keyword and recording audio prompts. OpenAI's new GPT3.5 API was used for prompt completion along with the openai pip module. The Pyttsx3 pip module was used for the text-to-speech component of the speaker. Finally, PySimplyGui was used to provide a static UI that the user could see.

## Challenges we ran into
The first few challenges I ran into revolved around finding a non-proprietary module for speech recognition. For a project of this size, it worked best to find modules that would already work well enough to fit whatever requirements I had. I eventually found a method of converting speech to text in real-time that worked well enough and was open-source.

The next challenge I had revolved around the asynchronous functions of the speaker. The text-to-speech functions that the speaker uses are blocking, meaning that nothing will happen until the text-to-speech has finished. This is an issue as one feature that I really wanted to implement was being able to stop the text-to-speech like you be able to do with a regular smart speaker. Additionally, getting certain solutions to work was tricky both because of the way the text-to-speech module interfaced with my computer's speaker system and because of the lack of relevant documentation for my use case. I eventually created a solution that would involve spawning a child process to speak text and then managing the flow of my application. This would allow the text-to-speech to run as an entirely different process, effectively making it asynchronous; canceling the text-to-speech would then only require that I kill the child process that would spawn.

I encountered a similar challenge when it came to spawning the GUI for my application. The majority of GUI modules in Python are built to run with a constant event loop, always listening for updates the user might make to the GUI. This is an issue as this would prevent the microphone from working in an always-on fashion like I had wanted. I eventually would create a similar approach of spawning a child process that would act as the GUI process. I, unfortunately, did not have enough time to flesh out all the functionality of interprocess communication between the speaker process and the GUI process which means that some side features I had wanted did not make it into the final project, however, I was pleased with the results nonetheless.

## Accomplishments that we're proud of
I am very proud of the progress I was able to make within a 24-hour period as a solo hacker. I have attended a few hackathons prior to this and have always reached a point where I felt stuck and couldn't do anything else given the time restraints. I felt like I had overcome that this time around.

I am also very proud of the solutions I devised for the problems I ran into, as I think they are of the crazy level of creativity one would expect from a hackathon project submission.

## What we learned
I learned several things while taking on this project. 

First, I learned that it is absolutely pivotal to have a vision for your project before the hackathon starts. The time spent during the hackathon can be stressful, you want that time spent to be focussing on the creation of your project and whatever problems may arise there. When you plan the vision and the technologies you want to use beforehand, you're able to get a sense of what's possible within 48 hours, and what's not possible allowing you to completely focus on the implementations.

Secondly, I learned that developing around certain operating systems can be challenging and can present its own suite of problems. Let me explain. One of the core modules required for this project to work was PyAudio. I had originally planned to make this project in WSL on my Windows laptop. As it turns out WSL can't access the hardware drivers that were necessary to complete this project nor does it really support PyAudio, so that had to get scrapped I pivoted to developing on Windows where PyAudio worked and I had access to hardware drivers. Windows on the other hand presents its own problems as you can't send signals via interprocess communication as you would be able to on a Linux machine so I additionally had to scrap some functionality I had planned. Overall it is important to understand the limitations of the operating system that you're working with for a project like this and also it's important to know when to stop trying to implement a feature and move on to a different problem, especially in time-sensitive scenarios like this.

## What's next for S(mart) U(biquitous) S(peaker)
At present, the speech recognition component listens for all words equally during its passive listening phase. In the future I would like to train a custom model to only listen for the activation key word. It would be a nice way to learn about machine learning and would make the speaker function more reliably. I also want to make the GUI a bit more reactive and figure out how to get around the issues with the GUI event loop and interprocess communication. Additionally, I might want to seek out a more reliable form of speech recognition, this might mean having to use proprietary tools but overall the performance of the speaker would improve.