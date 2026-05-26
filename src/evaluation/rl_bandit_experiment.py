import random

random.seed(42)


actions = [
    "keyword_retrieval",
    "semantic_retrieval",
    "safety_response",
    "fallback_response"
]


training_examples = [
    {
        "question": "ik heb honger",
        "state": "food_question",
        "best_action": "keyword_retrieval"
    },
    {
        "question": "waar kan ik douchen",
        "state": "hygiene_question",
        "best_action": "semantic_retrieval"
    },
    {
        "question": "ik wil drugs gebruiken",
        "state": "safety_question",
        "best_action": "safety_response"
    },
    {
        "question": "ik heb pijn op mijn borst",
        "state": "medical_emergency",
        "best_action": "safety_response"
    },
    {
        "question": "ik weet niet waar ik hulp kan krijgen",
        "state": "unknown_question",
        "best_action": "fallback_response"
    },
    {
        "question": "ik help iemand die honger heeft",
        "state": "helper_food_question",
        "best_action": "keyword_retrieval"
    },
    {
        "question": "een cliënt zoekt opvang",
        "state": "helper_shelter_question",
        "best_action": "semantic_retrieval"
    }
]


q_values = {}

action_counts = {}

for example in training_examples:
    state = example["state"]

    q_values[state] = {
        action: 0.0
        for action in actions
    }

    action_counts[state] = {
        action: 0
        for action in actions
    }


def choose_action(state, epsilon=0.2):

    if random.random() < epsilon:
        return random.choice(actions)

    return max(
        q_values[state],
        key=q_values[state].get
    )


def get_reward(chosen_action, best_action):

    if chosen_action == best_action:
        return 1.0

    if (
        chosen_action in ["keyword_retrieval", "semantic_retrieval"]
        and best_action in ["keyword_retrieval", "semantic_retrieval"]
    ):
        return 0.5

    return -1.0


episodes = 500

total_reward = 0

for episode in range(episodes):

    example = random.choice(training_examples)

    state = example["state"]
    best_action = example["best_action"]

    chosen_action = choose_action(state)

    reward = get_reward(
        chosen_action,
        best_action
    )

    total_reward += reward

    action_counts[state][chosen_action] += 1

    q_values[state][chosen_action] = (
        q_values[state][chosen_action]
        +
        (
            reward - q_values[state][chosen_action]
        )
        /
        action_counts[state][chosen_action]
    )


print("\nContextual RL Bandit experiment klaar\n")

print("Gemiddelde reward:")
print(round(total_reward / episodes, 2))

print("\nBeste actie per vraagtype:")

for state, values in q_values.items():

    best_action = max(
        values,
        key=values.get
    )

    print(f"{state}: {best_action} ({values[best_action]:.2f})")

print("\nQ-values per vraagtype:")

for state, values in q_values.items():
    print(f"\nState: {state}")

    for action, value in values.items():
        print(f"  {action}: {value:.2f}")