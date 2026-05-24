from rag.faq_loader import FAQLoader
from rag.keyword_retriever import KeywordRetriever


def main():
    loader = FAQLoader("data/faq/faq.json")
    faq_data = loader.load_faq()

    retriever = KeywordRetriever()
    retriever.fit(faq_data)

    test_questions = [
        "Ik heb honger",
        "Ik wil douchen",
        "Ik heb geen opvang",
        "Ik heb geen ID",
        "Ik heb geen papieren",
        "Ik ben niet verzekerd",
        "Ik wil afkicken",
        "Ik wil drugs gebruiken"
    ]

    for question in test_questions:
        result = retriever.retrieve(question)

        print("\n====================")
        print(f"Vraag: {question}")
        print(f"Methode: {result['method']}")
        print(f"Categorie: {result['category']}")
        print(f"Gevonden FAQ: {result['question']}")
        print(f"Score: {result['score']}")
        print(f"Antwoord: {result['answer']}")


if __name__ == "__main__":
    main()