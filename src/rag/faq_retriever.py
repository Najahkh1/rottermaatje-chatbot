from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class FAQRetriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.questions = []
        self.answers = []
        self.faq_texts = []
        self.embeddings = None

    def fit(self, faq_data):

        self.questions = [
            item["question"]
            for item in faq_data
        ]

        self.answers = [
            item["answer"]
            for item in faq_data
        ]

        # combine question + answer
        self.faq_texts = [
            f"{item['question']} {item['answer']}"
            for item in faq_data
        ]

        self.embeddings = self.model.encode(
            self.faq_texts
        )

    def retrieve(self, user_question, threshold=0.60):

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
                "score": float(best_score),
                "matched": False
            }

        return {
            "question": self.questions[best_index],
            "answer": self.answers[best_index],
            "score": float(best_score),
            "matched": True
        }