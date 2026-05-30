from openai import OpenAI
import json

from rag.faq_loader import FAQLoader
from evaluation.rl_strategy_selector import RLStrategySelector
from rag.hybrid_retriever import HybridRetriever

from safety.safety_rules import (
    detect_language,
    is_medical_complaint,
    is_drug_question,
    get_medical_safety_response,
    get_drug_safety_response,
    get_fallback_response,
    is_suicide_question,
    get_suicide_safety_response,
    is_recovery_question,
    get_recovery_response
)


class ChatbotService:

    def __init__(
        self,
        model_name,
        faq_path="data/faq/faq.json",
        web_path="data/web/web_sources.json",
        base_url="http://localhost:1234/v1",
        api_key="lm-studio"
    ):

        self.model_name = model_name
        self.rl_selector = RLStrategySelector()

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        loader = FAQLoader(faq_path)
        self.faq_data = loader.load_faq()

        try:
            with open(web_path, "r", encoding="utf-8") as file:
                web_data = json.load(file)

            for item in web_data:
                self.faq_data.append({
                    "question": item.get("question", ""),
                    "answer": item.get("answer", ""),
                    "category": item.get("category", "web")
                })

        except Exception:
            print("Geen web_sources.json gevonden.")

        self.retriever = HybridRetriever()
        self.retriever.fit(self.faq_data)

        self.system_prompt = """
Je bent RotterMaatje.

Je helpt mensen met informatie uit de FAQ van de Pauluskerk Rotterdam.

Regels:
- Gebruik ALLEEN informatie uit de FAQ context.
- Verzin geen telefoonnummers, adressen, websites of organisaties.
- Geef geen medisch advies.
- Geef geen juridisch advies.
- Bij medische klachten: geef geen diagnose en geen behandeling.
- Bij gevaar of spoed: zeg dat de gebruiker 112 moet bellen.
- Als informatie ontbreekt, zeg dat eerlijk.
- Antwoord in dezelfde taal als de gebruiker.
- Geef korte, veilige en duidelijke antwoorden.
"""

    def build_prompt(
        self,
        user_question,
        user_language,
        context
    ):

        return f"""
Gebruikersvraag:
{user_question}

Gedetecteerde taal:
{user_language}

FAQ context:
{context}

Beantwoord de vraag in {user_language}.

Gebruik alleen informatie uit de FAQ context.
Vertaal de FAQ-informatie indien nodig.
Verzin geen extra informatie.

Geef een kort, veilig en duidelijk antwoord.
"""

    def generate_answer(self, user_question):

        user_language = detect_language(user_question)

        if is_suicide_question(user_question):
            return get_suicide_safety_response(user_language)

        if is_recovery_question(user_question):
            return get_recovery_response(user_language)

        if is_medical_complaint(user_question):
            return get_medical_safety_response(user_language)

        if is_drug_question(user_question):
            return get_drug_safety_response(user_language)

        strategy = self.rl_selector.select_action(user_question)
        selected_action = strategy["action"]

        print("\nRL strategy:")
        print(strategy)

        if selected_action == "safety_response":
            return get_fallback_response(user_language)

        if selected_action == "fallback_response":
            return get_fallback_response(user_language)

        if selected_action in ["keyword_retrieval", "semantic_retrieval"]:

            result = self.retriever.retrieve(user_question)

            if result["matched"]:
                context = result["answer"]
            else:
                return get_fallback_response(user_language)

        else:
            return get_fallback_response(user_language)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.build_prompt(
                        user_question,
                        user_language,
                        context
                    )
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content