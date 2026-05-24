from services.chatbot_service import ChatbotService


def main():
    chatbot = ChatbotService(
        model_name="gemma-3-4b-it"
    )

    print("RotterMaatje chatbot gestart met Gemma.")
    print("Typ 'stop' om te stoppen.")

    while True:
        user_question = input("\nVraag: ")

        if user_question.lower().strip() in ["stop", "exit", "quit"]:
            print("Chatbot gestopt.")
            break

        answer = chatbot.generate_answer(user_question)

        print("\nAntwoord:")
        print(answer)


if __name__ == "__main__":
    main()