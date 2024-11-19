from fastapi import FastAPI, UploadFile, File

from app.validators.composite_validator import CompositeValidator
from app.validators.extention_validator import ExtensionValidator
from app.validators.mime_validator import MimeValidator
from app.validators.size_validator import SizeValidator

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    # Validate the file
    validator = CompositeValidator([
        ExtensionValidator(['pdf']),
        MimeValidator(['application/pdf']),
        SizeValidator(1)
    ])

    try:
        validator.validate(file)
    except Exception as e:
        return e

    return {"status": f"{file.filename} has been received successfully"}
