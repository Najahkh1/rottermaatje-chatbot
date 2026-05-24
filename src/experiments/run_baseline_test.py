import pandas as pd

from models.lm_studio_client import LMStudioClient


def load_system_prompt():
    with open(
        "prompts/system_prompts/rottermaatje_system_prompt.txt",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def main():

    questions_df = pd.read_csv(
        "data/evaluations/test_questions.csv"
    )

    system_prompt = load_system_prompt()

    client = LMStudioClient()

    results = []

    for index, row in questions_df.iterrows():

        question = row["question"]
        category = row["category"]

        print(f"Testing question {index + 1}: {question}")

        answer = client.generate_response(
            user_question=question,
            system_prompt=system_prompt
        )

        results.append({
            "question": question,
            "category": category,
            "answer": answer
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        "results/model_outputs/system_prompt_outputs.csv",
        index=False
    )

    print("System prompt test completed.")
    print("Saved to results/model_outputs/system_prompt_outputs.csv")


if __name__ == "__main__":
    main()