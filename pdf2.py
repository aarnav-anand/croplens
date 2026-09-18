from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import HexColor, white, black
import re

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY    = HexColor("#0B1829")
TEAL    = HexColor("#1DB88E")
SLATE   = HexColor("#F0F4F8")
DARKGRAY= HexColor("#2C3E50")
AMBER   = HexColor("#B7791F")
AMBERBG = HexColor("#FFFBEB")
AMBERBDR= HexColor("#F59E0B")
GREEN_DARK = HexColor("#065F46")
GREEN_BG   = HexColor("#EBF8F3")
GREEN_TEAL = HexColor("#1DB88E")
LIGHTGRAY  = HexColor("#888888")
W = A4[0]

# ── Custom Flowables ──────────────────────────────────────────────────────────
class SectionBanner(Flowable):
    def __init__(self, text, width=None):
        super().__init__()
        self.text = text
        self.bw = width or (A4[0] - 3.6*cm)
        self.height = 22

    def wrap(self, availW, availH):
        return self.bw, self.height + 16

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.bw, self.height, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(12, 5, self.text)


class DisclaimerBox(Flowable):
    def __init__(self, width=None):
        super().__init__()
        self.bw = width or (A4[0] - 3.6*cm)
        self.text = (
            "⚠  PROTOTYPE NOTICE:  SonoSense is a research prototype. It is not a certified "
            "medical device and has not received regulatory clearance from CDSCO, FDA, or CE. "
            "Outputs must not be used for clinical diagnosis or patient care decisions."
        )
        self._height = None

    def _calc_height(self):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        max_w = self.bw - 24
        words = self.text.split()
        line_h = 13
        lines = 1
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Helvetica", 8.5) <= max_w:
                line = test
            else:
                lines += 1
                line = w
        return lines * line_h + 20

    def wrap(self, availW, availH):
        h = self._calc_height()
        self._height = h
        return self.bw, h

    def draw(self):
        c = self.canv
        h = self._height or self._calc_height()
        c.setFillColor(AMBERBG)
        c.setStrokeColor(AMBERBDR)
        c.setLineWidth(1)
        c.rect(0, 0, self.bw, h, fill=1, stroke=1)
        # left accent bar
        c.setFillColor(AMBERBDR)
        c.rect(0, 0, 5, h, fill=1, stroke=0)
        # text
        c.setFillColor(AMBER)
        c.setFont("Helvetica-Bold", 8.5)
        x, y = 14, h - 14
        label = "PROTOTYPE NOTICE:  "
        c.drawString(x, y, label)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        lw = stringWidth(label, "Helvetica-Bold", 8.5)
        rest = ("SonoSense is a research prototype. It is not a certified "
                "medical device and has not received regulatory clearance from CDSCO, FDA, or CE. "
                "Outputs must not be used for clinical diagnosis or patient care decisions.")
        c.setFillColor(HexColor("#92400E"))
        c.setFont("Helvetica", 8.5)
        max_w = self.bw - 24
        words = rest.split()
        line = ""
        first = True
        cx = x + lw if first else x
        for w in words:
            test = (line + " " + w).strip()
            sw = stringWidth(test, "Helvetica", 8.5)
            avail = (max_w - lw) if first else max_w
            if sw <= avail:
                line = test
            else:
                c.drawString(cx if first else x, y, line)
                first = False
                y -= 13
                cx = x
                line = w
            if first and stringWidth(line, "Helvetica", 8.5) > max_w - lw:
                c.drawString(cx, y, line)
                first = False
                y -= 13
                line = ""
        if line:
            c.drawString(cx if first else x, y, line)


class InfoBox(Flowable):
    def __init__(self, label, text, width=None):
        super().__init__()
        self.label = label
        self.text = text
        self.bw = width or (A4[0] - 3.6*cm)
        self._height = None

    def _calc_height(self):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        max_w = self.bw - 28
        words = self.text.split()
        lines = 1
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Helvetica", 8.5) <= max_w:
                line = test
            else:
                lines += 1
                line = w
        return lines * 12 + 36

    def wrap(self, availW, availH):
        h = self._calc_height()
        self._height = h
        return self.bw, h

    def draw(self):
        c = self.canv
        h = self._height or self._calc_height()
        c.setFillColor(GREEN_BG)
        c.setStrokeColor(TEAL)
        c.setLineWidth(1)
        c.rect(0, 0, self.bw, h, fill=1, stroke=1)
        c.setFillColor(TEAL)
        c.rect(0, 0, 5, h, fill=1, stroke=0)
        c.setFillColor(GREEN_DARK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(14, h - 14, self.label)
        c.setFont("Helvetica", 8.5)
        from reportlab.pdfbase.pdfmetrics import stringWidth
        max_w = self.bw - 28
        words = self.text.split()
        line = ""
        y = h - 28
        for w in words:
            test = (line + " " + w).strip()
            if stringWidth(test, "Helvetica", 8.5) <= max_w:
                line = test
            else:
                c.drawString(14, y, line)
                y -= 12
                line = w
        if line:
            c.drawString(14, y, line)


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = getSampleStyleSheet()

    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=36, textColor=NAVY,
        spaceAfter=4, leading=40)
    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=18, textColor=TEAL,
        spaceAfter=4, leading=22)
    s['cover_italic'] = ParagraphStyle('cover_italic',
        fontName='Helvetica-Oblique', fontSize=12, textColor=HexColor("#555555"),
        spaceAfter=14, leading=16)
    s['cover_meta'] = ParagraphStyle('cover_meta',
        fontName='Helvetica', fontSize=10, textColor=HexColor("#555555"),
        spaceAfter=4, leading=13)

    s['h1'] = ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=15, textColor=NAVY,
        spaceBefore=18, spaceAfter=6, leading=19)
    s['h2'] = ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=12, textColor=NAVY,
        spaceBefore=12, spaceAfter=5, leading=15)
    s['h3'] = ParagraphStyle('h3',
        fontName='Helvetica-BoldOblique', fontSize=10.5, textColor=HexColor("#1A6B52"),
        spaceBefore=8, spaceAfter=4, leading=13)
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=DARKGRAY,
        spaceBefore=3, spaceAfter=6, leading=13)
    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, textColor=DARKGRAY,
        spaceBefore=2, spaceAfter=4, leading=13,
        leftIndent=14, firstLineIndent=0)
    s['subbullet'] = ParagraphStyle('subbullet',
        fontName='Helvetica', fontSize=9, textColor=HexColor("#555555"),
        spaceBefore=2, spaceAfter=3, leading=12,
        leftIndent=28, firstLineIndent=0)
    s['disclaimer_foot'] = ParagraphStyle('disclaimer_foot',
        fontName='Helvetica-Oblique', fontSize=8, textColor=LIGHTGRAY,
        spaceBefore=4, spaceAfter=0, leading=11)
    return s

