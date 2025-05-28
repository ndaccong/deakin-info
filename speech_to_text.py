import azure.cognitiveservices.speech as speechsdk


def voice_recognize():
    SPEECH_KEY = ""
    ENDPOINT = ""
    
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, endpoint=ENDPOINT)
    speech_config.speech_recognition_language="en-US"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)    
    
    is_reconized = False
    
    # Start recognition
    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        is_reconized = True
        print(f"Recognized: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
    
    return is_reconized, result.text
        
if __name__ == '__main__':
    voice_recognize()