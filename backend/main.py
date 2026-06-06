import json
import os
from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()     # creates the application instance. Every route is registered on this object.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("uploads", exist_ok=True)  

def load_metadata():
    if os.path.exists("metadata.json"):
        with open("metadata.json","r") as f:
            data = json.load(f)
        return data
    else:
        return []
    
def save_metadata(filename, size, upload_time):
    existing_data = load_metadata()

    new_entry = {
        "filename": filename,
        "size": size,
        "upload_time": upload_time 
    }
    existing_data.append(new_entry)

    with open("metadata.json", "w") as f:
        json.dump(existing_data, f, indent=4)
            
@app.post("/upload")            # creating an API route that listens for incoming POST requests.
async def upload_image(file: UploadFile = File(...)):   # async keyword makes the function asynchronous so that server can handle multiplr reuests simultaneously 
    contents = await file.read()   # await tells Python to not block other requests while waiting as reading a file is time taking

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)
    save_metadata(                                      
        file.filename,
        len(contents),                                      
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
    )
    return {"message": "Upload successful", "filename": file.filename}

@app.get("/files")
async def get_files():
    return load_metadata()




    