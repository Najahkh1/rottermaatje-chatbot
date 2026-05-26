class RLStrategySelector:

    def __init__(self):

        self.best_actions = {
            "food_question": "keyword_retrieval",
            "hygiene_question": "semantic_retrieval",
            "safety_question": "safety_response",
            "medical_emergency": "safety_response",
            "unknown_question": "fallback_response",
            "helper_food_question": "keyword_retrieval",
            "helper_shelter_question": "semantic_retrieval",
            "medical_care_question": "semantic_retrieval",
            "identity_question": "semantic_retrieval",
            "undocumented_question": "semantic_retrieval",
            "postal_address_question": "semantic_retrieval",
            "work_question": "semantic_retrieval",
            "legal_question": "semantic_retrieval"
        }

    def detect_state(self, question):

        text = question.lower()

        if (
            "id" in text
            or "identiteitsbewijs" in text
            or "paspoort" in text
            or "document kwijt" in text
            or "documenten kwijt" in text
        ):
            return "identity_question"

        if (
            "zonder papieren" in text
            or "geen papieren" in text
            or "ongedocumenteerd" in text
            or "geen documenten" in text
        ):
            return "undocumented_question"

        if (
            "postadres" in text
            or "briefadres" in text
            or "adres aanvragen" in text
        ):
            return "postal_address_question"

        if (
            "werk zoeken" in text
            or "baan zoeken" in text
            or "werk nodig" in text
            or "uitzendbureau" in text
        ):
            return "work_question"

        if (
            "juridische hulp" in text
            or "juridisch" in text
            or "bezwaar" in text
            or "rechtshulp" in text
        ):
            return "legal_question"

        if (
            "ik help iemand" in text
            or "ik help een" in text
            or "er is iemand" in text
            or "er is een dakloze" in text
            or "een cliënt" in text
            or "een client" in text
            or "een persoon" in text
            or "een dakloze" in text
        ):

            if (
                "honger" in text
                or "eten" in text
                or "voedsel" in text
            ):
                return "helper_food_question"

            if (
                "opvang" in text
                or "slapen" in text
                or "slaapplaats" in text
                or "geen plek" in text
            ):
                return "helper_shelter_question"

            if (
                "medisch" in text
                or "medische hulp" in text
                or "verzekering" in text
                or "verzekerd" in text
                or "onverzekerd" in text
                or "dokter" in text
                or "huisarts" in text
            ):
                return "medical_care_question"

        if (
            "drugs" in text
            or "verslaafd" in text
            or "afkicken" in text
            or "alcohol" in text
        ):
            return "safety_question"

        if (
            "pijn op mijn borst" in text
            or "spoed" in text
            or "nood" in text
            or "benauwd" in text
        ):
            return "medical_emergency"

        if (
            "honger" in text
            or "eten" in text
            or "voedsel" in text
        ):
            return "food_question"

        if (
            "douchen" in text
            or "douche" in text
            or "wassen" in text
        ):
            return "hygiene_question"

        return "unknown_question"

    def select_action(self, question):

        state = self.detect_state(question)

        action = self.best_actions.get(
            state,
            "semantic_retrieval"
        )

        return {
            "state": state,
            "action": action
        }