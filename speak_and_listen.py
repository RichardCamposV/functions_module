import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 120)
engine.setProperty("voice", "spanish")

r = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def hear_me():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="en-US")
            print("He enetendido: {}".format(text))
            return text
        except sr.UnknownValueError:
            return


if __name__ == "__main__":
    speak("Probando si funciona todo")
    print(hear_me())
