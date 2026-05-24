from rag.faq_loader import FAQLoader
from rag.faq_retriever import FAQRetriever


def main():

    loader = FAQLoader(
        "data/faq/faq.json"
    )

    faq_data = loader.load_faq()

    retriever = FAQRetriever()

    retriever.fit(faq_data)

    test_questions = [
        "Ik zoek een plek om te slapen",
        "Waar kan ik douchen?",
        "Ik heb medische hulp nodig",
        "Ik heb geen eten"
    ]

    for question in test_questions:

        result = retriever.retrieve(question)

        print(f"Vraag: {question}")
        print(f"Gevonden FAQ: {result['question']}")
        print(f"Antwoord: {result['answer']}")
        print(f"Score: {result['score']:.3f}")


if __name__ == "__main__":
    main()