from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME
import os


VISION_MODEL_NAME = os.getenv("VISION_MODEL_NAME", MODEL_NAME)


class PromptRequest(BaseModel):
    prompt: str
    image_base64: Optional[str] = None
    image_mime_type: Optional[str] = None


class PromptResponse(BaseModel):
    response: str
    model: str
    status: str


app = FastAPI(
    title="Gradio FastAPI AI Backend",
    description="FastAPI backend for a Gradio AI assistant",
    version="1.0.0"
)

client = Groq(api_key=GROQ_API_KEY)


@app.get("/")
def home():
    return {
        "message": "FastAPI backend is running."
    }


def generate_llm_response(
    prompt: str,
    image_base64: Optional[str] = None,
    image_mime_type: Optional[str] = None
):
    try:
        if image_base64 and image_mime_type:
            model_to_use = VISION_MODEL_NAME

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{image_mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        else:
            model_to_use = MODEL_NAME

            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        response = client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )

        generated_text = response.choices[0].message.content

        return {
            "response": generated_text,
            "model": model_to_use,
            "status": "success"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/generate")
def generate_response_get(prompt: str):
    return generate_llm_response(prompt)


@app.post("/generate", response_model=PromptResponse)
def generate_response_post(request: PromptRequest):
    return generate_llm_response(
        prompt=request.prompt,
        image_base64=request.image_base64,
        image_mime_type=request.image_mime_type
    )
    
    