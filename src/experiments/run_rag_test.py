import pandas as pd
from openai import OpenAI

from rag.faq_loader import FAQLoader
from rag.faq_retriever import FAQRetriever


def main():
    questions_df = pd.read_csv("data/evaluations/test_questions.csv")

    loader = FAQLoader("data/faq/faq.json")
    faq_data = loader.load_faq()

    retriever = FAQRetriever()
    retriever.fit(faq_data)

    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    )

    results = []

    for index, row in questions_df.iterrows():
        question = row["question"]
        category = row["category"]

        retrieved = retriever.retrieve(question)
        faq_context = retrieved["answer"]
        similarity_score = retrieved["score"]
        matched_faq = retrieved["question"]

        prompt = f"""
Je bent RotterMaatje.

Gebruik ALLEEN informatie uit de FAQ context.
Verzin geen telefoonnummers, adressen, websites of organisaties.
Geef geen medisch of juridisch advies.
Als informatie ontbreekt, zeg dat eerlijk.
Antwoord kort en duidelijk in eenvoudig Nederlands.

FAQ context:
{faq_context}

Vraag:
{question}
"""

        response = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        results.append({
            "question": question,
            "category": category,
            "matched_faq": matched_faq,
            "similarity_score": similarity_score,
            "answer": answer
        })

        print(f"Tested: {question}")

    results_df = pd.DataFrame(results)
    results_df.to_csv("results/model_outputs/rag_outputs.csv", index=False)

    print("RAG test completed.")
    print("Saved to results/model_outputs/rag_outputs.csv")


if __name__ == "__main__":
    main()