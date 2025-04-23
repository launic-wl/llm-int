import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
load_dotenv()


def load_model():
    access_token = os.environ.get("HUGGINGFACE_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", token=access_token)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", token=access_token)
    return tokenizer, model


def process_message(message, tokenizer, model):
    # Tokenize input
    inputs = tokenizer(message, return_tensors="pt")

    # Generate output
    outputs = model.generate(**inputs,
                             max_new_tokens=750,
                             do_sample=True,
                             temperature=0.7,
                             top_k=50,
                             top_p=0.9)

    # Return the generated text
    return tokenizer.decode(outputs[0])
