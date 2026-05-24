class KeywordRetriever:

    def __init__(self):
        self.faq_data = []

    def fit(self, faq_data):
        self.faq_data = faq_data

    def retrieve(self, user_question):
        text = user_question.lower()

        rules = {
            "voedsel": ["honger", "eten", "maaltijd", "brood", "koffie", "thee"],
            "douchen": ["douchen", "douche", "wassen"],
            "opvang": ["slapen", "slaapplek", "opvang", "dakloos", "nachtopvang"],
            "identiteit": ["id", "paspoort", "identiteitsbewijs"],
            "juridisch": ["papieren", "documenten", "juridisch", "bezwaar"],
            "medisch": ["huisarts", "dokter", "arts", "niet verzekerd", "medische hulp"],
            "drugs": ["drugs", "verslaafd", "afkicken"]
        }

        for category, keywords in rules.items():
            if any(keyword in text for keyword in keywords):
                for item in self.faq_data:
                    faq_text = (
                        item.get("question", "") + " " + item.get("answer", "")
                    ).lower()

                    if any(keyword in faq_text for keyword in keywords):
                        return {
                            "question": item["question"],
                            "answer": item["answer"],
                            "score": 1.0,
                            "matched": True,
                            "method": "keyword",
                            "category": category
                        }

        return {
            "question": None,
            "answer": "",
            "score": 0.0,
            "matched": False,
            "method": "keyword",
            "category": None
        }