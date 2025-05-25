from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, constr
import html

app = FastAPI()

class UserInput(BaseModel):
    query: constr(strip_whitespace=True, min_length=1)

@app.get("/sanitize-input")
async def sanitize_input(user_input: UserInput):
    # Sanitize the input to prevent XSS
    sanitized_input = html.escape(user_input.query)
    return {"sanitized_data": sanitized_input}