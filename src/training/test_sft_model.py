from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch


BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

LORA_PATH = "models/rottermaatje-sft"


def main():

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL
    )

    model = PeftModel.from_pretrained(
        base_model,
        LORA_PATH
    )

    print("RotterMaatje SFT model geladen.")
    print("Typ 'stop' om te stoppen.")

    while True:

        question = input("\nVraag: ")

        if question.lower() == "stop":
            break

        prompt = f"""
Gebruiker:
{question}

Assistent:
"""

        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.2
            )

        answer = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        print("\nAntwoord:")
        print(answer)


if __name__ == "__main__":
    main()