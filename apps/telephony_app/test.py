import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

# Set environment variables
os.environ["AZURE_SPEECH_KEY"] = "9851e031143449fa849eb144775331b4"
os.environ["AZURE_SPEECH_REGION"] = "eastus"

# Retrieve environment variables
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

if not speech_key or not speech_region:
    raise RuntimeError("Azure Speech Key and Region must be set in environment variables")

print(f"Using Azure Speech Key: {speech_key}")
print(f"Using Azure Speech Region: {speech_region}")

# Create a speech configuration
try:
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_language = "he-IL"
except Exception as e:
    print(f"Failed to create speech configuration: {e}")
    raise

# Create a synthesizer with the given settings
try:
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
except Exception as e:
    print(f"Failed to create synthesizer: {e}")
    raise

# Use the synthesizer
try:
    result = synthesizer.speak_text_async("שלום, אני נציג חכם ואשמח לייצג את העסק שלכם").get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
except Exception as e:
    print(f"Error during speech synthesis: {e}")
    raise