import requests

response = requests.post(
    "http://127.0.0.1:8000/generate",
    json={
        "prompt": "Explain Agentic AI in one paragraph."
    }
)

data = response.json()

print(
    "Status Code:",
    response.status_code
)

print(
    "API Status:",
    data.get("status")
)

print(
    "Model Used:",
    data.get("model")
)

print("Generated Response:")
print(
    data.get("response")
)





