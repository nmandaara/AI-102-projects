from dotenv import load_dotenv
from datetime import datetime
import os
import azure.cognitiveservices.speech as speechsdk
from playsound import playsound
# Import namespaces


def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        speech_config = speechsdk.SpeechConfig(ai_key,ai_region)

        # Get spoken input
        command = TranscribeCommand(speech_config)
        if command.lower() == 'what time is it?':
            TellTime(speech_config)

    except Exception as ex:
        print(ex)

def TranscribeCommand(speech_config):
    command = ''

    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = current_dir + '/time.wav'
    playsound(audioFile)
    audio_config = speechsdk.AudioConfig(filename=audioFile)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speechsdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speechsdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command


def TellTime(speech_config):
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config)

    # Synthesize spoken output
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()