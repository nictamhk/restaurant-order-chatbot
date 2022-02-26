import grpc
import riva.modules.client.src.riva_proto.audio_pb2 as ri
import riva.modules.client.src.riva_proto.riva_tts_pb2 as rtts
import riva.modules.client.src.riva_proto.riva_tts_pb2_grpc as rtts_srv
from riva.tts.tts_processing.main_pronunciation import RunPronuncations

class TTSPipe(object):
    def __init__(self):
        . . . .
        self._buff = queue.Queue()
        self._flusher = bytes(np.zeros(dtype=np.int16,
                              shape=(self.sample_rate, 1))) # Silence audio
        self.pronounce = RunPronunciation(pronounce_dict_path)

    def start(self):
        self.channel = grpc.insecure_channel(riva_config["Riva_SPEECH_API_URL"])
        self.tts_client = rtts_srv.RivaSpeechSynthesisStub(self.channel)

    def fill_buffer(self, in_data):
        if len(in_data):
            self._buff.put(in_data)

    def get_speech(self):
        """
        The method used to perform TTS
        """
        while not self.closed:
            if not self._buff.empty():
                try:
                    text = self._buff.get(block = False, timeout = 0)
                    req = rtts.SynthesizeSpeechRequest()
                    req.text = self.pronounce.get_text(text)
                    req.language_code = 'en-US'
                    req.encoding = self.audio_encoding
                    req.sample_rate_hz = self.sample_rate
                    req.voice_name = self.voice_name
                    duration = 0
                    self.current_tts_duration = 0
                    responses = self.tts_client.SynthesizeOnline(req)

                    for resp in responses:
                        datalen = len(resp.audio) // 4
                        data32 = np.ndarray(buffer = resp.audio,
                                            dtype = np.float32,
                                            shape = (datalen, 1))
                        data16 = np.int16(data32 * 23173.26)
                        speech = bytes(data16.data)
                        duration += len(data16)*2 / (self.sample_rate*1*16/8)
                        self.current_tts_duration += duration
                        yield speech

                except Exception as e:
                    print('[Riva TTS] ERROR:', e)

