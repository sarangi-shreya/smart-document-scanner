# Document Upload System

A fullstack document upload system built with React and FastAPI. Users can drag-and-drop or select files for upload, which are saved to the server with JSON-based metadata tracking.

---

## Project Structure

```
Document_Upload_System/
├── frontend/                   # React application
│   ├── src/
│   │   ├── component/
│   │   │   ├── UploadForm.jsx  # Drag-and-drop file upload component
│   │   │   ├── ImagePreview.jsx # (upcoming - Week 2)
│   │   │   └── DataFrame.jsx   # (upcoming - Week 3)
│   │   ├── services/
│   │   │   └── api.js          # API call functions
│   │   ├── App.jsx             # Root component
│   │   └── App.css             # Global styles
│   ├── package.json
│   └── .gitignore
│
├── backend/                    # Python FastAPI application
│   ├── main.py                 # API routes and server logic
│   ├── requirements.txt        # Python dependencies
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
| Python  | Core language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| python-multipart | File upload handling |

---

## Getting Started

### Prerequisites
- Node.js (v16+)
- Python 3.8+
- Git

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

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload an image or document file |
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

## Features — Week 1

- [x] Drag-and-drop file upload UI
- [x] Click-to-select file fallback
- [x] FastAPI backend with file saving to `uploads/` folder
- [x] React to FastAPI connection with CORS configured
- [x] Toast notification on upload success and error
- [x] JSON-based metadata tracking (filename, size, upload time)
- [x] GitHub repository setup with `.gitignore`

---

## How It Works

```
User selects or drags a file
        ↓
React stores file in useState
        ↓
Click Upload → file wrapped in FormData
        ↓
fetch POST → http://127.0.0.1:8000/upload
        ↓
FastAPI receives → saves file to uploads/
        ↓
Metadata saved to metadata.json
        ↓
JSON response → toast notification shown
```

---

## Development Notes

- `backend/uploads/` is gitignored — contains user uploaded files
- `backend/metadata.json` is gitignored — auto generated at runtime
- `frontend/node_modules/` is gitignored — run `npm install` to recreate
- CORS configured for `http://localhost:3000`

---

## Author

**Shreya Sarangi**
GitHub: [@sarangi-shreya](https://github.com/sarangi-shreya)

---

*Built as part of a structured 3-week internship project.*
