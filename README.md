# 🌱 CropLens v3 — AI Crop Doctor

Mobile-friendly crop disease detector with Hindi/English support, DIF-code sign-in, credit tracking, Gemini AI fallback diagnosis, and outbreak reporting with farm polygon mapping.

---

## Features

| Feature | Details |
|---|---|
| 🌐 Language | English & Hindi — toggle anywhere in the app |
| 🔑 Sign-in | DIF code (2 letters + 2 digits, e.g. `AB12`) validated against `farmers` table |
| 🔬 Credits | Reads `croplens` field from `farmers` table; decrements on every scan; shows modal when 0 |
| 🤖 AI Diagnosis | If model confidence < 80%, calls Gemini 2.0 Flash for disease name + 3-4 point treatment advice |
| 🚩 Outbreak Report | Polygon/marker drawing tool on map; stores farm GeoJSON + disease to `outbreak_reports` table |
| 📱 Mobile-friendly | Max 720px layout, large touch targets, camera input |

---

## Supabase Setup

### Table: `farmers`
| Column | Type | Notes |
|---|---|---|
| `dif_code` | text | Primary key / unique — format: 2 letters + 2 digits, e.g. `AB12` |
| `croplens` | integer | Number of scans remaining |
| any other fields | — | Optional |

### Table: `outbreak_reports`
| Column | Type | Notes |
|---|---|---|
| `id` | uuid | auto |
| `disease_class` | text | Raw model class, e.g. `Tomato___Late_blight` |
| `crop` | text | |
| `disease` | text | |
| `confidence` | float | 0-100 |
| `farmer_name` | text | |
| `farmer_dif` | text | |
| `farm_geojson` | text | JSON string of drawn shapes |
| `center_lat` | float | Computed centroid latitude |
| `center_lng` | float | Computed centroid longitude |
| `notes` | text | nullable |
| `language` | text | `en` or `hi` |
| `reported_at` | timestamptz | |

---

## Secrets Setup

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in:

```toml
[supabase]
url = "https://xxxx.supabase.co"
key = "your-anon-key"

[gemini]
api_key = "your-gemini-api-key"
```

Get a **Gemini API key** free at: https://aistudio.google.com/app/apikey

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Credits-Exhausted Flow

When a farmer's `croplens` field reaches 0, the app blocks further scans and displays a modal directing them to: **agrifusion-net.vercel.app**

## DIF Code Format

- Exactly 4 characters
- First 2: alphabetic (A-Z, case-insensitive)
- Last 2: numeric digits (0-9)
- Examples: `AB12`, `KR07`, `MH99`