ST = make_styles()

def h1(t): return Paragraph(t, ST['h1'])
def h2(t): return Paragraph(t, ST['h2'])
def h3(t): return Paragraph(t, ST['h3'])
def body(t): return Paragraph(t, ST['body'])
def bul(t, bold_prefix=None):
    if bold_prefix:
        t = f'<b>{bold_prefix}</b>{t}'
    return Paragraph(f'• {t}', ST['bullet'])
def subbul(t, bold_prefix=None):
    if bold_prefix:
        t = f'<b>{bold_prefix}</b>{t}'
    return Paragraph(f'  ◦ {t}', ST['subbullet'])
def sp(h=6): return Spacer(1, h)

def make_table(headers, rows, col_widths, usable_w=None):
    if usable_w is None:
        usable_w = A4[0] - 3.6*cm
    total = sum(col_widths)
    scaled = [w / total * usable_w for w in col_widths]

    def cell(txt, bold=False, bg=None):
        fs = 8.5
        fn = 'Helvetica-Bold' if bold else 'Helvetica'
        col = white if bold else DARKGRAY
        return Paragraph(f'<font name="{fn}" size="{fs}" color="#{col.hexval()[2:] if bold else "2C3E50"}">{txt}</font>',
                         ParagraphStyle('tc', fontName=fn, fontSize=fs,
                                        textColor=white if bold else DARKGRAY,
                                        leading=11, spaceBefore=0, spaceAfter=0))

    data = [[cell(h, bold=True) for h in headers]]
    for ri, row in enumerate(rows):
        data.append([cell(c) for c in row])

    style = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, SLATE]),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor("#D0D8E4")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]
    return Table(data, colWidths=scaled, style=TableStyle(style), repeatRows=1)


