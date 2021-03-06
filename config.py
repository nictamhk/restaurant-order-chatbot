client_config = {
    "CLIENT_APPLICATION": "WEBAPPLICATION", # Default and only config value for this version
    "PORT": 5555, # The port your flask app will be hosted at
    "DEBUG": False, # When this flag is set, the UI displays detailed riva data
    "VERBOSE": True  # print logs/details for diagnostics
}

riva_config = {
    "RIVA_SPEECH_API_URL": "192.168.1.180:50051", # Replace the IP port with your hosted RIVA endpoint
    "VERBOSE": True  # print logs/details for diagnostics
}

rasa_config = {
    "VERBOSE": False, # Print logs/details for diagnostics
    "RASA_API_URL": "http://192.168.1.180:5005", # Replace the IP & Port with the rasa-weatherbot's IP & Port
}

asr_config = {
    "VERBOSE": False, # Print logs/details for diagnostics
    "SAMPLING_RATE": 16000, # The Sampling Rate for the audio input file. The only value currently supported is 16000
    "LANGUAGE_CODE": "en-US", # The language code as a BCP-47 language tag. The only value currently supported is "en-US"
    "ENABLE_AUTOMATIC_PUNCTUATION": True, # Enable or Disable punctuation in the transcript generated. The only value currently supported by the chatbot is True (Although Riva ASR supports both True & False)
}

tts_config = {
    "VERBOSE": True, # Print logs/details for diagnostics
    "SAMPLE_RATE": 22050, # The speech is generated at this sampling rate. The only value currently supported is 22050
    "LANGUAGE_CODE": "en-US", # The language code as a BCP-47 language tag. The only value currently supported is "en-US"
    "VOICE_NAME": "ljspeech", # The voice name for the speech generated. The only value currently supported is "ljspeech"
}

rivanlp_config = {
    "VERBOSE": False, # Print logs/details for diagnostics
    "NLU_FALLBACK_THRESHOLD": 0.3 # When Intent's confidence/score is less than this value, intent is set to nlu_fallback
    }
