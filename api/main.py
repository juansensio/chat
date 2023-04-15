from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, GPTNeoXForCausalLM

app = FastAPI()

checkpoint = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
cache_dir = '/cache'
tokenizer = AutoTokenizer.from_pretrained(checkpoint, cache_dir=cache_dir)
model = GPTNeoXForCausalLM.from_pretrained(checkpoint, cache_dir=cache_dir)


class Body(BaseModel):
    prompt: str

@app.post("/")
def generate(body: Body):
    inputs = tokenizer(f"<|prompter|>{body.prompt}<|endoftext|><|assistant|>", return_tensors="pt")
    tokens = model.generate(**inputs)
    return tokenizer.decode(tokens[0], skip_special_tokens=True)