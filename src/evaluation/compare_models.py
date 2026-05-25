from services.chatbot_service import ChatbotService


TEST_QUESTIONS = [
    "ik wil eten",
    "ik heb honger",
    "waar kan ik douchen",
    "ik heb geen id",
    "ik heb geen papieren",
    "ik ben niet verzekerd",
    "ik wil drugs gebruiken",
    "ik heb pijn op mijn borst",
    "Where can I shower?",
    "I have no insurance",
    "انا جوعان",
    "انا ليس لدي مكان للنوم",
    "Nie mam miejsca do spania"
]


MODELS = {
    "Qwen": "qwen/qwen3-4b-instruct-2507",
    "Gemma": "google/gemma-2-2b-it"
}


def main():

    for model_label, model_name in MODELS.items():

        print("\n" + "=" * 60)
        print(f"MODEL: {model_label}")
        print("=" * 60)

        chatbot = ChatbotService(
            model_name=model_name
        )

        for question in TEST_QUESTIONS:

            answer = chatbot.generate_answer(
                question
            )

            print("\n---")
            print(f"Vraag: {question}")
            print(f"Antwoord: {answer}")


if __name__ == "__main__":
    main()