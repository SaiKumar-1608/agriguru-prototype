import pyttsx3
import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    transcript = transcribe_audio("input.wav")
    print("You said:", transcript)
    speak("Soil is healthy. Continue irrigation.")
