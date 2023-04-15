from transformers import AutoTokenizer, GPTNeoXForCausalLM

checkpoint = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = GPTNeoXForCausalLM.from_pretrained(checkpoint)
inputs = tokenizer("<|prompter|>What is a meme, and what's the history behind this word?<|endoftext|><|assistant|>", return_tensors="pt")
tokens = model.generate(**inputs)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))