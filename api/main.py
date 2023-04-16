from fastapi import FastAPI
from starlette.responses import StreamingResponse
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
model = GPTNeoXForCausalLM.from_pretrained(checkpoint, cache_dir=cache_dir, device_map="auto").half()
print("Model loaded.")

def generator(body, max_steps = 2048*2):
    input = f"<|prompter|>{body.prompt}<|endoftext|><|assistant|>"
    max_new_tokens = 4
    for _ in range(max_steps):
        inputs = tokenizer(input, return_tensors="pt")
        inputs.to(0)
        tokens = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=True, temperature=0.9, top_k=50, top_p=0.9, repetition_penalty=1.2)
        input = tokenizer.decode(tokens[0])
        response = input.split('<|assistant|>')[-1].split('<|endoftext|>')[0]
        if input.endswith('<|endoftext|>'): return response
        yield response

class Body(BaseModel):
    prompt: str

@app.post("/")
async def generate(body: Body):
    return StreamingResponse(
            content=generator(body),
            media_type="text/plain"
        )
    