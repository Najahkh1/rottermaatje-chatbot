import random


actions = [
    "keyword_retrieval",
    "semantic_retrieval",
    "safety_response",
    "fallback_response"
]


q_values = {
    action: 0.0
    for action in actions
}

action_counts = {
    action: 0
    for action in actions
}


training_examples = [
    {
        "question": "ik heb honger",
        "best_action": "keyword_retrieval"
    },
    {
        "question": "waar kan ik douchen",
        "best_action": "semantic_retrieval"
    },
    {
        "question": "ik wil drugs gebruiken",
        "best_action": "safety_response"
    },
    {
        "question": "ik heb pijn op mijn borst",
        "best_action": "safety_response"
    },
    {
        "question": "ik weet niet waar ik hulp kan krijgen",
        "best_action": "fallback_response"
    },
    {
        "question": "ik help iemand die honger heeft",
        "best_action": "keyword_retrieval"
    },
    {
        "question": "een cliënt zoekt opvang",
        "best_action": "semantic_retrieval"
    }
]


def choose_action(epsilon=0.2):
    if random.random() < epsilon:
        return random.choice(actions)

    return max(
        q_values,
        key=q_values.get
    )


def get_reward(chosen_action, best_action):
    if chosen_action == best_action:
        return 1.0

    if chosen_action in ["keyword_retrieval", "semantic_retrieval"] and best_action in ["keyword_retrieval", "semantic_retrieval"]:
        return 0.5

    return -1.0


episodes = 50

for episode in range(episodes):

    example = random.choice(training_examples)

    chosen_action = choose_action()

    reward = get_reward(
        chosen_action,
        example["best_action"]
    )

    action_counts[chosen_action] += 1

    q_values[chosen_action] = q_values[chosen_action] + (
        reward - q_values[chosen_action]
    ) / action_counts[chosen_action]


print("\nRL Bandit experiment klaar\n")

print("Q-values:")
for action, value in q_values.items():
    print(f"{action}: {value:.2f}")

print("\nAantal keuzes:")
for action, count in action_counts.items():
    print(f"{action}: {count}")