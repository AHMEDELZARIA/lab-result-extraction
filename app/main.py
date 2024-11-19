from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    return {"status": "File has been received successfully"}