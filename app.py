import os
import openai
import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from dotenv import load_dotenv

load_dotenv()

client = httpx.AsyncClient(timeout=60)

app = FastAPI()

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT_N")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY_N")


def get_openai_chat_resp_stream():
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",  # engine = "deployment_name".
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "generate a 300 words paragraph",
            },
        ],
        temperature=0.7,
        stream=True,
    )
    for chunk in response:
        current_content = chunk["choices"][0]["delta"].get("content", "")
        print(current_content)
        yield current_content


@app.get("/openai/chat/stream")
def openai_chat_stream():
    return StreamingResponse(
        get_openai_chat_resp_stream(), media_type="text/event-stream"
    )


@app.get("/chat/stream")
async def chat_stream():
    r_req = client.build_request("GET", "http://localhost:9999/openai/chat/stream")
    r_resp = await client.send(r_req, stream=True)
    return StreamingResponse(r_resp.aiter_raw(), media_type="text/event-stream")


# hypercorn app --bind 0.0.0.0:9999
