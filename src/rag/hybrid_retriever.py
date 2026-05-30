from rag.faq_retriever import FAQRetriever


class HybridRetriever:
    def __init__(self):
        self.semantic_retriever = FAQRetriever()

    def fit(self, faq_data):
        self.faq_data = faq_data
        self.semantic_retriever.fit(faq_data)

    def keyword_score(self, question, faq_question):
        question_words = set(question.lower().split())
        faq_words = set(faq_question.lower().split())

        if not question_words:
            return 0

        overlap = question_words.intersection(faq_words)
        return len(overlap) / len(question_words)

    def retrieve(self, question):
        semantic_result = self.semantic_retriever.retrieve(question)

        best_keyword_item = None
        best_keyword_score = 0

        for item in self.faq_data:
            score = self.keyword_score(
                question,
                item.get("question", "")
            )

            if score > best_keyword_score:
                best_keyword_score = score
                best_keyword_item = item

        semantic_score = semantic_result.get("score", 0)

        if best_keyword_item and best_keyword_score >= 0.4:
            return {
                "matched": True,
                "answer": best_keyword_item["answer"],
                "method": "keyword_retrieval",
                "score": best_keyword_score
            }

        if semantic_result.get("matched"):
            return {
                "matched": True,
                "answer": semantic_result["answer"],
                "method": "semantic_retrieval",
                "score": semantic_score
            }

        return {
            "matched": False,
            "answer": "",
            "method": "fallback",
            "score": 0
        }
