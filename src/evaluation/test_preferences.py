import json

from services.chatbot_service import ChatbotService


def load_preferences(path):

    preferences = []

    with open(path, "r", encoding="utf-8") as file:

        for line in file:

            preferences.append(
                json.loads(line)
            )

    return preferences


def evaluate_answer(
    generated,
    chosen,
    rejected
):

    generated = generated.lower()
    chosen = chosen.lower()
    rejected = rejected.lower()

    chosen_score = 0
    rejected_score = 0

    chosen_words = chosen.split()

    rejected_words = rejected.split()

    for word in chosen_words:

        if word in generated:
            chosen_score += 1

    for word in rejected_words:

        if word in generated:
            rejected_score += 1

    final_score = chosen_score - rejected_score

    return final_score


def main():

    chatbot = ChatbotService(
        model_name="gemma-3-4b-it"
    )

    preferences = load_preferences(
        "data/evaluations/preference_dataset.jsonl"
    )

    total_score = 0

    for item in preferences:

        prompt = item["prompt"]

        chosen = item["chosen"]

        rejected = item["rejected"]

        generated = chatbot.generate_answer(
            prompt
        )

        score = evaluate_answer(
            generated,
            chosen,
            rejected
        )

        total_score += score

        print("\n====================")
        print("PROMPT:")
        print(prompt)

        print("\nMODEL:")
        print(generated)

        print("\nCHOSEN:")
        print(chosen)

        print("\nREJECTED:")
        print(rejected)

        print(f"\nSCORE: {score}")

    print("\n====================")
    print(f"TOTALE SCORE: {total_score}")


if __name__ == "__main__":
    main()