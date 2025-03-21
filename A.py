import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="expense_db"
    )
from pydantic import BaseModel
from typing import Optional

class ExpenseRequest(BaseModel):
    request_id: int
    user_id: int
    category: str
    amount: float
    description: Optional[str] = None
    file_status: int  # 1 if file needs to be uploaded, 0 otherwise

class FileUpload(BaseModel):
    request_id: int
    filename: str
    file_type: str
    file_size: int

from database import get_db_connection

def insert_expense_request(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO expense_requests (request_id, user_id, category, amount, description, file_status)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (data.request_id, data.user_id, data.category, data.amount, data.description, data.file_status)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def insert_file_metadata(request_id, filename, file_type, file_size):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO file_attachments (request_id, filename, file_type, file_size)
             VALUES (%s, %s, %s, %s)"""
    cursor.execute(sql, (request_id, filename, file_type, file_size))
    conn.commit()
    conn.close()

from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Depends
import httpx
from models import ExpenseRequest
from queries import insert_expense_request, insert_file_metadata

app = FastAPI()

# API 1: Upload JSON Data
@app.post("/upload-data/")
async def upload_data(expense: ExpenseRequest, background_tasks: BackgroundTasks):
    insert_expense_request(expense)
    
    # If file_status is 1, trigger file upload API in the background
    if expense.file_status == 1:
        background_tasks.add_task(call_file_upload_api, expense.request_id)

    return {"message": "Expense request saved", "request_id": expense.request_id}

# API 2: Upload File (Triggered Separately)
@app.post("/upload-file/{request_id}")
async def upload_file(request_id: int, file: UploadFile = File(...)):
    file_content = await file.read()
    file_metadata = {
        "request_id": request_id,
        "filename": file.filename,
        "file_type": file.content_type,
        "file_size": len(file_content)
    }

    insert_file_metadata(request_id, file_metadata["filename"], file_metadata["file_type"], file_metadata["file_size"])

    return {"message": "File uploaded successfully", "filename": file.filename}

# Function to Call File Upload API (Triggered Automatically)
async def call_file_upload_api(request_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://127.0.0.1:8000/upload-file/{request_id}")
    return response.json()



CREATE TABLE expense_requests (
    request_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    file_status TINYINT NOT NULL DEFAULT 0
);

CREATE TABLE file_attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size INT,
    FOREIGN KEY (request_id) REFERENCES expense_requests(request_id) ON DELETE CASCADE
);
