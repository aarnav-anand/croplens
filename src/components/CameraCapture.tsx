import React, { useRef, useState, useEffect } from 'react';
import { Camera, RefreshCw, X, Check } from 'lucide-react';

interface CameraCaptureProps {
  onCapture: (base64: string) => void;
  onClose: () => void;
  t: {
    take_photo_btn: string;
    retake_photo_btn: string;
    close_camera: string;
  };
}

export const CameraCapture: React.FC<CameraCaptureProps> = ({ onCapture, onClose, t }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [capturedImg, setCapturedImg] = useState<string | null>(null);
  const [facingMode, setFacingMode] = useState<'environment' | 'user'>('environment');
  const [error, setError] = useState<string | null>(null);

  const startStream = async () => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: facingMode }, width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.warn('Camera access error:', err);
      // Fallback to any video device
      try {
        const fallbackStream = await navigator.mediaDevices.getUserMedia({ video: true });
        streamRef.current = fallbackStream;
        if (videoRef.current) {
          videoRef.current.srcObject = fallbackStream;
        }
      } catch (fallbackErr) {
        setError('Unable to access camera. Please allow camera permissions or upload an image file instead.');
      }
    }
  };

  useEffect(() => {
    startStream();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, [facingMode]);

  const snapPhoto = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
      setCapturedImg(dataUrl);
    }
  };

  const confirmPhoto = () => {
    if (capturedImg) {
      onCapture(capturedImg);
    }
  };

  const retakePhoto = () => {
    setCapturedImg(null);
    startStream();
  };

  const flipCamera = () => {
    setFacingMode((prev) => (prev === 'environment' ? 'user' : 'environment'));
  };

  return (
    <div className="relative rounded-2xl overflow-hidden border border-emerald-500/30 bg-slate-950 p-3 shadow-2xl">
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800">
        <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
          <Camera className="w-4 h-4" />
          <span>Live Leaf Camera</span>
        </div>
        <div className="flex items-center gap-2">
          {!capturedImg && (
            <button
              type="button"
              onClick={flipCamera}
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              title="Switch camera"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
            title={t.close_camera}
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {error ? (
        <div className="p-6 text-center text-amber-400 text-sm">{error}</div>
      ) : (
        <div className="relative aspect-[4/3] max-h-[380px] w-full bg-black rounded-xl overflow-hidden flex items-center justify-center">
          {capturedImg ? (
            <img src={capturedImg} alt="Captured preview" className="w-full h-full object-contain" />
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
          )}

          {/* Guide Overlay */}
          {!capturedImg && (
            <div className="absolute inset-8 border-2 border-dashed border-emerald-400/40 rounded-2xl pointer-events-none flex items-center justify-center">
              <span className="text-xs bg-slate-900/80 text-emerald-300 px-3 py-1 rounded-full border border-emerald-500/20">
                Center leaf inside frame
              </span>
            </div>
          )}
        </div>
      )}

      <div className="mt-3 flex gap-2">
        {capturedImg ? (
          <>
            <button
              type="button"
              onClick={retakePhoto}
              className="flex-1 py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium rounded-xl flex items-center justify-center gap-2 transition-colors text-sm"
            >
              <RefreshCw className="w-4 h-4" />
              {t.retake_photo_btn}
            </button>
            <button
              type="button"
              onClick={confirmPhoto}
              className="flex-1 py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/30 transition-colors text-sm"
            >
              <Check className="w-4 h-4" />
              {t.take_photo_btn}
            </button>
          </>
        ) : (
          <button
            type="button"
            onClick={snapPhoto}
            className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/30 transition-colors text-sm"
          >
            <Camera className="w-4 h-4" />
            {t.take_photo_btn}
          </button>
        )}
      </div>
    </div>
  );
};
