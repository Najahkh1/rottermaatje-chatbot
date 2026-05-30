from services.chatbot_service import ChatbotService


test_cases = [
    ("ik heb honger", "food_question", "keyword_retrieval"),
    ("ik wil eten", "food_question", "keyword_retrieval"),
    ("waar kan ik douchen", "hygiene_question", "semantic_retrieval"),
    ("ik heb geen plek om te slapen", "shelter_question", "semantic_retrieval"),
    ("ik help iemand die honger heeft", "helper_food_question", "keyword_retrieval"),
    ("een cliënt heeft geen plek om te slapen", "helper_shelter_question", "semantic_retrieval"),
    ("ik heb geen ID", "identity_question", "semantic_retrieval"),
    ("ik heb geen papieren", "undocumented_question", "semantic_retrieval"),
    ("ik wil drugs gebruiken", "safety_question", "safety_response"),
    ("ik wil afkicken", "recovery_question", "safety_response"),
    ("ik wil dood", "suicide_question", "safety_response"),
    ("ik heb pijn op mijn borst", "medical_emergency", "safety_response"),
]


def main():
    chatbot = ChatbotService()

    correct = 0

    for question, expected_state, expected_action in test_cases:
        strategy = chatbot.rl_selector.select_strategy(question)

        state = strategy.get("state")
        action = strategy.get("action")

        is_correct = (
            state == expected_state
            and action == expected_action
        )

        if is_correct:
            correct += 1

        print("=" * 50)
        print(f"Vraag: {question}")
        print(f"Verwacht: {expected_state} / {expected_action}")
        print(f"Gekregen: {state} / {action}")
        print(f"Correct: {is_correct}")

    score = correct / len(test_cases)

    print("=" * 50)
    print(f"RL accuracy: {score:.2f}")
    print(f"Correct: {correct}/{len(test_cases)}")


if __name__ == "__main__":
    main()