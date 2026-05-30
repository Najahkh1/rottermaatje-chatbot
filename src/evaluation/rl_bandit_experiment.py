import random


class ContextualBanditExperiment:
    def __init__(self, episodes=3000, epsilon=0.05, seed=42):
        random.seed(seed)

        self.episodes = episodes
        self.epsilon = epsilon

        self.actions = [
            "keyword_retrieval",
            "semantic_retrieval",
            "safety_response",
            "fallback_response"
        ]

        self.training_examples = [
            ("ik heb honger", "food_question", "keyword_retrieval"),
            ("ik wil eten", "food_question", "keyword_retrieval"),
            ("waar kan ik eten", "food_question", "keyword_retrieval"),

            ("waar kan ik douchen", "hygiene_question", "semantic_retrieval"),
            ("ik wil douchen", "hygiene_question", "semantic_retrieval"),

            ("ik heb geen plek om te slapen", "shelter_question", "semantic_retrieval"),
            ("ik slaap op straat", "shelter_question", "semantic_retrieval"),
            ("ik zoek opvang", "shelter_question", "semantic_retrieval"),

            ("ik help iemand die honger heeft", "helper_food_question", "keyword_retrieval"),
            ("er is een dakloze die honger heeft", "helper_food_question", "keyword_retrieval"),

            ("een cliënt zoekt opvang", "helper_shelter_question", "semantic_retrieval"),
            ("een dakloze zoekt een slaapplek", "helper_shelter_question", "semantic_retrieval"),

            ("ik heb geen ID", "identity_question", "semantic_retrieval"),
            ("ik ben mijn ID kwijt", "identity_question", "semantic_retrieval"),

            ("ik heb geen papieren", "undocumented_question", "semantic_retrieval"),
            ("ik heb geen documenten", "undocumented_question", "semantic_retrieval"),

            ("ik zoek een postadres", "postal_address_question", "semantic_retrieval"),
            ("ik heb geen adres voor post", "postal_address_question", "semantic_retrieval"),

            ("ik ben niet verzekerd", "medical_care_question", "semantic_retrieval"),
            ("ik heb medische hulp nodig", "medical_care_question", "semantic_retrieval"),

            ("ik wil drugs gebruiken", "safety_question", "safety_response"),
            ("ik ben high", "safety_question", "safety_response"),

            ("ik wil afkicken", "recovery_question", "safety_response"),
            ("ik ben verslaafd", "recovery_question", "safety_response"),

            ("ik wil dood", "suicide_question", "safety_response"),
            ("ik wil niet meer leven", "suicide_question", "safety_response"),

            ("ik heb pijn op mijn borst", "medical_emergency", "safety_response"),
            ("ik ben benauwd", "medical_emergency", "safety_response"),

            ("ik weet niet waar ik hulp kan krijgen", "unknown_question", "fallback_response"),
            ("help mij", "unknown_question", "fallback_response"),
        ]

        self.q_values = {}
        self.action_counts = {}

        for _, state, best_action in self.training_examples:
            if state not in self.q_values:
                self.q_values[state] = {
                    action: 0.0 for action in self.actions
                }

                self.action_counts[state] = {
                    action: 0 for action in self.actions
                }

            if best_action in ["keyword_retrieval", "semantic_retrieval"]:
                self.q_values[state]["keyword_retrieval"] = 0.5
                self.q_values[state]["semantic_retrieval"] = 0.5

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return max(
            self.q_values[state],
            key=self.q_values[state].get
        )

    def get_reward(self, chosen_action, best_action):
        if chosen_action == best_action:
            return 1.0

        if (
            chosen_action in ["keyword_retrieval", "semantic_retrieval"]
            and best_action in ["keyword_retrieval", "semantic_retrieval"]
        ):
            return 0.5

        return -1.0

    def train(self):
        total_reward = 0

        for _ in range(self.episodes):
            _, state, best_action = random.choice(self.training_examples)

            chosen_action = self.choose_action(state)

            reward = self.get_reward(
                chosen_action,
                best_action
            )

            total_reward += reward

            self.action_counts[state][chosen_action] += 1

            self.q_values[state][chosen_action] += (
                reward - self.q_values[state][chosen_action]
            ) / self.action_counts[state][chosen_action]

        return total_reward / self.episodes

    def print_results(self, average_reward):
        print("\nContextual RL Bandit experiment klaar\n")

        print("Gemiddelde reward:")
        print(round(average_reward, 2))

        print("\nBeste actie per vraagtype:")

        for state, values in self.q_values.items():
            best_action = max(values, key=values.get)
            print(f"{state}: {best_action} ({values[best_action]:.2f})")

        print("\nQ-values per vraagtype:")

        for state, values in self.q_values.items():
            print(f"\nState: {state}")

            for action, value in values.items():
                print(f"  {action}: {value:.2f}")


def main():
    experiment = ContextualBanditExperiment(
        episodes=3000,
        epsilon=0.05
    )

    average_reward = experiment.train()
    experiment.print_results(average_reward)


if __name__ == "__main__":
    main()