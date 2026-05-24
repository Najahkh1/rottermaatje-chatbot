import pandas as pd
from openai import OpenAI

from rag.faq_loader import FAQLoader
from rag.faq_retriever import FAQRetriever


def main():

    # laad multilingual testvragen
    questions_df = pd.read_csv(
        "data/evaluations/multilingual_test_questions.csv"
    )

    # laad FAQ data
    loader = FAQLoader("data/faq/faq.json")
    faq_data = loader.load_faq()

    # maak retriever
    retriever = FAQRetriever()
    retriever.fit(faq_data)

    # LM Studio client
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

    results = []

    for index, row in questions_df.iterrows():

        question = row["question"]
        language = row["language"]
        category = row["category"]
        expected_behavior = row["expected_behavior"]

        # retrieval
        retrieved = retriever.retrieve(question)

        matched_faq = retrieved["question"]
        faq_context = retrieved["answer"]
        similarity_score = retrieved["score"]

        # threshold
        if similarity_score < 0.75:

            final_answer = (
                "Ik weet het niet zeker op basis van de beschikbare FAQ. "
                "Vraag hulp bij de Pauluskerk of een hulpverlener."
            )

        else:

            prompt = f"""
Je bent RotterMaatje.

Gebruik ALLEEN informatie uit de FAQ context.
Verzin geen telefoonnummers, websites of organisaties.
Geef geen medisch of juridisch advies.
Als informatie ontbreekt, zeg dat eerlijk.

Antwoord kort, veilig en duidelijk.

FAQ context:
{faq_context}

Vraag:
{question}
"""

            response = client.chat.completions.create(
                model="local-model",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            final_answer = response.choices[0].message.content

        results.append({
            "question": question,
            "language": language,
            "category": category,
            "matched_faq": matched_faq,
            "similarity_score": similarity_score,
            "answer": final_answer,
            "expected_behavior": expected_behavior
        })

        print(f"Tested: {question}")

    # save resultaten
    results_df = pd.DataFrame(results)

    results_df.to_csv(
        "results/model_outputs/multilingual_outputs.csv",
        index=False
    )

    print("\nMultilingual test completed.")
    print(
        "Saved to results/model_outputs/multilingual_outputs.csv"
    )


if __name__ == "__main__":
    main()