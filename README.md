# AI Academic Content Detector

A full-stack web application that detects whether academic text is AI-generated or Human-written using Machine Learning.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python FastAPI |
| ML | Scikit-Learn (Logistic Regression, Random Forest, SVM) |
| Database | SQLite (via SQLAlchemy) |
| Charts | Chart.js |

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (optional, for advanced features)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start server (auto-trains model on first run)
python run.py
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: http://localhost:5173

## Features

- **AI vs Human Detection** with confidence scores
- **Content Statistics**: word count, sentences, vocabulary richness
- **AI Indicators**: repetitive patterns, sentence uniformity, lexical diversity
- **Visualizations**: pie chart + feature importance bar chart
- **Model Info**: algorithm details, dataset info, evaluation metrics
- **Admin Dashboard**: upload dataset, retrain model, view history
- **Dark Mode** support
- **PDF Export** of analysis results
- **Mobile Responsive** design

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Analyze text |
| GET | `/api/model-info` | Model metadata |
| POST | `/api/admin/upload-dataset` | Upload CSV |
| POST | `/api/admin/retrain` | Retrain model |
| GET | `/api/admin/history` | Prediction history |
| GET | `/api/admin/export` | Export CSV report |
