from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
import torch

def use_falcon():
    # Use a pipeline as a high-level helper
    model = "tiiuae/falcon-7b"
    tokenizer = AutoTokenizer.from_pretrained(model)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
    )
    sequences = pipe(
       "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )
    for seq in sequences:
        print(f"Result: {seq['generated_text']}")


def main():
    use_falcon()
    # with open("../resource/processed-text.txt", "r", encoding="utf-8") as f:
    #     processed_text = f.read()

    # # Based on https://github.com/rohan-paul/MachineLearning-DeepLearning-Code-for-my-YouTube-Channel/blob/master/NLP/FinBERT_Long_Text_Part_2.ipynb
    # tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    # tokens = tokenizer.encode_plus(processed_text, add_special_tokens=True, return_tensors="pt")
    # chunked_input_ids = tokens["input_ids"][0].split(tokenizer.model_max_length )
    # chunked_attn_mask = tokens["attention_mask"][0].split(tokenizer.model_max_length )
    # print(len(chunked_input_ids), chunked_input_ids[0].shape, tokenizer.model_max_length )

    # # REFACTOR: Idee zum schön machen Padde die sequence lang genug damit sie einfach mit nem reshape gesplittet werden kann
    # # TODO Padde last sequence and make it into dict so modell can process it

    # model = AutoModel.from_pretrained("facebook/bart-large-cnn")
    # # TODO model forward and decode tokens into text


    # Legacy Code
    #summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    #print(summarizer(processed_text, max_length=130, min_length=30, do_sample=False))

if __name__ == "__main__":
    main()