from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch


BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

LORA_PATH = "models/rottermaatje-sft-v2/checkpoint-225"

def build_prompt(question):
    return f"""
Je bent RotterMaatje.

Regels:
- Antwoord in dezelfde taal als de gebruiker.
- Gebruik eenvoudige B1-taal.
- Geef korte antwoorden.
- Gebruik maximaal één emoji.
- Geef geen medisch of juridisch advies.
- Verzin geen informatie.

Gebruiker:
{question}

Assistent:
"""


def main():

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL
    )

    model = PeftModel.from_pretrained(
        base_model,
        LORA_PATH
    )

    model.eval()

    print("RotterMaatje Instruction SFT model geladen.")
    print("Typ 'stop' om te stoppen.")

    while True:

        question = input("\nVraag: ")

        if question.lower() == "stop":
            break

        prompt = build_prompt(question)

        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                max_new_tokens=80,
                temperature=0.2,
                do_sample=False,
                repetition_penalty=1.15,
                pad_token_id=tokenizer.pad_token_id
            )

        full_output = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        answer = full_output.split("Assistent:")[-1].strip()

        print("\nAntwoord:")
        print(answer)


if __name__ == "__main__":
    main()