# ── Page template with header/footer ─────────────────────────────────────────
def make_doc(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.0*cm, bottomMargin=2.0*cm,
        title="SonoSense Technical Architecture",
        author="Aarnav Anand",
    )
    return doc

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        # Header bar
        canvas.setFillColor(NAVY)
        canvas.rect(1.8*cm, h - 1.5*cm, w - 3.6*cm, 1, fill=1, stroke=0)
        canvas.setFillColor(NAVY)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(1.8*cm, h - 1.35*cm, "SonoSense")
        canvas.setFillColor(TEAL)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(1.8*cm + 52, h - 1.35*cm, "Technical Architecture")
        canvas.setFillColor(LIGHTGRAY)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(w - 1.8*cm, h - 1.35*cm, f"Page {doc.page}")
        # Footer
        canvas.setFillColor(HexColor("#D0D8E4"))
        canvas.rect(1.8*cm, 1.5*cm, w - 3.6*cm, 0.5, fill=1, stroke=0)
        canvas.setFillColor(LIGHTGRAY)
        canvas.setFont("Helvetica-Oblique", 7)
        canvas.drawString(1.8*cm, 1.2*cm,
            "Research prototype — not a certified medical device — not for clinical use")
        canvas.drawRightString(w - 1.8*cm, 1.2*cm, "Aarnav Anand · aarnav.anandkumar@gmail.com")
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    usable_w = A4[0] - 3.6*cm

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────
    story += [
        sp(30),
        Paragraph("SonoSense", ST['cover_title']),
        Paragraph("Detailed Technical Architecture", ST['cover_sub']),
        Paragraph("AI-Powered Liver Fibrosis Staging from Routine Abdominal Ultrasound",
                  ST['cover_italic']),
        sp(8),
        HRFlowable(width=usable_w, thickness=2, color=TEAL, spaceAfter=16),
        Paragraph('<b>Version:</b>  0.1 — Pre-launch Research Draft', ST['cover_meta']),
        Paragraph('<b>Expected Prototype Launch:</b>  <font color="#1DB88E"><b>Early November 2026</b></font>',
                  ST['cover_meta']),
        Paragraph('<b>Team:</b>  Aarnav Anand', ST['cover_meta']),
        Paragraph('<b>Contact:</b>  <font color="#1DB88E">aarnav.anandkumar@gmail.com</font>',
                  ST['cover_meta']),
        sp(28),
        DisclaimerBox(width=usable_w),
        PageBreak(),
    ]

    # ── SECTION 1 ──────────────────────────────────────────────────────────
    story += [
        SectionBanner("01  SYSTEM OVERVIEW", width=usable_w), sp(6),
        h2("1.1  Purpose and Scope"),
        body("SonoSense is a multimodal deep learning system designed to automatically stage liver fibrosis from F0 to F4 using standard B-mode abdominal ultrasound images combined with routine clinical laboratory values. It targets the primary care and radiology settings where MASLD patients most commonly present, deploying within existing PACS workstation pipelines without requiring new hardware, specialist operators, or changes to patient workflows."),
        body("This document describes the complete technical architecture of SonoSense: the data pipeline, preprocessing stack, model architecture (segmentation branch + classification branch + fusion layer), explainability module, inference pipeline, deployment targets, and evaluation framework."),
        sp(6),
        h2("1.2  High-Level System Architecture"),
        body("SonoSense is structured as a five-layer system:"),
        bul("Data Ingestion & Preprocessing — DICOM handling, image normalisation, lab value parsing and imputation"),
        bul("Segmentation Branch — Attention U-Net for liver boundary delineation"),
        bul("Classification Branch — EfficientNet-B4 / ResNet50 ensemble CNN for fibrosis feature extraction"),
        bul("Multimodal Fusion Layer — Cross-attention fusion of image embeddings with clinical tabular features"),
        bul("Output & Explainability Layer — Calibrated classification head, Grad-CAM heatmap, SHAP feature attribution, structured report generation"),
        sp(8),
        make_table(
            ["Layer", "Component", "Primary Technology", "Output"],
            [
                ["1 — Ingestion", "DICOM parser + preprocessor", "pydicom, OpenCV", "Normalised PNG tensors"],
                ["2 — Segmentation", "Liver boundary U-Net", "Attention U-Net (EfficientNet encoder)", "Binary liver mask + ROI crop"],
                ["3 — Classification", "Fibrosis CNN encoder", "EfficientNet-B4 + ResNet50 ensemble", "2048-dim image embedding"],
                ["4 — Fusion", "Multimodal attention fusion", "Cross-attention + MLP tabular encoder", "Fused 512-dim representation"],
                ["5 — Output", "Calibrated head + explainability", "Softmax + temperature scaling + Grad-CAM + SHAP", "F0–F4 grade, heatmap, report"],
            ],
            [2200, 2400, 2600, 2880]
        ),
    ]

    # ── SECTION 2 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("02  DATA PIPELINE & PREPROCESSING", width=usable_w), sp(6),
        h2("2.1  Input Data Specification"),
        body("SonoSense accepts two data streams at inference time: the ultrasound image and a structured clinical metadata object containing laboratory values and patient demographics. Both streams are required; however, missing lab values are handled via learned imputation (see Section 2.3)."),
        h3("2.1.1  Imaging Input"),
        bul("Format: DICOM (.dcm) — converted internally to PNG for model processing"),
        bul("Modality: B-mode (2D grayscale) abdominal ultrasound"),
        bul("Required views: Right lobe subcostal view (primary); intercostal view (secondary, optional)"),
        bul("Frame selection: If a multi-frame DICOM cine clip is provided, a quality scoring model (sharpness + liver coverage heuristic) automatically selects the best 3 frames for ensemble averaging"),
        bul("Resolution: Accepted from 256×256 up to 1024×1024; internally resized to 512×512 before model ingestion"),
        bul("Machine vendor: Vendor-agnostic — trained on images from Siemens, GE, Philips, and Mindray machines to ensure cross-vendor generalisation"),
        sp(6),
        h3("2.1.2  Clinical Input (Tabular Stream)"),
        make_table(
            ["Variable", "Type", "Required?", "Clinical Rationale"],
            [
                ["AST (U/L)", "Continuous", "Yes", "Hepatocyte injury; AST/ALT ratio rises with fibrosis stage"],
                ["ALT (U/L)", "Continuous", "Yes", "Hepatocyte injury marker; part of FIB-4 formula"],
                ["Platelet count (x10^9/L)", "Continuous", "Yes", "Falls with portal hypertension; strongest single lab predictor"],
                ["Age (years)", "Continuous", "Yes", "Part of FIB-4; fibrosis risk increases with age"],
                ["GGT (U/L)", "Continuous", "Recommended", "Sensitive to both steatosis and fibrosis progression"],
                ["Albumin (g/dL)", "Continuous", "Recommended", "Drops in advanced fibrosis as synthetic function declines"],
                ["HbA1c (%)", "Continuous", "Optional", "Reflects metabolic dysfunction driving fibrosis"],
                ["BMI (kg/m2)", "Continuous", "Optional", "Strongest clinical predictor in gradient-boosted models"],
                ["ALP (U/L)", "Continuous", "Optional", "Cholestasis marker; useful for advanced disease"],
                ["Bilirubin (mg/dL)", "Continuous", "Optional", "Secondary signal for F3–F4 and cirrhosis"],
                ["Type 2 diabetes (Y/N)", "Binary", "Optional", "Independently doubles fibrosis risk"],
                ["Sex (M/F)", "Binary", "Optional", "Sex-specific progression patterns"],
            ],
            [2100, 1500, 1500, 4980]
        ),
        sp(10),
        h2("2.2  DICOM Ingestion Pipeline"),
        body("Raw DICOM files are parsed using pydicom. The pipeline performs the following steps in sequence:"),
        bul("Metadata extraction: Patient ID, study date, ultrasound machine vendor/model, and acquisition parameters are extracted and logged for audit trail"),
        bul("Pixel array extraction: The raw pixel array is extracted and converted to uint8 grayscale"),
        bul("Photometric interpretation check: MONOCHROME1 images are inverted; RGB images are converted to grayscale via luminosity weighting"),
        bul("Probe region detection: A heuristic crops out the on-screen annotation overlay using connected-component analysis on high-entropy border regions"),
        bul("Fan-mask removal: Ultrasound fan-shaped scanning region is isolated from background using Otsu thresholding; only the scan region is passed downstream"),
        sp(6),
        h2("2.3  Image Normalisation & Augmentation"),
        h3("2.3.1  Normalisation"),
        bul("CLAHE (Contrast Limited Adaptive Histogram Equalisation): Applied with clip limit 2.0, tile grid 8×8 — enhances echotexture visibility without amplifying noise"),
        bul("Z-score normalisation per image: Mean subtracted, divided by standard deviation — accounts for inter-machine gain differences"),
        bul("Resize to 512×512: Bicubic interpolation"),
        sp(4),
        h3("2.3.2  Training-Time Augmentation"),
        body("To address the limited size of ultrasound fibrosis datasets and improve generalisation across machine vendors:"),
        bul("Geometric: Random horizontal flip (p=0.5), random rotation ±15°, random elastic deformation (sigma=10, alpha=100)"),
        bul("Intensity: Random brightness/contrast jitter (±20%), random Gaussian noise (sigma in [0, 0.05]), random gamma correction (gamma in [0.8, 1.2])"),
        bul("Ultrasound-specific: Random speckle noise injection, random shadowing artifact simulation (vertical dark bands), random gain simulation"),
        bul("Mixup: Applied with alpha=0.2 between same-stage examples only — prevents boundary blur between adjacent stages"),
        sp(6),
        h2("2.4  Missing Lab Value Imputation"),
        body("At inference, it is common for one or more optional lab values to be absent. SonoSense handles this in two ways:"),
        bul("Median imputation (baseline): Missing values are replaced by the population median from the training cohort, stratified by age group and sex"),
        bul("Learned missingness mask (advanced): A binary missingness mask vector is concatenated to the tabular input tensor, allowing the MLP tabular encoder to learn imputation-aware representations — the model learns to down-weight imputed values implicitly"),
        body("The minimum viable input set is: one ultrasound image + AST + ALT + platelet count + age. All other features improve performance but are never required."),
    ]

    # ── SECTION 3 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("03  SEGMENTATION BRANCH — LIVER BOUNDARY DELINEATION", width=usable_w), sp(6),
        h2("3.1  Architecture: Attention U-Net with EfficientNet-B4 Encoder"),
        body("The segmentation branch produces a binary liver mask from the preprocessed ultrasound image. This mask serves two purposes: (1) it gates the classification branch to analyse only liver parenchyma, excluding surrounding tissue and artefacts; (2) it provides the spatial canvas onto which the Grad-CAM heatmap is projected for clinical display."),
        h3("3.1.1  Encoder"),
        bul("Backbone: EfficientNet-B4 pretrained on ImageNet, adapted for single-channel greyscale input by averaging the three-channel first-layer weights"),
        bul("Feature pyramid: Encoder produces feature maps at 5 spatial scales — 256×256, 128×128, 64×64, 32×32, 16×16 — passed to decoder via skip connections"),
        bul("Rationale: EfficientNet-B4 achieves highest sensitivity (0.85) among CNN backbones tested on ultrasound liver classification tasks, with fewer parameters than ResNet50 or DenseNet"),
        sp(4),
        h3("3.1.2  Decoder with Attention Gates"),
        bul("Architecture: Standard U-Net decoder with transposed convolution upsampling blocks at each scale"),
        bul("Attention gates: Inserted at every skip connection — each gate computes a soft attention weight map from the gating signal (decoder) and encoder feature map, suppressing background and noise while emphasising liver boundary regions"),
        bul("Multi-scale dilated convolutional attention module (MDCAM): Placed at the bottleneck to capture global contextual information across varying liver shapes and sizes"),
        bul("Boundary decoder: A separate lightweight decoder branch explicitly supervised on liver boundary masks during training — sharpens capsule edge delineation"),
        sp(4),
        h3("3.1.3  Training the Segmentation Branch"),
        bul("Loss function: Combined Dice loss + Binary Cross-Entropy loss (lambda=0.5 each) — Dice handles class imbalance; BCE ensures pixel-level precision"),
        bul("Label source: Liver masks from Saudi NAFLD OSF dataset (manually annotated) + auto-generated pseudo-labels from a pre-trained nnU-Net applied to additional unlabelled scans"),
        bul("Target metric: Dice Similarity Coefficient (DSC) >= 0.94 on held-out test set — matching Attention U-Net published benchmarks of 0.9468"),
        sp(6),
        h2("3.2  ROI Cropping"),
        body("After segmentation, the bounding box of the predicted liver mask is extracted with a 5% padding margin. The original image is cropped to this bounding box and resized to 384×384 for input to the classification branch. This ensures the CNN operates entirely within liver parenchyma, improving sensitivity to echotexture changes and eliminating irrelevant background signal."),
    ]

    # ── SECTION 4 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("04  CLASSIFICATION BRANCH — FIBROSIS FEATURE EXTRACTION", width=usable_w), sp(6),
        h2("4.1  Architecture: EfficientNet-B4 + ResNet50 Ensemble"),
        body("The classification branch takes the liver-cropped ROI image as input and produces a dense image embedding capturing fibrosis-relevant features: echotexture coarseness, increased echogenicity, posterior echo attenuation, surface nodularity, and capsule irregularity."),
        h3("4.1.1  Dual Backbone Ensemble"),
        body("A 2025 Scientific Reports paper demonstrated that fusing EfficientNetB0 and ResNet50 features achieved 99.45% accuracy on liver fibrosis staging — significantly outperforming either backbone alone. SonoSense adopts this ensemble principle with EfficientNet-B4 (stronger than B0) and ResNet50:"),
        sp(6),
        make_table(
            ["Backbone", "Parameters", "Strengths", "Output embedding dim"],
            [
                ["EfficientNet-B4", "19M", "Best sensitivity on ultrasound; efficient compound scaling; fewer FLOPs", "1792-dim"],
                ["ResNet50", "25M", "Strong residual feature learning; well-studied on medical images; complementary texture features", "2048-dim"],
            ],
            [2200, 1500, 4500, 1880]
        ),
        sp(8),
        bul("Feature concatenation: After global average pooling, the 1792-dim and 2048-dim embeddings are concatenated to form a 3840-dim combined image embedding"),
        bul("Dimensionality reduction: A linear projection layer with dropout (p=0.3) reduces this to a 1024-dim image feature vector for fusion"),
        bul("Weight sharing with segmentation encoder: The EfficientNet-B4 encoder weights are partially shared with the segmentation branch — layers 1–5 are shared (multi-task learning), layers 6–9 are task-specific — reducing total parameter count by ~35%"),
        sp(6),
        h3("4.1.2  Hybrid CNN-Transformer Attention"),
        body("The classification branch optionally incorporates a lightweight Transformer self-attention module applied to the patch-level feature grid from EfficientNet-B4 (before global average pooling). This allows the model to capture long-range spatial dependencies — correlating surface irregularity at the liver capsule with internal echotexture changes — which purely convolutional models miss."),
        bul("Implementation: 4-head self-attention on a 16×16 spatial grid of patch embeddings from the EfficientNet-B4 penultimate feature map"),
        bul("Parameter cost: +1.8M parameters — small relative to the backbone"),
        bul("Ablation finding: Hybrid CNN-Transformer architectures consistently outperform pure CNN models by 1.5–3% AUROC on hepatic ultrasound classification tasks"),
        sp(6),
        h2("4.2  Pre-training Strategy"),
        body("Both backbones are initialised with ImageNet weights and then fine-tuned in two stages:"),
        bul("Stage 1 — Ultrasound domain adaptation: Pre-trained on a large corpus of unlabelled abdominal ultrasound images using self-supervised contrastive learning (SupCon loss). A 2025 PMC paper (LivSCP) demonstrated that supervised contrastive pretraining on liver ultrasound achieved AUROC values of 0.989–1.000 across all fibrosis stages."),
        bul("Stage 2 — Task-specific fine-tuning: Fine-tuned on labelled fibrosis staging data (Saudi OSF + Kaggle + Korean hospital datasets) with a cosine annealing learning rate schedule (initial LR: 1e-4, min LR: 1e-6, warmup: 5 epochs)"),
    ]

    # ── SECTION 5 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("05  TABULAR ENCODER — CLINICAL FEATURE PROCESSING", width=usable_w), sp(6),
        h2("5.1  MLP Tabular Encoder"),
        body("The clinical laboratory values and patient metadata are encoded by a dedicated multi-layer perceptron (MLP) that produces a 256-dim clinical embedding, which is then fused with the 1024-dim image embedding in the fusion layer."),
        h3("5.1.1  Input Feature Engineering"),
        body("Before passing lab values to the MLP, four derived features are computed and appended to the raw lab vector:"),
        bul("FIB-4 score: (Age × AST) / (Platelet × sqrt(ALT)) — the current clinical standard, fed in so the model can learn when it is wrong"),
        bul("APRI score: (AST / 40) × 100 / Platelet — independent fibrosis signal"),
        bul("AST/ALT ratio: Rises above 1.0 in advanced fibrosis, providing a simple but powerful discriminator"),
        bul("Albumin/Globulin ratio: Derived from albumin and total protein — imbalance reflects synthetic liver dysfunction"),
        body("This gives a total of up to 16 input features (12 raw + 4 derived), with a missingness mask of equal length concatenated, yielding a 32-dim input vector to the MLP."),
        h3("5.1.2  MLP Architecture"),
        bul("Input layer: 32 neurons (16 features + 16 missingness flags)"),
        bul("Hidden layers: 128 → 256 → 256 neurons with ReLU activation, batch normalisation, and dropout (p=0.25) at each layer"),
        bul("Output: 256-dim clinical embedding"),
        bul("Regularisation: L2 weight decay (lambda=1e-4) to prevent overfitting on small tabular datasets"),
    ]

    # ── SECTION 6 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("06  MULTIMODAL FUSION LAYER", width=usable_w), sp(6),
        h2("6.1  Cross-Attention Fusion"),
        body("The 1024-dim image embedding and the 256-dim clinical embedding are combined using a cross-attention mechanism — the image embedding attends over clinical features and vice versa, producing a jointly modulated 512-dim fused representation."),
        h3("6.1.1  Fusion Architecture"),
        bul("Query: Clinical embedding (256-dim), projected to 512-dim"),
        bul("Key / Value: Image embedding (1024-dim), projected to 512-dim"),
        bul("Attention: Single-head cross-attention; attention weights are logged per inference for interpretability — they reveal how much each clinical variable modulated the image prediction"),
        bul("Concatenation fallback: If attention training is unstable during early runs, a simpler concatenation + linear projection layer (1024 + 256 → 512) is used as the fusion mechanism — both are implemented and switchable via config flag"),
        sp(6),
        h2("6.2  Why Fusion Outperforms Single-Stream Models"),
        body("Published evidence confirms the multimodal advantage: a Nature Communications 2026 paper integrating patient history, routine labs, and ultrasound features achieved AUROC 0.90 for advanced fibrosis — outperforming FIB-4 alone and ultrasound-only models. The cross-attention mechanism specifically allows the model to condition its image interpretation on clinical context — for example, treating an ambiguous echotexture reading differently when platelet count is normal vs. critically low."),
    ]

    # ── SECTION 7 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("07  OUTPUT LAYER — CLASSIFICATION, CALIBRATION & EXPLAINABILITY", width=usable_w), sp(6),
        h2("7.1  Classification Head"),
        bul("Architecture: Two-layer MLP on the 512-dim fused representation → 5-class softmax output (F0, F1, F2, F3, F4)"),
        bul("Ordinal constraint: A cumulative link model (CLM) layer is applied on top of raw logits to enforce ordinality — the model cannot predict a higher probability for F2 than F0 while simultaneously predicting a low probability for F1"),
        bul("Multi-threshold outputs: Five separate binary classifiers are derived from the main model to support specific clinical decision thresholds described in the evaluation framework"),
        sp(6),
        h2("7.2  Confidence Calibration"),
        body("Raw neural network softmax probabilities are systematically overconfident and must be calibrated before clinical use. SonoSense applies:"),
        bul("Temperature scaling: A single scalar parameter T is learned on the validation set — logits are divided by T before softmax, expanding the probability distribution. Target: Expected Calibration Error (ECE) < 0.05"),
        bul("Platt scaling (fallback): A logistic regression layer trained on validation set predictions provides an alternative calibration approach for binary threshold outputs"),
        bul("Reliability diagrams: Generated on the test set and included in the evaluation report — bins of 0.1 width across the [0,1] confidence range, plotting mean predicted probability vs. observed frequency"),
        sp(6),
        h2("7.3  Uncertainty Quantification"),
        body("A single deterministic prediction is insufficient for clinical trust. SonoSense provides two uncertainty measures:"),
        bul("MC Dropout: At inference, dropout is kept active and 20 forward passes are run. The mean of predictions is the final output; the standard deviation is the epistemic uncertainty estimate. High uncertainty outputs (sigma > 0.15) are flagged with a 'Low Confidence — Recommend Clinical Review' warning"),
        bul("Prediction interval: The 10th–90th percentile range across MC Dropout passes is reported alongside the point estimate — e.g., 'F2 (84% confidence, range: F1–F3)'"),
        sp(6),
        h2("7.4  Explainability — Grad-CAM Heatmap"),
        body("Gradient-weighted Class Activation Mapping (Grad-CAM) is applied to the EfficientNet-B4 backbone to produce a spatial heatmap indicating which liver regions drove the predicted fibrosis stage. Published liver fibrosis staging studies applying Grad-CAM achieved AUROCs of 0.92, 0.89, and 0.88 for significant fibrosis, advanced fibrosis, and cirrhosis respectively."),
        h3("7.4.1  Heatmap Generation Pipeline"),
        bul("Target layer: The final convolutional layer of EfficientNet-B4 (before global average pooling)"),
        bul("Gradient computation: Gradients of the predicted class score with respect to the target layer activations are computed and global-average-pooled to produce channel weights"),
        bul("Activation weighting: Channel weights multiply the activation maps and are ReLU-clipped to retain only positive contributions"),
        bul("Upsampling: The resulting low-resolution activation map is bilinearly upsampled to match the original image resolution (512×512)"),
        bul("Overlay: The heatmap is blended onto the original ultrasound image (alpha=0.45) using a jet colourmap — red/yellow regions indicate high fibrosis signal; blue/cool regions indicate low contribution"),
        bul("Masking: The heatmap is zero-masked outside the U-Net liver segmentation boundary — only activations within the liver region are shown"),
        sp(4),
        h3("7.4.2  Heatmap Validation (Faithfulness Testing)"),
        bul("Occlusion test: High-activation regions are progressively occluded; model confidence must drop proportionally — if not, the heatmap is flagged as non-faithful and Grad-CAM++ is used instead"),
        bul("Pointing game: The peak activation must fall within a hepatologist-annotated region of interest — target accuracy >= 70% on held-out annotated subset"),
        bul("IoU with expert annotations: Target Intersection over Union >= 0.50 on a 100-image subset annotated by two hepatologists"),
        sp(6),
        h2("7.5  SHAP Feature Attribution (Tabular Explanation)"),
        body("To explain the contribution of individual clinical variables to each prediction, SHAP (SHapley Additive Explanations) values are computed for the tabular MLP encoder output. This tells the clinician: 'platelet count of 98 x 10^9/L contributed +0.23 toward an F3 prediction, while normal ALT contributed -0.11.' SHAP values are displayed in the structured report as a horizontal bar chart ordered by contribution magnitude."),
        sp(6),
        h2("7.6  At-Risk MASH Flag and Referral Logic"),
        body("Any prediction of F2 or above triggers the At-Risk MASH flag automatically. The referral recommendation is generated as follows:"),
        sp(6),
        make_table(
            ["Predicted Stage", "Confidence", "Action Generated"],
            [
                ["F0–F1", ">= 70%", "No referral. Reassess in 12 months if metabolic risk factors present."],
                ["F0–F1", "< 70%", "Indeterminate result. Recommend FIB-4 repeat or hepatology review."],
                ["F2", ">= 70%", "At-Risk MASH flag. Hepatology referral recommended. Consider Resmetirom eligibility assessment."],
                ["F3", "Any", "Advanced fibrosis. Urgent hepatology referral. Varices screening recommended."],
                ["F4", "Any", "Cirrhosis. Immediate hepatology referral. HCC surveillance protocol."],
            ],
            [1900, 1600, 6580]
        ),
    ]

    # ── SECTION 8 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("08  STRUCTURED REPORT GENERATION", width=usable_w), sp(6),
        h2("8.1  Report Contents"),
        body("Each SonoSense inference generates a structured clinical report containing:"),
        bul("Patient demographics and scan metadata (date, machine, operator ID)"),
        bul("Three-panel image: original ultrasound | liver segmentation overlay | Grad-CAM heatmap"),
        bul("Fibrosis grade: F0–F4 with confidence percentage and prediction interval"),
        bul("Uncertainty flag: 'Low Confidence' warning if MC Dropout sigma > 0.15"),
        bul("SHAP bar chart: Top 5 contributing clinical variables"),
        bul("FIB-4 corroboration: Computed FIB-4 score displayed alongside SonoSense grade — flagged as 'consistent' or 'discordant' (discordance triggers a review prompt)"),
        bul("At-Risk MASH flag and recommended action"),
        bul("Disclaimer: Prototype research tool notice — not for clinical use"),
        sp(6),
        h2("8.2  Export Formats"),
        bul("PDF: Self-contained clinical summary for printing or EMR attachment"),
        bul("HL7 FHIR R4 DiagnosticReport resource: Machine-readable, structured for direct EMR ingestion (Epic, Cerner, OpenMRS)"),
        bul("JSON: Raw inference output for API consumers and downstream analytics"),
    ]

    # ── SECTION 9 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("09  DEPLOYMENT ARCHITECTURE", width=usable_w), sp(6),
        h2("9.1  Deployment Targets"),
        h3("9.1.1  PACS Plugin (Primary Deployment)"),
        body("SonoSense deploys as a DICOM node within the hospital PACS network. When a radiologist opens an abdominal ultrasound study for reporting, SonoSense automatically receives the DICOM series via DICOM C-STORE, runs inference, and pushes the structured report back as a DICOM SR (Structured Report) and secondary capture image. The radiologist sees the heatmap overlay and grade within their existing reporting interface with zero additional steps."),
        h3("9.1.2  REST API (Cloud / EMR Integration)"),
        bul("Endpoint: POST /v1/infer — accepts multipart form data with DICOM file + JSON clinical data"),
        bul("Response: JSON inference result + base64-encoded heatmap PNG + FHIR DiagnosticReport"),
        bul("Authentication: OAuth 2.0 bearer tokens; all payloads encrypted in transit (TLS 1.3)"),
        bul("SLA: Inference latency < 8 seconds end-to-end (preprocessing + segmentation + classification + report generation) on T4 GPU"),
        h3("9.1.3  SaaS Dashboard (Clinic Portal)"),
        body("Gastroenterology and primary care clinics without PACS infrastructure access SonoSense via a web dashboard. Clinicians upload the ultrasound image and enter lab values manually or via CSV import. Results are returned within 10 seconds and stored in an audit-logged patient record within the dashboard."),
        sp(6),
        h2("9.2  Infrastructure"),
        make_table(
            ["Component", "Technology", "Notes"],
            [
                ["Model serving", "FastAPI + Uvicorn on Docker", "Containerised inference; horizontal scaling via Kubernetes"],
                ["GPU inference", "NVIDIA T4 / A10G", "ONNX Runtime for optimised inference; TorchScript export"],
                ["Model registry", "MLflow", "Version tracking, experiment logging, A/B testing between model versions"],
                ["DICOM handling", "Orthanc PACS + pydicom", "Receives and sends DICOM via C-STORE and C-FIND"],
                ["Database", "PostgreSQL", "Patient records, audit logs, prediction history"],
                ["Storage", "AWS S3 / on-prem MinIO", "DICOM archives, model artefacts, report PDFs"],
                ["Monitoring", "Prometheus + Grafana", "Inference latency, confidence distribution drift, error rates"],
                ["Security", "TLS 1.3, AES-256 at rest", "HIPAA-aligned data handling; de-identification pipeline for research exports"],
            ],
            [2400, 2800, 4880]
        ),
    ]

    # ── SECTION 10 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("10  TRAINING DATASETS & EXPERIMENTAL SETUP", width=usable_w), sp(6),
        h2("10.1  Dataset Stack"),
        make_table(
            ["Dataset", "Images/Patients", "Labels", "Lab Data", "Access"],
            [
                ["Saudi NAFLD (OSF: osf.io/c2yg8)", "10,352 images / 384 pts", "NAS F0–F4 + steatosis (biopsy-proven)", "No", "Open access"],
                ["BEHSOF (Figshare)", "~500 images / 113 pts", "Steatosis + fibrosis grade", "Yes (full labs)", "Open access"],
                ["Kaggle Liver Fibrosis (vibhingupta028)", "~2,500 images", "F0–F4 stage", "No", "Open access"],
                ["Korean Hospital (Park et al. 2024)", "7,920 images / 933 pts", "METAVIR F0–F4 (biopsy/hepatectomy)", "No", "Request from authors"],
                ["NIDDK NASH CRN", "2,500+ pts", "NAS biopsy gold standard + full labs", "Yes (complete)", "Apply via NIDDK repository"],
            ],
            [2800, 2200, 2400, 1200, 1480]
        ),
        sp(10),
        h2("10.2  Data Split Strategy"),
        bul("Training set: 65% — model learns weights"),
        bul("Validation set: 15% — hyperparameter tuning, early stopping, calibration"),
        bul("Internal test set: 20% — reported performance metrics, never touched during training"),
        bul("External validation: Separate hospital dataset not used in any training phase — essential for regulatory-grade claims"),
        body("Patient-level splits are enforced: all images from the same patient appear in the same split only, preventing data leakage from multi-frame studies."),
        sp(6),
        h2("10.3  Training Configuration"),
        make_table(
            ["Hyperparameter", "Value", "Rationale"],
            [
                ["Optimiser", "AdamW (beta1=0.9, beta2=0.999)", "Weight decay decoupling prevents feature co-adaptation"],
                ["Learning rate", "1e-4 (backbone), 1e-3 (head)", "Differential LR: slower fine-tuning for pretrained layers"],
                ["LR schedule", "Cosine annealing with warm restart", "Avoids sharp loss valleys; improves generalisation"],
                ["Batch size", "32 (image) / 128 (tabular)", "Larger tabular batches for stable BN statistics"],
                ["Epochs", "100 max with early stopping (patience=15)", "Prevents overfitting on small ultrasound datasets"],
                ["Loss — segmentation", "Dice + BCE (lambda=0.5 each)", "Handles class imbalance; pixel precision"],
                ["Loss — classification", "Weighted cross-entropy + ordinal penalty", "Higher weight on F3/F4 minority classes; penalises large stage errors"],
                ["Class weights", "Inverse frequency weighting", "F3 and F4 are underrepresented — upweighted by factor 3–5x"],
                ["Hardware", "2x NVIDIA A100 40GB", "Multi-GPU training via PyTorch DDP; ~18h for full pipeline"],
            ],
            [2800, 3000, 4280]
        ),
    ]

    # ── SECTION 11 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("11  EVALUATION FRAMEWORK", width=usable_w), sp(6),
        h2("11.1  Primary Metrics"),
        make_table(
            ["Metric", "Target", "Clinical Threshold"],
            [
                ["AUROC — F2+ (significant fibrosis)", ">= 0.88", "Regulatory-grade performance for staging tool"],
                ["AUROC — F3+ (advanced fibrosis)", ">= 0.90", "Strong discrimination for urgent referral decisions"],
                ["Sensitivity — F2+", ">= 85%", "Missing an at-risk patient is the primary harm to avoid"],
                ["Specificity — F2+", ">= 78%", "Limits unnecessary referrals and patient anxiety"],
                ["AUPRC — F2+", ">= 0.80", "Accounts for class imbalance in real-world prevalence"],
                ["Quadratic Weighted Kappa", ">= 0.65", "Substantial agreement with biopsy gold standard"],
                ["Expected Calibration Error (ECE)", "< 0.05", "Well-calibrated confidence scores for clinical trust"],
                ["Heatmap IoU", ">= 0.50", "Heatmap reliably highlights radiologist-identified regions"],
            ],
            [3200, 2200, 4680]
        ),
        sp(10),
        h2("11.2  Benchmark Comparisons"),
        body("All reported metrics are compared head-to-head against:"),
        bul("FIB-4 score alone — current standard of care in primary care"),
        bul("FibroScan (VCTE) — current best non-invasive tool"),
        bul("Radiologist reading of the same ultrasound without SonoSense"),
        bul("Radiologist reading with SonoSense — to demonstrate augmentation benefit"),
        body("The most clinically compelling result is: SonoSense alone >= FibroScan, and Radiologist + SonoSense > Radiologist alone, measured by both AUROC and Net Reclassification Improvement (NRI) vs. FIB-4."),
        sp(6),
        h2("11.3  Clinical Impact Metrics"),
        bul("Net Reclassification Improvement (NRI) vs. FIB-4: Proportion of patients correctly moved from indeterminate or wrong category to correct stage"),
        bul("Integrated Discrimination Improvement (IDI): Improvement in predicted probability separation between true positives and negatives vs. FIB-4"),
        bul("Number Needed to Screen (NNS): How many ultrasounds SonoSense reads to correctly identify one at-risk patient missed by FIB-4 alone"),
    ]

    # ── SECTION 12 ──────────────────────────────────────────────────────────
    story += [
        sp(16), SectionBanner("12  DEVELOPMENT ROADMAP", width=usable_w), sp(6),
        make_table(
            ["Phase", "Timeline", "Milestones"],
            [
                ["Phase 1 — Baseline", "Now → Aug 2026", "Saudi OSF + Kaggle data prep; baseline EfficientNet-B4 image-only classifier; internal test AUROC >= 0.80 for F2+"],
                ["Phase 2 — Multimodal", "Aug → Oct 2026", "Tabular encoder integration; cross-attention fusion; BEHSOF lab data incorporated; target AUROC >= 0.87"],
                ["Phase 3 — Explainability", "Sep → Oct 2026", "Attention U-Net segmentation branch; Grad-CAM pipeline; SHAP attribution; heatmap IoU validation"],
                ["Phase 4 — Prototype Launch", "Early Nov 2026", "Full pipeline integrated; SaaS dashboard live; structured report generation; disclaimer-compliant public prototype"],
                ["Phase 5 — Clinical Validation", "Nov 2026 → 2027", "Partner hospital data collection; external validation cohort; NRI/IDI vs. FIB-4; ethics board submission"],
                ["Phase 6 — Regulatory", "2027+", "CDSCO Class B medical device submission; CE Mark technical file; FDA De Novo pathway assessment"],
            ],
            [1600, 1800, 6680]
        ),
    ]

    # ── FINAL DISCLAIMER ──────────────────────────────────────────────────
    story += [
        sp(20),
        SectionBanner("IMPORTANT NOTICES", width=usable_w),
        sp(10),
        DisclaimerBox(width=usable_w),
        sp(8),
        Paragraph(
            "SonoSense is developed by Lumina AI as a research prototype. All clinical claims are based on "
            "published peer-reviewed literature and have not yet been validated in prospective clinical trials. "
            "Performance figures cited from the literature reflect published models and may not be directly "
            "reproducible without equivalent datasets, hardware, and training configurations. This document is "
            "for informational and research planning purposes only.",
            ST['disclaimer_foot']
        ),
    ]

    return story


# ── Render ────────────────────────────────────────────────────────────────────
out = "sonosensesummary.pdf"
doc = make_doc(out)
story = build()
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("Done →", out)