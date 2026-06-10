from dotenv import load_dotenv
load_dotenv()

import json        
import os        # Built-in Python module for interacting with the operating system
import cv2       # OpenCV library for image processing. Used to read, convert, and transform images.
import io        # Built-in Python module for handling data streams in memory. Used to wrap image bytes into a stream for HTTP response.
import numpy as np
import easyocr
import re
import google.generativeai as genai
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from image_processor import ImageProcessor

app = FastAPI()     # creates the application instance. Every route is registered on this object.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],              
    allow_headers=["*"],
)
os.makedirs("uploads", exist_ok=True) 
processor = ImageProcessor() 
reader = easyocr.Reader(['en'])
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")


def refine_with_llm(ocr_text):
    try:
        prompt = f"""
        You are a document data extraction assistant.
        Below is raw OCR text extracted from a scanned document.
        The text may contain errors due to OCR misreading.

        OCR Text:
        {ocr_text}

        Extract and correct these fields and return ONLY a valid JSON object with no extra text:
        {{
            "name": "extracted name or null",
            "date": "extracted date or null",
            "id": "extracted id number or null",
            "address": "extracted address or null"
        }}
        """
        response = model.generate_content(prompt)
        raw = response.text
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}

def extract_fields(text):
    fields = {}

    name_match = re.search(r"(?:name|wane|nane)[:\s#@]+([A-Za-z\s]+)", text, re.IGNORECASE)
    date_match = re.search(r"(?:date|dated|@ated)[:\s#@]+(\d{1,2}[\/:]\d{1,2}[\/:]\d{4})", text, re.IGNORECASE)
    id_match = re.search(r"(?:id|703|1d)[:\s#@]+(\d+)", text, re.IGNORECASE)
    address_match = re.search(r"(?:address|addressd)[:\s#@]+(.+)", text, re.IGNORECASE)

    if name_match:
        fields["name"] = name_match.group(1).strip()
    if date_match:
        fields["date"] = date_match.group(1).strip()
    if id_match:
        fields["ID"] = id_match.group(1).strip()
    if address_match:
        fields["address"] = address_match.group(1).strip()

    return fields

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
    
@app.post("/ocr")
async def ocr_text(file:UploadFile = File(...)):

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    binarized_img = processor.binarize(image)
    result = reader.readtext(binarized_img )
    texts = [item[1] for item in result]
    full_text = "\n".join(texts)
    return {
    "text": full_text,
    "fields": extract_fields(full_text),
    "refined_text":refine_with_llm(full_text)
}
    
@app.post("/deskew")
async def deskew_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = processor.deskew(image)
    _,buffer = cv2.imencode('.jpg',result)

    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/jpeg"
    )

@app.post("/binarize")
async def binarize_img(file:UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents,np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = processor.binarize(image)
    _, buffer = cv2.imencode('.jpg',result)
    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/jpeg" 
    )

@app.post("/process")
async def process_img(file: UploadFile = File(...)):
    contents = await file.read()   
    nparr = np.frombuffer(contents, np.uint8)         # Coverting the image into an array with data type as unsigned 8-bit integer 
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)     # Decoding the numpy array into image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # Coverting the image into gryscale image
    _, buffer = cv2.imencode('.jpg', gray)            # Converts image matrix backs to bytes to send over HTTP

    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),                 # io.BytesIO() wraps those bytes into a file-like stream
        media_type = "image/jpeg"                     # StreamingResponse sends that stream back to the frontend (React)
    )

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




    