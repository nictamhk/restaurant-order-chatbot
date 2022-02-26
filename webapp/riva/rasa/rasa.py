class RASAPipe(object):
    def __init__(self, user_conversation_index):
        self.user_conversation_index = user_conversation_index

    def request_rasa_for_question(self, message):
        rasa_requestdata = {'message': message,
                            'sender': self.user_conservation_index}
        x = requests.post(self.messages_url, json = rasa_requestdata)
        rasa_response = x.json()

        # Calls Rasa to process the text and retrieve the response
        processed_rasa_response = self.process_rasa_response(rasa_response)

        return processed_rasa_response