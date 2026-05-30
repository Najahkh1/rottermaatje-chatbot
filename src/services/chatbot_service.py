from openai import OpenAI
import json

from rag.faq_loader import FAQLoader
from rag.faq_retriever import FAQRetriever
from evaluation.rl_strategy_selector import RLStrategySelector
from rag.hybrid_retriever import HybridRetriever

from safety.safety_rules import (
    is_helper_context,
    detect_language,
    is_medical_complaint,
    is_medical_care_question,
    is_drug_question,
    get_medical_safety_response,
    get_drug_safety_response,
    get_fallback_response,
    is_suicide_question,
    get_suicide_safety_response,
    is_recovery_question,
    get_recovery_response,
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

    def get_medical_care_context(self):

        for item in self.faq_data:

            question = item.get("question", "").lower()
            answer = item.get("answer", "").lower()
            category = item.get("category", "").lower()

            if (
                "medisch" in category
                or
                "huisarts" in question
                or
                "niet verzekerd" in question
                or
                "geen verzekering" in question
                or
                "onverzekerd" in question
                or
                "medische hulp" in question
                or
                "straatzorg" in answer
            ):

                return item.get("answer", "")

        return ""

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

    def get_context_from_faq(self, user_question, user_language):

        result = self.retriever.retrieve(
            user_question
        )

        if result["matched"]:

            return result["answer"]

        return get_fallback_response(
            user_language
        )

    def generate_answer(self, user_question):

        user_language = detect_language(
            user_question
        )
        if is_suicide_question(user_question):
            return get_suicide_safety_response(
                user_language
            )

        if is_recovery_question(user_question):
            return get_recovery_response(
                user_language
            )

        strategy = self.rl_selector.select_action(user_question)
        selected_action = strategy["action"]
        print("\nRL strategy:")
        print(strategy)
        # 1. Helper-context eerst via FAQ laten lopen
        # Voorbeelden:
        # - ik help iemand die medische hulp nodig heeft
        # - een dakloze is niet verzekerd
        # - ik help iemand die verslaafd is
        if is_helper_context(
            user_question
        ):

            result = self.retriever.retrieve(
                user_question
            )

            if result["matched"]:

                context = result["answer"]

            else:

                return get_fallback_response(
                    user_language
                )

        else:

            # 2. Directe medische klachten blijven safety-first
            # Voorbeeld: ik heb pijn op mijn borst
            if is_medical_complaint(
                user_question
            ):

                return get_medical_safety_response(
                    user_language
                )

            # 3. Directe drugsgebruik-vragen blijven safety-first
            # Voorbeeld: ik wil drugs gebruiken
            if is_drug_question(
                user_question
            ):

                return get_drug_safety_response(
                    user_language
                )

            # 4. Medische zorgvragen mogen FAQ-context gebruiken
            # Voorbeeld: ik ben niet verzekerd
            if is_medical_care_question(
                user_question
            ):

                result = self.retriever.retrieve(
                    user_question
                )

                if result["matched"]:

                    context = result["answer"]

                else:

                    context = self.get_medical_care_context()

                    if not context:

                        return get_fallback_response(
                            user_language
                        )

            else:

                result = self.retriever.retrieve(
                    user_question
                )

                if result["matched"]:

                    context = result["answer"]

                else:

                    return get_fallback_response(
                        user_language
                    )

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