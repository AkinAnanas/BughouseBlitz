import threading
import speech_recognition as sr


class CommandListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.thread = threading.Thread(target=self.listen, args=(1,), daemon=True)
        self.listening = False
        self.commands = []

    def listen(self, *args):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google_cloud(audio)
                    text = text.lower()
                    self.process_data(text)
            except sr.UnknownValueError:
                self.recognizer = sr.Recognizer()

    def process_data(self, text):
        pass

    def start(self):
        self.listening = True
        self.thread.start()

    def stop(self):
        self.listening = False
