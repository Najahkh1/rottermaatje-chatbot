from services.chatbot_service import ChatbotService

chatbot = ChatbotService(
    model_name="qwen/qwen3-4b-instruct-2507"
)

test_questions = [
    "ik help iemand die honger heeft",
    "er is een dakloze die honger heeft",
    "een cliënt heeft geen plek om te slapen",
    "ik help iemand zonder ID",
    "er is iemand zonder papieren",
    "ik help iemand die wil douchen",
    "een dakloze is niet verzekerd",
    "ik help iemand die verslaafd is",
    "een cliënt zoekt een postadres",
    "ik help iemand die medische hulp nodig heeft"
]

for question in test_questions:
    print("\n" + "=" * 50)
    print("VRAAG:")
    print(question)

    answer = chatbot.generate_answer(question)

    print("\nANTWOORD:")
    print(answer)