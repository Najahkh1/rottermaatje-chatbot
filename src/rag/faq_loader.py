import json


class FAQLoader:

    def __init__(self, filepath):
        self.filepath = filepath

    def load_faq(self):

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as file:

            faq_data = json.load(file)

        return faq_data