import sys

sys.path.append("../riva")

from riva.asr.asr import ASRPipe
from riva.rasa.rasa import RASAPipe
from riva.tts.tts import TTSPipe

class ChatBot(object):
    """
    Pipeline of the chatbot
    """
    def __init__(self, user_conversation_index, verbose=False):
        self.id = user_conversation_index
        self.asr = ASRPipe()
        self.rasa = RASAPipe(user_conversation_index)
        self.tts = TTSPipe()
        self.thread_asr = None
        self.pause_asr_flag = False
        self.enableTTS = False

    """
    ASR
    """
    def server_asr(self):
        self.asr.main_asr()

    def start_asr(self, sio):
        self.thread_asr = sio.start_background_task(self.server_asr)

    def asr_fill_buffer(self, audio_in):
        if not self.pause_asr_flag:
            self.asr.fill_buffer(audio_in)
            
    def get_asr_transcript(self):
        return self.asr.get_transcript()


    """
    TTS
    """
    def rasa_tts_pipeline(self, text):
        response_text = self.rasa.request_rasa_for_question(text)
        if len(response_text) and self.enableTTS == True:
            self.tts_fill_buffer(response_text)
        return response_text

    def tts_fill_buffer(self, response_text):
        if self.enableTTS:
            self.tts.fill_buffer(response_text)
    def get_tts_speech(self):
        return self.tts.get_speech()