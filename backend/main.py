import json        
import os        # Built-in Python module for interacting with the operating system
import cv2       # OpenCV library for image processing. Used to read, convert, and transform images.
import io        # Built-in Python module for handling data streams in memory. Used to wrap image bytes into a stream for HTTP response.
import numpy as np
from fastapi.responses import StreamingResponse
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
    
def order_points(pts):
    rect = np.zeros((4,2), dtype = "float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    doc_contour = None
    for c in contours:
        epsilon = 0.02 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        if len(approx) == 4:
            doc_contour = approx
            break
    if doc_contour is not None:

        rect = order_points(doc_contour.reshape(4,2))
        (tl, tr, br, bl) = rect    
        widthA = np.sqrt((br[0]-bl[0])**2 + (br[1]-bl[1])**2)
        widthB = np.sqrt((tr[0]-tl[0])**2 + (tr[1]-tl[1])**2) 
        maxWidth = max(int(widthA),int(widthB))

        heightA = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2)
        heightB = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2)
        maxHeight = max(int(heightA), int(heightB))

        dst = np.array([
            [0,0],
            [maxWidth-1,0],
            [maxWidth-1, maxHeight-1],
            [0, maxHeight-1]],
            dtype = "float32"
            )
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (maxWidth,maxHeight))
        return warped
    else:
        coords = np.column_stack(np.where(edges>0))
        if len(coords) == 0:
            return image
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle =  -angle
        if abs(angle) < 0.5:
            return image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        return rotated
    
def binarize(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    return thresh
    
@app.post("/deskew")
async def deskew_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = deskew(image)
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
    result = binarize(image)
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




    