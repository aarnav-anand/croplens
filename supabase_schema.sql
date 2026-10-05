-- =========================================================
-- CropLens Supabase Database Schema
-- Run this in your Supabase Project: SQL Editor -> New Query
-- =========================================================

-- 1. Create the `farmers` table for DIF authentication & scan credits
CREATE TABLE IF NOT EXISTS public.farmers (
    dif_code TEXT PRIMARY KEY,
    croplens INTEGER NOT NULL DEFAULT 10,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.farmers ENABLE ROW LEVEL SECURITY;

-- Allow public/anon access to read and update scan credits
CREATE POLICY "Allow public select on farmers"
    ON public.farmers FOR SELECT
    USING (true);

CREATE POLICY "Allow public update on farmers"
    ON public.farmers FOR UPDATE
    USING (true);

CREATE POLICY "Allow public insert on farmers"
    ON public.farmers FOR INSERT
    WITH CHECK (true);

-- Seed initial test farmers
INSERT INTO public.farmers (dif_code, croplens)
VALUES 
    ('AB12', 10),
    ('CD34', 5),
    ('EF56', 25),
    ('KL78', 8),
    ('XY99', 15)
ON CONFLICT (dif_code) DO NOTHING;


-- 2. Create the `outbreak_reports` table for community outbreak mapping
CREATE TABLE IF NOT EXISTS public.outbreak_reports (
    id TEXT PRIMARY KEY,
    disease TEXT NOT NULL,
    crop TEXT NOT NULL,
    confidence NUMERIC DEFAULT 95.0,
    farmer_name TEXT NOT NULL,
    farmer_dif TEXT DEFAULT 'GUEST',
    center_lat DOUBLE PRECISION NOT NULL,
    center_lng DOUBLE PRECISION NOT NULL,
    notes TEXT,
    language TEXT DEFAULT 'en',
    ai_provider TEXT DEFAULT 'gemini',
    reported_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.outbreak_reports ENABLE ROW LEVEL SECURITY;

-- Allow public/anon access to read and insert outbreak reports
CREATE POLICY "Allow public select on outbreak_reports"
    ON public.outbreak_reports FOR SELECT
    USING (true);

CREATE POLICY "Allow public insert on outbreak_reports"
    ON public.outbreak_reports FOR INSERT
    WITH CHECK (true);

-- Seed sample initial outbreak reports
INSERT INTO public.outbreak_reports (id, disease, crop, confidence, farmer_name, farmer_dif, center_lat, center_lng, notes, language, ai_provider, reported_at)
VALUES
    ('rep-001', 'Early Blight', 'Tomato', 96.4, 'Rajesh Kumar', 'AB12', 28.6139, 77.2090, 'Noticed dark spots with concentric rings on lower tomato foliage.', 'en', 'gemini', NOW() - INTERVAL '4 hours'),
    ('rep-002', 'Apple Scab', 'Apple', 97.2, 'Suresh Patel', 'CD34', 31.1048, 77.1734, 'Brown scabby spots visible across orchard trees.', 'en', 'gemini', NOW() - INTERVAL '1 day')
ON CONFLICT (id) DO NOTHING;
