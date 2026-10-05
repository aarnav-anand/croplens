# 🌱 CropLens — AI Crop Doctor

CropLens is an AI-powered agricultural tool that identifies crop leaf diseases from photos, provides targeted treatment and prevention advice in English and Hindi, and enables farmers to map and report regional disease outbreaks.

---

## ✨ Features

- **DIF Code Authentication**: Farmer sign-in via 2-letter + 2-digit identifier (e.g. `AB12`, `CD34`, `EF56`) with scan credits management.
- **Multilingual Support**: Complete English and Hindi (हिन्दी) localization for all instructions, diagnosis labels, and treatment advice.
- **Photo Upload & Live Camera**: Capture leaves using your device's webcam/camera or upload image files (JPG, PNG).
- **Multimodal AI Diagnosis**: Server-side Gemini AI Vision (`gemini-3.8-flash`) combined with an agronomic pathology knowledge base covering 22+ plant diseases.
- **Detailed Treatment & Prevention**: Severity ratings, visible symptoms, field hygiene prevention, and targeted 4-point chemical/organic treatment protocols.
- **Outbreak Mapping & Reporting**: Interactive OpenStreetMap interface to pin farm coordinates, check against water bodies, and broadcast outbreak alerts to neighboring growers.
- **Dual Deployment**:
  - **AI Studio Web App**: Node.js + Vite React + Express full-stack architecture on port 3000.
  - **Gradio Application**: `gradio_app.py` for deployment to Hugging Face Spaces or standalone Gradio servers.

---

## 🚀 Running the App

### Option 1: AI Studio Web Runtime (Vite + React + Express)

```bash
# Install dependencies
npm install

# Run dev server on port 3000
npm run dev

# Build for production
npm run build
```

### Option 2: Gradio Deployment

```bash
# Install Python dependencies
pip install -r requirements-gradio.txt

# Launch Gradio app
python gradio_app.py
```

---

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=3000
```
