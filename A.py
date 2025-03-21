from fastapi import FastAPI, File, UploadFile, Form, Depends
from pydantic import BaseModel
import json

app = FastAPI()

# Define Pydantic model for JSON data
class ExpenseRequest(BaseModel):
    expense_type: str
    travel_mode: str
    accommodation_type: str

# Function to parse JSON string
def parse_json(json_data: str = Form(...)):
    return json.loads(json_data)

@app.post("/submit/")
async def submit_expense(
    json_data: dict = Depends(parse_json),  # JSON as string
    file: UploadFile = File(...)            # File Upload
):
    return {
        "json_data": json_data,
        "filename": file.filename,
        "content_type": file.content_type
    }
