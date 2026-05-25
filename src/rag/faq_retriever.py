from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class FAQRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.faq_data = []
        self.questions = []
        self.answers = []
        self.faq_texts = []
        self.embeddings = None

    def fit(self, faq_data):

        self.faq_data = faq_data

        self.questions = [
            item.get("question", "")
            for item in faq_data
        ]

        self.answers = [
            item.get("answer", "")
            for item in faq_data
        ]

        self.faq_texts = []

        for item in faq_data:

            question = item.get("question", "")
            answer = item.get("answer", "")
            category = item.get("category", "")
            keywords = item.get("keywords", [])

            keywords_text = " ".join(keywords)

            text = f"{category} {question} {keywords_text} {answer}"

            self.faq_texts.append(text)

        self.embeddings = self.model.encode(
            self.faq_texts
        )

    def keyword_retrieve(self, user_question):

        user_text = user_question.lower()

        for item in self.faq_data:

            keywords = item.get("keywords", [])

            for keyword in keywords:

                keyword = keyword.lower()

                if keyword in user_text:

                    return {
                        "question": item.get("question"),
                        "answer": item.get("answer"),
                        "category": item.get("category"),
                        "score": 1.0,
                        "matched": True,
                        "method": "keyword"
                    }

        return None

    def semantic_retrieve(self, user_question, threshold):

        question_embedding = self.model.encode(
            [user_question]
        )

        similarities = cosine_similarity(
            question_embedding,
            self.embeddings
        )[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]

        if best_score < threshold:

            return {
                "question": None,
                "answer": (
                    "Ik weet het niet zeker op basis van de beschikbare FAQ. "
                    "Vraag hulp bij de Pauluskerk of een hulpverlener."
                ),
                "category": None,
                "score": float(best_score),
                "matched": False,
                "method": "fallback"
            }

        return {
            "question": self.questions[best_index],
            "answer": self.answers[best_index],
            "category": self.faq_data[best_index].get("category"),
            "score": float(best_score),
            "matched": True,
            "method": "semantic"
        }

    def retrieve(self, user_question, threshold=0.60):

        keyword_result = self.keyword_retrieve(
            user_question
        )

        if keyword_result:

            return keyword_result

        return self.semantic_retrieve(
            user_question,
            threshold
        )