import grpc
import riva.modules.client.src.riva_proto.audio_pb2 as ri
import riva.modules.client.src.riva_proto.riva_asr_pb2 as risr
import riva.modules.client.src.riva_proto.riva_asr_pb2_grpc as risr_svr
import queue

"""
    An ASR Pipe handles operations from Riva ASR
"""
class ASRPipe(object):
    def __init__(self):
        # Length of speech to be processed
        self.chunk = int(self.sampling_rate / 10)

        # Creates a queue
        self._buff = queue.Queue()
        self._transcript = queue.Queue() 

        self.closed = False

    def fill_buffer(self, in_data):
        """
        Continuously collect data from audio stream to the buffer
        :param in_data:
        :return: (None)
        """

        self._buff.put(in_data)

    def main_asr(self):
        config = risr.RecognitionConfig(
            encoding = ri.AudioEncoding.LINEAR_PCM,
            sample_rate_hertz = self.sampling_rate,
            language_code = 'en-US',
            max_alternatives = 1,
            enable_automatic_punctuation = True
        )
        streaming_config = risr.StreamingRecognitionConfig(
            config = config,
            interim_results = self.stream_interim_results
        )

        if self.verbose:
            print("[Riva ASR] Starting Background ASR Process")

        self.request_generator = self.build_request_generator()
        requests = (risr.StreamingRecongizeRequest(audio_content = content)
                    for content in self.request_generator)

        def build_generator(cfg, gen):
            yield risr.StreamingRecognizeRequest(streaming_config = cfg)
            for x in gen:
                yield x
            yield cfg

        if self.verbose:
            print("[Riva ASR] StreamingRecognize Start")

        # Generate Transcript Response
        responses = self.asr_client.StreamingRecognize(build_generator(
            streaming_config, requests)
        )

        # Print transcript response
        self.listen_print_loop(responses)