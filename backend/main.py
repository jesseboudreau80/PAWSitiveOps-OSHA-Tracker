from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import pdfkit
import os

app = FastAPI(title="PAWSitiveOps OSHA Tracker", version="0.1")

UPLOAD_DIR = "uploads"
PDF_DIR = "pdf_reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

@app.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        df = pd.read_excel(file_path)
        records = df.to_dict(orient="records")
        return {"message": "Excel file uploaded successfully", "rows": len(records)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate_pdf/")
async def generate_pdf(title: str = Form(...), content: str = Form(...)):
    try:
        html_content = f"<h1>{title}</h1><p>{content}</p>"
        pdf_path = os.path.join(PDF_DIR, f"{title.replace(' ', '_')}.pdf")
        pdfkit.from_string(html_content, pdf_path)
        return FileResponse(pdf_path, media_type="application/pdf", filename=os.path.basename(pdf_path))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "Welcome to the PAWSitiveOps OSHA Tracker API"}
