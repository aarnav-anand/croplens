import React, { useState, useEffect } from 'react';
import { Camera, Upload, ArrowRight, RotateCcw, AlertTriangle, ShieldCheck, MapPin, Sparkles, Send, X, ExternalLink, Leaf } from 'lucide-react';
import { TEXT } from './data/translations';
import { ReportMap } from './components/ReportMap';
import { CameraCapture } from './components/CameraCapture';

interface DiagnosisResult {
  is_leaf: boolean;
  confidence: number;
  disease: string;
  crop: string;
  treatment_en: string[] | null;
  treatment_hi: string[] | null;
  info: any;
  ai_provider?: string;
}

interface OutbreakReportItem {
  id: string;
  disease: string;
  crop: string;
  confidence: number;
  farmer_name: string;
  farmer_dif: string;
  center_lat: number;
  center_lng: number;
  notes?: string;
  language: string;
  reported_at: string;
}

export function App() {
  const [lang, setLang] = useState<'en' | 'hi'>('en');
  const [farmerDif, setFarmerDif] = useState<string | null>(() => localStorage.getItem('croplens_dif'));
  const [farmerCredits, setFarmerCredits] = useState<number | null>(() => {
    const saved = localStorage.getItem('croplens_credits');
    return saved !== null ? parseInt(saved, 10) : null;
  });
  const [difInput, setDifInput] = useState('');
  const [difError, setDifError] = useState<string | null>(null);
  const [isSigningIn, setIsSigningIn] = useState(false);

  // Photo & Camera State
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [showCamera, setShowCamera] = useState(false);
  const [cropInput, setCropInput] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [adviceLang, setAdviceLang] = useState<'en' | 'hi'>('en');

  // Report Outbreak State
  const [showReport, setShowReport] = useState(false);
  const [reportCoords, setReportCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [farmerName, setFarmerName] = useState('');
  const [reportNotes, setReportNotes] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);
  const [reportSuccessMsg, setReportSuccessMsg] = useState<string | null>(null);
  const [reportErrorMsg, setReportErrorMsg] = useState<string | null>(null);
  const [recentReports, setRecentReports] = useState<OutbreakReportItem[]>([]);
  const [showRecentReports, setShowRecentReports] = useState(false);
  const [showClosingPage, setShowClosingPage] = useState(false);

  const t = TEXT[lang];

  // Fetch recent reports
  useEffect(() => {
    fetch('/api/reports')
      .then((res) => res.json())
      .then((data) => {
        if (data.reports) setRecentReports(data.reports);
      })
      .catch((err) => console.warn('Could not fetch reports:', err));
  }, []);

  const handleSignIn = async (codeToTry?: string) => {
    const code = (codeToTry || difInput).trim().toUpperCase();
    setDifError(null);

    if (!/^[A-Za-z0-9]{4}$/.test(code)) {
      setDifError(t.dif_invalid_format);
      return;
    }

    setIsSigningIn(true);
    try {
      const res = await fetch('/api/farmer/lookup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dif_code: code }),
      });
      const data = await res.json();
      if (res.ok && data.dif_code) {
        setFarmerDif(data.dif_code);
        setFarmerCredits(data.credits);
        localStorage.setItem('croplens_dif', data.dif_code);
        localStorage.setItem('croplens_credits', String(data.credits));
        setDifInput('');
      } else {
        setDifError(t.dif_not_found);
      }
    } catch (err) {
      setDifError(t.dif_error);
    } finally {
      setIsSigningIn(false);
    }
  };

  const handleSignOut = () => {
    setFarmerDif(null);
    setFarmerCredits(null);
    localStorage.removeItem('croplens_dif');
    localStorage.removeItem('croplens_credits');
    setImageSrc(null);
    setDiagnosis(null);
    setShowReport(false);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setImageSrc(reader.result as string);
      setDiagnosis(null);
      setShowReport(false);
    };
    reader.readAsDataURL(file);
  };

  const handleCameraCapture = (base64: string) => {
    setImageSrc(base64);
    setShowCamera(false);
    setDiagnosis(null);
    setShowReport(false);
  };

  const handleAnalyze = async () => {
    if (!cropInput.trim()) {
      alert(t.crop_warning);
      return;
    }
    if (!imageSrc) return;

    if (farmerCredits !== null && farmerCredits <= 0) {
      alert(t.credits_exhausted_title);
      return;
    }

    setIsAnalyzing(true);
    setDiagnosis(null);
    setShowReport(false);

    try {
      const res = await fetch('/api/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          imageBase64: imageSrc,
          cropName: cropInput.trim(),
        }),
      });

      const data: DiagnosisResult = await res.json();
      setDiagnosis(data);

      if (data.is_leaf && farmerCredits !== null && farmerCredits > 0 && farmerDif) {
        // Decrement credit on successful leaf diagnosis
        const decRes = await fetch('/api/farmer/decrement', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ dif_code: farmerDif }),
        });
        const decData = await decRes.json();
        if (decData.credits !== undefined) {
          setFarmerCredits(decData.credits);
          localStorage.setItem('croplens_credits', String(decData.credits));
        }
      }
    } catch (err) {
      console.error('Diagnosis failed:', err);
      alert('Network error while analyzing leaf. Please retry.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSubmitReport = async () => {
    if (!farmerName.trim()) {
      setReportErrorMsg(t.farmer_name_req);
      return;
    }
    if (!reportCoords) {
      setReportErrorMsg(t.no_polygon_warning);
      return;
    }

    setReportErrorMsg(null);
    setReportSuccessMsg(null);
    setIsSubmittingReport(true);

    try {
      // Water check
      const waterCheck = await fetch(`/api/check-water?lat=${reportCoords.lat}&lng=${reportCoords.lng}`);
      const waterData = await waterCheck.json();
      if (waterData.isWater) {
        setReportErrorMsg(t.water_location_error);
        setIsSubmittingReport(false);
        return;
      }

      const res = await fetch('/api/reports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disease: diagnosis?.disease || 'Suspected Crop Disease',
          crop: diagnosis?.crop || cropInput || 'General Crop',
          confidence: diagnosis?.confidence || 95,
          farmer_name: farmerName.trim(),
          farmer_dif: farmerDif || 'DEMO',
          center_lat: reportCoords.lat,
          center_lng: reportCoords.lng,
          notes: reportNotes.trim() || undefined,
          language: lang,
        }),
      });

      const data = await res.json();
      if (res.ok && data.success) {
        setReportSuccessMsg(t.report_success);
        setRecentReports((prev) => [data.report, ...prev]);
        setTimeout(() => {
          setShowReport(false);
          setReportSuccessMsg(null);
        }, 2200);
      } else {
        setReportErrorMsg(data.error || t.report_error);
      }
    } catch (err) {
      setReportErrorMsg(t.report_error);
    } finally {
      setIsSubmittingReport(false);
    }
  };

  // Optional Closing Announcement View
  if (showClosingPage) {
    return (
      <div className="min-h-screen bg-[#0F172A] text-slate-200 flex flex-col items-center justify-center p-4">
        <div className="max-w-[680px] w-full bg-[#1E293B] border border-[#84A98C]/30 rounded-2xl p-8 shadow-2xl text-center space-y-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[#84A98C]/15 border border-[#84A98C]/30 text-3xl">
            🌱
          </div>
          <div className="text-xs uppercase tracking-widest font-bold text-[#84A98C]">AGRIFUSION</div>
          <h1 className="text-3xl font-extrabold text-white">A New Chapter for AgriFusion</h1>
          <p className="text-slate-400 text-sm">Reflecting on our journey with DizMatrix, SenseOrbit, CropLens, and Quallis.</p>
          <div className="flex flex-wrap justify-center gap-2">
            {['DizMatrix', 'SenseOrbit', 'CropLens', 'Quallis'].map((p) => (
              <span key={p} className="px-3.5 py-1 rounded-full text-xs bg-slate-800 border border-slate-700 text-slate-300">
                {p}
              </span>
            ))}
          </div>
          <div className="h-px bg-gradient-to-r from-transparent via-[#84A98C]/30 to-transparent my-4" />
          <div className="text-left bg-[#0F172A]/60 border border-white/5 rounded-xl p-6 space-y-4">
            <h2 className="text-[#D4AF37] font-semibold text-lg">Stepping back to evaluate the future.</h2>
            <p className="text-slate-400 text-sm leading-relaxed">
              As the agricultural landscape evolves, we have made the strategic decision to pause operational activities across the AgriFusion ecosystem, including DizMatrix, SenseOrbit, CropLens, and Quallis.
            </p>
            <p className="text-slate-400 text-sm leading-relaxed">
              AgriFusion remains committed to thoughtful innovation, and we look forward to exploring new opportunities when the timing and resources align.
            </p>
          </div>
          <div className="pt-2 border-t border-slate-800 text-xs text-slate-500">
            <button
              onClick={() => setShowClosingPage(false)}
              className="text-[#84A98C] hover:text-[#D4AF37] font-semibold underline underline-offset-4"
            >
              ← Back to CropLens Application
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0F172A] text-slate-100 flex flex-col items-center">
      <main className="w-full max-w-[740px] px-4 py-6 space-y-5">
        {/* Header & Language selector */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3 border-b border-slate-800">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">
              {t.app_title}
            </h1>
            <p className="text-xs sm:text-sm text-slate-400">
              <span className="text-emerald-400 font-medium">{t.app_subtitle}</span> · {t.tagline}
            </p>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto bg-slate-800/80 p-1 rounded-xl border border-slate-700/60">
            <span className="text-xs text-slate-400 px-2 font-medium">🌐</span>
            <button
              type="button"
              onClick={() => { setLang('en'); setAdviceLang('en'); }}
              className={`px-3 py-1 text-xs rounded-lg font-semibold transition-all ${
                lang === 'en' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-300 hover:text-white'
              }`}
            >
              English
            </button>
            <button
              type="button"
              onClick={() => { setLang('hi'); setAdviceLang('hi'); }}
              className={`px-3 py-1 text-xs rounded-lg font-semibold transition-all ${
                lang === 'hi' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-300 hover:text-white'
              }`}
            >
              हिंदी
            </button>
          </div>
        </div>

        {/* SIGN-IN GATE */}
        {!farmerDif ? (
          <div className="cl-signin-wrap space-y-4">
            <div className="text-3xl">🌾</div>
            <div className="space-y-1">
              <h2 className="text-xl font-bold text-white">{t.signin_title}</h2>
              <p className="text-xs text-slate-400">{t.signin_subtitle}</p>
            </div>

            <div className="max-w-xs mx-auto space-y-3">
              <div>
                <label className="block text-left text-xs font-semibold text-slate-300 mb-1">
                  {t.dif_label}
                </label>
                <input
                  type="text"
                  maxLength={4}
                  value={difInput}
                  onChange={(e) => setDifInput(e.target.value.toUpperCase())}
                  placeholder={t.dif_placeholder}
                  className="w-full bg-slate-900 border border-emerald-500/30 rounded-xl px-4 py-2.5 text-center text-lg font-mono font-bold tracking-widest text-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 uppercase placeholder:text-slate-600"
                />
                <span className="block text-left text-[11px] text-slate-400 mt-1">{t.dif_help}</span>
              </div>

              {difError && (
                <div className="text-xs text-rose-400 bg-rose-950/40 border border-rose-500/30 p-2.5 rounded-lg text-left">
                  {difError}
                </div>
              )}

              <button
                type="button"
                onClick={() => handleSignIn()}
                disabled={isSigningIn}
                className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-emerald-950/40 disabled:opacity-50"
              >
                {isSigningIn ? 'Verifying...' : t.signin_button}
              </button>

              {/* Demo DIF hints */}
              <div className="pt-2 text-left">
                <span className="text-[11px] text-slate-400 block mb-1.5 font-medium">Quick Demo Access:</span>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { code: 'AB12', label: 'AB12 (10 Scans)' },
                    { code: 'CD34', label: 'CD34 (5 Scans)' },
                    { code: 'EF56', label: 'EF56 (25 Scans)' },
                  ].map((demo) => (
                    <button
                      key={demo.code}
                      type="button"
                      onClick={() => handleSignIn(demo.code)}
                      className="text-[11px] bg-slate-800/90 hover:bg-slate-700 border border-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-lg transition-colors"
                    >
                      {demo.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800/60 flex items-center justify-center">
              <a
                href="https://cropradar.vercel.app"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1.5 text-xs text-emerald-400 hover:text-emerald-300 underline underline-offset-4"
              >
                <span>Live CropRadar Community Outbreak Map</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        ) : (
          /* SIGNED-IN USER BAR */
          <div className="space-y-4">
            <div className="flex items-center justify-between bg-slate-900/80 border border-slate-800 p-2.5 sm:p-3 rounded-xl gap-2">
              <div className="flex items-center gap-2">
                <span className="cl-badge text-xs">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  {t.signed_in_as}: <span className="font-mono">{farmerDif}</span>
                </span>
              </div>

              <div className="flex items-center gap-2">
                {farmerCredits !== null && (
                  <div
                    className={`text-xs px-3 py-1 rounded-lg font-bold text-white shadow-sm flex items-center gap-1 ${
                      farmerCredits > 5 ? 'bg-emerald-600' : farmerCredits > 2 ? 'bg-amber-600' : 'bg-rose-600'
                    }`}
                  >
                    <span>🔬</span>
                    <span>{t.credits_label}: {farmerCredits}</span>
                  </div>
                )}

                <button
                  type="button"
                  onClick={handleSignOut}
                  className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-rose-400 transition-colors"
                  title={t.signout}
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Credits Exhausted Alert */}
            {farmerCredits !== null && farmerCredits <= 0 && (
              <div className="cl-card-danger flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <h4 className="font-bold text-sm text-rose-300">{t.credits_exhausted_title}</h4>
                  <p className="text-xs text-slate-300">
                    {t.credits_exhausted_body}{' '}
                    <a
                      href="https://agrifusion-web.vercel.app"
                      target="_blank"
                      rel="noreferrer"
                      className="font-bold underline text-white"
                    >
                      agrifusion-web.vercel.app
                    </a>
                  </p>
                </div>
              </div>
            )}

            {/* INSTRUCTIONS CARD */}
            <div className="cl-card space-y-2">
              <h3 className="font-bold text-sm text-emerald-300 flex items-center gap-2">
                <span>{t.instructions_title}</span>
              </h3>
              <ul className="text-xs text-slate-300 space-y-1.5 list-disc pl-4 leading-relaxed">
                {t.instructions.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                ))}
              </ul>
            </div>

            {/* CAMERA & IMAGE UPLOAD SECTION */}
            <div className="space-y-3">
              {showCamera ? (
                <CameraCapture
                  onCapture={handleCameraCapture}
                  onClose={() => setShowCamera(false)}
                  t={{
                    take_photo_btn: t.take_photo_btn,
                    retake_photo_btn: t.retake_photo_btn,
                    close_camera: t.close_camera,
                  }}
                />
              ) : (
                <div className="flex flex-col sm:flex-row gap-2.5">
                  <label className="flex-1 cursor-pointer py-3 px-4 rounded-xl bg-slate-900 border border-slate-700 hover:border-emerald-500/50 flex items-center justify-center gap-2 text-sm font-semibold text-slate-200 transition-all hover:bg-slate-800/80 shadow-sm">
                    <Upload className="w-4 h-4 text-emerald-400" />
                    <span>{t.upload_label}</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>

                  <button
                    type="button"
                    onClick={() => setShowCamera(true)}
                    className="py-3 px-5 rounded-xl bg-emerald-600/20 border border-emerald-500/40 hover:bg-emerald-600/30 flex items-center justify-center gap-2 text-sm font-semibold text-emerald-300 transition-all shadow-sm"
                  >
                    <Camera className="w-4 h-4" />
                    <span>{t.open_camera}</span>
                  </button>
                </div>
              )}

              {/* Uploaded / Captured Image Preview */}
              {imageSrc && (
                <div className="space-y-4 pt-2">
                  <div className="relative rounded-2xl overflow-hidden border border-slate-700 bg-black/40 p-2">
                    <div className="text-xs text-slate-400 mb-1.5 flex items-center justify-between px-1">
                      <span>📸 {t.uploaded_caption}</span>
                      <button
                        type="button"
                        onClick={() => {
                          setImageSrc(null);
                          setDiagnosis(null);
                          setShowReport(false);
                        }}
                        className="text-xs text-slate-400 hover:text-rose-400 transition-colors"
                      >
                        Remove
                      </button>
                    </div>
                    <img
                      src={imageSrc}
                      alt="Crop leaf"
                      className="w-full max-h-[380px] object-contain rounded-xl mx-auto"
                    />
                  </div>

                  {/* Crop name selection step */}
                  {!diagnosis && (
                    <div className="bg-slate-900/90 border border-emerald-500/30 p-4 rounded-2xl space-y-3 shadow-lg">
                      <div className="space-y-1">
                        <label className="block text-sm font-bold text-white flex items-center gap-2">
                          <Leaf className="w-4 h-4 text-emerald-400" />
                          <span>{t.crop_prompt}</span>
                        </label>
                        <p className="text-xs text-slate-400">
                          {lang === 'en'
                            ? 'Identify your crop for higher botanical precision.'
                            : 'उच्च सटीकता के लिए अपनी फसल निर्दिष्ट करें।'}
                        </p>
                      </div>

                      {/* Common crop pills */}
                      <div className="flex flex-wrap gap-1.5">
                        {['Tomato', 'Potato', 'Apple', 'Corn', 'Grape', 'Rice', 'Wheat', 'Peach', 'Chili'].map((cp) => (
                          <button
                            key={cp}
                            type="button"
                            onClick={() => setCropInput(cp)}
                            className={`text-xs px-2.5 py-1 rounded-lg border transition-all ${
                              cropInput === cp
                                ? 'bg-emerald-600 text-white border-emerald-500'
                                : 'bg-slate-800 text-slate-300 border-slate-700 hover:border-emerald-500/40'
                            }`}
                          >
                            {cp}
                          </button>
                        ))}
                      </div>

                      <div className="flex gap-2 pt-1">
                        <input
                          type="text"
                          value={cropInput}
                          onChange={(e) => setCropInput(e.target.value)}
                          placeholder={t.crop_placeholder}
                          className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        />
                        <button
                          type="button"
                          onClick={handleAnalyze}
                          disabled={isAnalyzing || !cropInput.trim()}
                          className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl text-sm flex items-center gap-2 transition-all shadow-lg shadow-emerald-950/40 disabled:opacity-50"
                        >
                          {isAnalyzing ? (
                            <>
                              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                              <span>{t.diagnosing}</span>
                            </>
                          ) : (
                            <>
                              <span>{t.crop_analyze_btn}</span>
                              <ArrowRight className="w-4 h-4" />
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* DIAGNOSIS RESULTS */}
            {diagnosis && (
              <div className="space-y-4 pt-2 animate-fadeIn">
                {!diagnosis.is_leaf ? (
                  <div className="cl-card-danger space-y-2">
                    <div className="flex items-center gap-2 text-rose-400 font-bold">
                      <AlertTriangle className="w-5 h-5" />
                      <span>{t.not_a_leaf}</span>
                    </div>
                    <p className="text-xs text-slate-300">
                      The AI model did not detect a clear crop leaf. Please photograph a single leaf on a plain daylight background.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Diagnosis Headline Banner */}
                    <div className="bg-slate-900/90 border border-emerald-500/40 rounded-2xl p-4 sm:p-5 space-y-3 shadow-xl">
                      <div className="flex items-center justify-between">
                        <span className="text-xs uppercase font-bold tracking-wider text-emerald-400 flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5" />
                          {t.diagnosis_title}
                        </span>
                        <span className="text-xs text-slate-400">
                          {t.confidence_label}: <span className="text-white font-semibold">{diagnosis.confidence.toFixed(1)}%</span>
                        </span>
                      </div>

                      <div className="cl-disease-name text-white">
                        {diagnosis.crop ? `${diagnosis.crop} — ` : ''}
                        <span className="text-emerald-400">{diagnosis.disease}</span>
                      </div>

                      {/* Confidence Bar */}
                      <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-emerald-500 to-teal-400 h-2.5 rounded-full transition-all duration-700"
                          style={{ width: `${Math.min(100, diagnosis.confidence)}%` }}
                        />
                      </div>
                    </div>

                    {/* TREATMENT & CARE ADVICE */}
                    <div className="cl-treatment-section space-y-4">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                        <h4 className="font-bold text-base text-emerald-300 flex items-center gap-2">
                          <span>{t.treatment_title}</span>
                        </h4>

                        {/* Advice language switcher */}
                        <div className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-700/80 self-start sm:self-auto">
                          <span className="text-[11px] text-slate-400 px-2">{t.modal_lang_label}:</span>
                          <button
                            type="button"
                            onClick={() => setAdviceLang('en')}
                            className={`px-2.5 py-0.5 text-xs rounded-lg font-medium transition-all ${
                              adviceLang === 'en' ? 'bg-emerald-600 text-white font-bold' : 'text-slate-300 hover:text-white'
                            }`}
                          >
                            English
                          </button>
                          <button
                            type="button"
                            onClick={() => setAdviceLang('hi')}
                            className={`px-2.5 py-0.5 text-xs rounded-lg font-medium transition-all ${
                              adviceLang === 'hi' ? 'bg-emerald-600 text-white font-bold' : 'text-slate-300 hover:text-white'
                            }`}
                          >
                            हिंदी
                          </button>
                        </div>
                      </div>

                      {/* Structured Details if available */}
                      {diagnosis.info && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
                            <span className="text-emerald-400 font-bold block mb-1">{t.severity_label}:</span>
                            <span className="text-slate-200">
                              {adviceLang === 'en' ? diagnosis.info.severity_en : diagnosis.info.severity_hi}
                            </span>
                          </div>
                          <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
                            <span className="text-emerald-400 font-bold block mb-1">{t.symptoms_label}:</span>
                            <span className="text-slate-200">
                              {adviceLang === 'en' ? diagnosis.info.symptoms_en : diagnosis.info.symptoms_hi}
                            </span>
                          </div>
                          <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
                            <span className="text-emerald-400 font-bold block mb-1">{t.prevention_label}:</span>
                            <span className="text-slate-200">
                              {adviceLang === 'en' ? diagnosis.info.prevention_en : diagnosis.info.prevention_hi}
                            </span>
                          </div>
                          <div className="bg-slate-900/70 p-3 rounded-xl border border-slate-800">
                            <span className="text-emerald-400 font-bold block mb-1">{t.treatment_label}:</span>
                            <span className="text-slate-200">
                              {adviceLang === 'en' ? diagnosis.info.treatment_en : diagnosis.info.treatment_hi}
                            </span>
                          </div>
                        </div>
                      )}

                      {/* 4 AI Treatment Points */}
                      <div className="space-y-2 pt-1">
                        <span className="text-xs font-bold text-slate-300 block">
                          {t.gemini_treatment_label}:
                        </span>
                        {(adviceLang === 'hi' ? diagnosis.treatment_hi : diagnosis.treatment_en)?.map((point, i) => (
                          <div key={i} className="cl-treatment-box text-xs sm:text-sm">
                            • {point}
                          </div>
                        ))}
                      </div>

                      <p className="text-[11px] text-slate-500 italic pt-1">{t.disclaimer}</p>
                    </div>

                    {/* Report Outbreak Button (if not healthy) */}
                    {diagnosis.disease.toLowerCase() !== 'healthy' && (
                      <div className="pt-2">
                        <button
                          type="button"
                          onClick={() => setShowReport(!showReport)}
                          className="w-full py-3 px-4 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 text-amber-300 font-bold text-sm flex items-center justify-center gap-2 transition-all shadow-md"
                        >
                          <MapPin className="w-4 h-4 text-amber-400" />
                          <span>{showReport ? t.hide_report : t.report_button}</span>
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* OUTBREAK REPORTING FORM & INTERACTIVE MAP */}
                {showReport && (
                  <div className="cl-report-section space-y-4 animate-fadeIn">
                    <div className="flex items-center justify-between border-b border-amber-500/20 pb-2">
                      <div className="space-y-0.5">
                        <h4 className="font-bold text-sm sm:text-base text-amber-300 flex items-center gap-1.5">
                          <span>🚩 {t.report_dialog_title}</span>
                        </h4>
                        <p className="text-xs text-slate-300">{t.report_instructions}</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setShowReport(false)}
                        className="text-slate-400 hover:text-slate-200"
                        title={t.hide_report}
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>

                    {/* Interactive Leaflet Map */}
                    <ReportMap
                      onLocationSelect={(lat, lng) => setReportCoords({ lat, lng })}
                      selectedLocation={reportCoords}
                      t={{
                        locate_me: t.locate_me,
                        locate_me_help: t.locate_me_help,
                        map_caption: t.map_caption,
                      }}
                    />

                    {/* Farmer Form Fields */}
                    <div className="space-y-3 pt-1">
                      <div>
                        <label className="block text-xs font-semibold text-slate-300 mb-1">
                          {t.farmer_name_label} <span className="text-rose-400">*</span>
                        </label>
                        <input
                          type="text"
                          value={farmerName}
                          onChange={(e) => setFarmerName(e.target.value)}
                          placeholder="e.g. Ramesh Singh"
                          className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-slate-300 mb-1">
                          {t.notes_label}
                        </label>
                        <textarea
                          rows={2}
                          value={reportNotes}
                          onChange={(e) => setReportNotes(e.target.value)}
                          placeholder="Describe symptoms, acreage affected, or weather conditions..."
                          className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-amber-500"
                        />
                      </div>

                      {reportErrorMsg && (
                        <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-300 text-xs flex items-center gap-2">
                          <AlertTriangle className="w-4 h-4 shrink-0" />
                          <span>{reportErrorMsg}</span>
                        </div>
                      )}

                      {reportSuccessMsg && (
                        <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 text-xs">
                          {reportSuccessMsg}
                        </div>
                      )}

                      <div className="flex gap-2 pt-1">
                        <button
                          type="button"
                          onClick={() => setShowReport(false)}
                          className="flex-1 py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-xl text-sm transition-colors"
                        >
                          {t.hide_report}
                        </button>
                        <button
                          type="button"
                          onClick={handleSubmitReport}
                          disabled={isSubmittingReport}
                          className="flex-1 py-2.5 px-4 bg-amber-600 hover:bg-amber-500 text-white font-bold rounded-xl text-sm flex items-center justify-center gap-2 transition-all shadow-md disabled:opacity-50"
                        >
                          <Send className="w-4 h-4" />
                          <span>{isSubmittingReport ? t.submitting : t.submit_report}</span>
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* RECENT OUTBREAKS ACCORDION */}
            <div className="pt-4 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setShowRecentReports(!showRecentReports)}
                className="w-full flex items-center justify-between text-xs text-slate-400 hover:text-emerald-400 font-semibold transition-colors py-1"
              >
                <span>🌐 {t.view_reports} ({recentReports.length})</span>
                <span>{showRecentReports ? '▲ Hide' : '▼ Show'}</span>
              </button>

              {showRecentReports && (
                <div className="mt-3 space-y-2 max-h-[300px] overflow-y-auto pr-1">
                  {recentReports.length === 0 ? (
                    <div className="text-xs text-slate-500 p-3 text-center">No reports recorded yet.</div>
                  ) : (
                    recentReports.map((rep) => (
                      <div
                        key={rep.id}
                        className="bg-slate-900/60 border border-slate-800 rounded-xl p-3 text-xs space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-amber-400">
                            {rep.crop} — {rep.disease}
                          </span>
                          <span className="text-[11px] text-slate-500 font-mono">
                            {new Date(rep.reported_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="text-slate-400 flex items-center gap-2 text-[11px]">
                          <span>Farmer: {rep.farmer_name}</span>
                          <span>•</span>
                          <span>Coords: {rep.center_lat.toFixed(2)}°, {rep.center_lng.toFixed(2)}°</span>
                        </div>
                        {rep.notes && <p className="text-slate-300 italic pt-0.5">"{rep.notes}"</p>}
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* FOOTER */}
        <footer className="pt-6 pb-4 border-t border-slate-800/80 text-center space-y-2 text-xs text-slate-500">
          <div>
            🌱 CropLens AI Crop Doctor · Powered by Gemini Multimodal Vision & Plant Pathology Knowledge Base
          </div>
          <div>
            <button
              onClick={() => setShowClosingPage(true)}
              className="text-slate-500 hover:text-slate-400 underline underline-offset-2"
            >
              AgriFusion Ecosystem Statement
            </button>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
