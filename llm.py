from aiohttp import web
from urllib import parse
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m")
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
print("====== Model Loaded ======")

def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

async def cleanup_kwargs(kwargs):
    for key in kwargs:
        if kwargs[key].isdigit():
            kwargs[key]=int(kwargs[key])
        elif is_float(kwargs[key]):
            kwargs[key]=float(kwargs[key])
        elif kwargs[key] in ["true","false"]:
            kwargs[key]=kwargs[key]=="true"
        else:
            kwargs[key]=tokenizer(kwargs[key],return_tensors="pt").input_ids
            if key!="input_ids":
                kwargs[key]=kwargs[key][0]
    return kwargs

async def handle_generation(request):
    kwargs=dict(parse.parse_qsl(await request.text()))
    print(kwargs)
    kwargs=await cleanup_kwargs(kwargs)
    print(kwargs)
    output_tokens=model.generate(**kwargs).squeeze(0)
    #print(output_tokens)
    output_text=tokenizer.decode(output_tokens,skip_special_tokens=True)
    print(output_text)
    return web.Response(text=output_text)

app=web.Application()
app.add_routes([web.post("/",handle_generation)])
web.run_app(app,port=4242)
