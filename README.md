# Smart Document Scanner

A fullstack AI-powered document scanner built with React and FastAPI. Users can drag-and-drop or select document images for upload. The backend processes images using OpenCV, extracts text using EasyOCR, and refines extracted fields using Google Gemini LLM.

---

## Project Structure

```
smart-document-scanner/
├── frontend/                       # React application
│   ├── src/
│   │   ├── component/
│   │   │   ├── UploadForm.jsx      # Drag-and-drop file upload component
│   │   │   ├── ImagePreview.jsx    # Side-by-side original vs processed display
│   │   │   └── DataFrame.jsx       # Auto-populated form (upcoming - Week 3 Day 4)
│   │   ├── services/
│   │   │   └── api.js              # All API call functions
│   │   ├── App.jsx                 # Root component
│   │   └── App.css                 # Global styles
│   ├── package.json
│   └── .gitignore
│
├── backend/                        # Python FastAPI application
│   ├── main.py                     # API routes and server logic
│   ├── image_processor.py          # OpenCV image processing class
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # API keys (gitignored)
│   └── .gitignore
│
└── README.md
```

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React (Create React App) | UI framework |
| react-hot-toast | Toast notifications |
| Vanilla CSS | Styling |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.13 | Core language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| python-multipart | File upload handling |
| OpenCV | Image processing |
| NumPy | Array operations for image data |
| EasyOCR | AI-based text extraction from images |
| Google Gemini API | LLM for cleaning and structuring OCR output |
| python-dotenv | Secure API key management |

---

## Getting Started

### Prerequisites
- Node.js (v16+)
- Python 3.8+
- Git
- Google Gemini API key from https://aistudio.google.com

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Runs at: `http://localhost:3000`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Runs at: `http://127.0.0.1:8000`

API docs: `http://127.0.0.1:8000/docs`

### Environment Variables

Create a `.env` file inside the `backend/` folder:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload and save an image or document file |
| POST | `/process` | Convert uploaded image to grayscale |
| POST | `/deskew` | Correct perspective and straighten document |
| POST | `/binarize` | Apply adaptive thresholding for clean black/white output |
| POST | `/ocr` | Extract text and structured fields using EasyOCR + Gemini |
| GET | `/files` | Get all uploaded file metadata |

### POST `/upload`
**Request:** `multipart/form-data` with `file` field

**Response:**
```json
{
  "message": "Upload successful",
  "filename": "photo.jpg"
}
```

### POST `/ocr`
**Request:** `multipart/form-data` with `file` field

**Response:**
```json
{
  "text": "raw OCR extracted text",
  "fields": {
    "ID": "123456",
    "address": "extracted address"
  },
  "refined_text": {
    "name": "John Doe",
    "date": "15/06/2023",
    "id": "123456",
    "address": "Dunball Road"
  }
}
```

### GET `/files`
**Response:**
```json
[
  {
    "filename": "photo.jpg",
    "size": 204800,
    "upload_time": "2024-01-15 10:30:00"
  }
]
```

---

## Features

### Week 1 — Core Upload System 
- [x] Drag-and-drop file upload UI
- [x] Click-to-select file fallback
- [x] FastAPI backend with file saving to `uploads/` folder
- [x] React to FastAPI connection with CORS configured
- [x] Toast notification on upload success and error
- [x] JSON-based metadata tracking (filename, size, upload time)
- [x] GitHub repository setup with `.gitignore`

### Week 2 — Image Processing
- [x] Grayscale conversion using OpenCV
- [x] Perspective correction (deskewing) using contour detection
- [x] Angle-based rotation fallback for skewed documents
- [x] Adaptive thresholding for clean black/white OCR-ready output
- [x] Side-by-side Original vs Processed image display in React UI
- [x] Refactored image processing into reusable `ImageProcessor` class

### Week 3 — AI/OCR Pipeline
- [x] EasyOCR integration for text extraction from document images
- [x] Regex-based structured field extraction (Name, Date, ID, Address)
- [x] Google Gemini LLM integration for intelligent OCR error correction
- [x] Returns raw text, regex fields, and LLM-refined fields in one response
- [x] Dynamic React form auto-populated with extracted data
- [ ] End-to-end demo: Upload → Process → Extract → Fill Form (Day 5)

---

## How It Works

```
User selects or drags a document image
        ↓
React stores file in useState
        ↓
Click Upload
        ↓
Original image displayed on left
        ↓
fetch POST → /upload → FastAPI saves file + metadata
        ↓
fetch POST → /binarize → OpenCV processes image
        ↓
Processed image displayed on right
        ↓
fetch POST → /ocr
        ↓
EasyOCR extracts raw text from binarized image
        ↓
Regex finds structured fields (Name, Date, ID, Address)
        ↓
Gemini LLM corrects OCR errors and returns clean JSON
        ↓
Structured data returned to frontend
```

---

## Image Processing Pipeline

```
Original color photo
        ↓
/deskew → perspective correction or angle rotation
        ↓
/process → grayscale conversion
        ↓
/binarize → gaussian blur + adaptive threshold
        ↓
Clean black/white document ready for OCR
```

---

## Development Notes

- `backend/uploads/` is gitignored — contains user uploaded files
- `backend/metadata.json` is gitignored — auto generated at runtime
- `backend/.env` is gitignored — contains sensitive API keys
- `frontend/node_modules/` is gitignored — run `npm install` to recreate
- CORS configured for `http://localhost:3000`
- EasyOCR downloads language models on first run — takes a few minutes
- Gemini API free tier has rate limits — paid key needed for production

---

## Author

**Shreya Sarangi**
GitHub: [@sarangi-shreya](https://github.com/sarangi-shreya)

---

*Built as part of a structured 3-week internship project covering fullstack development, computer vision, and AI integration.*
