from openai import OpenAI
from rag.faq_retriever import FAQRetriever
import json

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

prompt = f"""
Je bent RotterMaatje.

Gebruik ALLEEN informatie uit de FAQ context.
Verzin geen telefoonnummers, adressen of organisaties.
Als informatie ontbreekt, zeg dat eerlijk.

FAQ context:
{faq_answer}

Vraag:
{question}

Geef een kort antwoord in eenvoudig Nederlands.
"""

with open("data/faq/faq.json", "r") as f:
    faq_data = json.load(f)

retriever = FAQRetriever()
retriever.fit(faq_data)

while True:
    user_question = input("\nVraag: ")

    result = retriever.retrieve(user_question)

    context = result["answer"]

    response = client.chat.completions.create(
        model="qwen/qwen3-4b-instruct-2507",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Gebruikersvraag:
{user_question}

FAQ context:
{context}

Beantwoord de vraag kort en behulpzaam.
"""
            }
        ],
        temperature=0.3
    )

    answer = response.choices[0].message.content

    print("\nAntwoord:")
    print(answer)