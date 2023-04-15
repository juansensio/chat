from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, GPTNeoXForCausalLM
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading model...")
checkpoint = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
cache_dir = '/cache'
tokenizer = AutoTokenizer.from_pretrained(checkpoint, cache_dir=cache_dir)
model = GPTNeoXForCausalLM.from_pretrained(checkpoint, cache_dir=cache_dir).half().cuda()
print("Model loaded.")

class Body(BaseModel):
    prompt: str

@app.post("/")
def generate(body: Body):
    inputs = tokenizer(f"<|prompter|>{body.prompt}<|endoftext|><|assistant|>", return_tensors="pt")
    inputs.to(0)
    tokens = model.generate(**inputs, max_length=1024, do_sample=True)
    return {
        'response': tokenizer.decode(tokens[0]).split('<|assistant|>')[-1].split('<|endoftext|>')[0]
    }