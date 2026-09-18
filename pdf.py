from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import Table, TableStyle

output_path = "chapter4_summary.pdf"

doc = SimpleDocTemplate(output_path, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('CT', parent=styles['Title'], fontSize=22,
    textColor=HexColor('#7B2D2D'), spaceAfter=6, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('CS', parent=styles['Normal'], fontSize=12,
    textColor=HexColor('#555555'), spaceAfter=20, fontName='Helvetica-Oblique')
h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=15,
    textColor=HexColor('#7B2D2D'), spaceBefore=16, spaceAfter=6, fontName='Helvetica-Bold')
h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12,
    textColor=HexColor('#3A5F8A'), spaceBefore=12, spaceAfter=4, fontName='Helvetica-Bold')
h3_style = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11,
    textColor=HexColor('#2E7D32'), spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold')
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10,
    leading=15, spaceAfter=6, fontName='Helvetica')
bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=10,
    leading=14, leftIndent=15, spaceAfter=3, fontName='Helvetica', bulletIndent=5)
footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9,
    textColor=HexColor('#888888'), alignment=1)

def table(data, col_widths, header_color=HexColor('#7B2D2D'), row_colors=None):
    if row_colors is None:
        row_colors = [HexColor('#FDF3F3'), white]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), row_colors),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#CCCCCC')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    return t

story = []

# ── TITLE ──────────────────────────────────────────────────────────────────
story.append(Paragraph("Chapter 4 — Detailed Summary", title_style))
story.append(Paragraph("Early Humans and Beginning of Civilisation", subtitle_style))
story.append(Paragraph("Grade 9 | Understanding Society: India and Beyond — Part 1", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=HexColor('#7B2D2D'), spaceAfter=14))

# ── 1. INTRODUCTION ────────────────────────────────────────────────────────
story.append(Paragraph("1. Introduction", h1_style))
story.append(Paragraph(
    "This chapter traces the complete journey of humankind from its earliest African origins to the rise of "
    "Bronze Age civilisations. It covers biological and cultural evolution, the Stone Age stages, the Neolithic "
    "Revolution, the Sindhu–Sarasvati civilisation, and three other major contemporaneous civilisations: "
    "Mesopotamia, Egypt, and China.", body_style))

story.append(Paragraph("Big Questions the Chapter Addresses", h2_style))
for q in [
    "How did humans live on Earth before the beginning of civilisation?",
    "How did humans communicate before writing was invented?",
    "How is archaeology helpful in understanding our past?",
    "How did early civilisations interact with each other?",
]:
    story.append(Paragraph(f"• {q}", bullet_style))

# ── 2. THE INVENTION OF WRITING ────────────────────────────────────────────
story.append(Paragraph("2. The Invention of Writing: Before and After", h1_style))
story.append(Paragraph(
    "The period before writing is known as <b>prehistory</b> and is studied almost entirely through "
    "archaeological evidence. Writing systems emerged at different times in different places. Key writing "
    "systems include:", body_style))
wr_data = [
    ["Script / System", "Civilisation", "Status"],
    ["Sindhu Lipi (Harappan script)", "Sindhu–Sarasvati (Indus Valley)", "Pictographic; NOT yet deciphered"],
    ["Cuneiform", "Sumerians, Mesopotamia", "Wedge-shaped; deciphered; ~3200 BCE"],
    ["Hieroglyphics", "Ancient Egypt", "Deciphered 1822 via Rosetta Stone"],
    ["Brahmi", "Indian subcontinent", "Used from ~400 BCE; formalised by Ashoka (3rd century BCE)"],
    ["Chinese logographic script", "China", "Characters representing words; derived from oracle bones"],
]
story.append(table(wr_data, [5*cm, 4.5*cm, 6.5*cm]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "Before writing, more than 99% of human history falls in the prehistoric period (from ~3 million years ago "
    "to 5000 years ago). After writing, only the last ~5000 years constitute 'history'. Before writing, only "
    "material artefacts are sources of knowledge; after writing, both material remains and written documents "
    "are available. Dating of events becomes more accurate with written records.", body_style))

# ── 3. WHY STUDY EARLY HUMAN HISTORY ──────────────────────────────────────
story.append(Paragraph("3. Why Study Early Human History?", h1_style))
story.append(Paragraph(
    "<b>Biological evolution</b> refers to the gradual physical and genetic changes through which early "
    "ancestors — known as <b>australopithecines</b> (australis = southern; pithecus = primates) — evolved "
    "into modern humans (<i>Homo sapiens</i>).", body_style))
story.append(Paragraph(
    "<b>Cultural evolution</b> explains how humans adapted to their surroundings during the "
    "<b>Quaternary Period</b> (the last 26 lakh years, including the present). Humans developed tools, "
    "techniques, and other technologies to exploit natural resources. Over time, the shift from hunting and "
    "gathering to agriculture and food production enabled the production of surplus food, which laid the "
    "foundation for the emergence of civilisation.", body_style))

# ── 4. WHO WERE OUR HUMAN ANCESTORS ───────────────────────────────────────
story.append(Paragraph("4. Who Were Our Human Ancestors?", h1_style))
story.append(Paragraph(
    "The earliest human settlements were found in Africa, Asia, and Europe — collectively called the "
    "<b>'Old World'</b>. Around <b>3.3 million years ago</b>, one of our ancestors made the earliest stone "
    "tools, marking the beginning of 'human behaviour'. Humans became known as <b>hominins</b> (tool makers). "
    "Tools functioned as 'extra-corporal limbs' — extensions of the human body. Discarded tools and fossil "
    "remains, buried underground and turned to stone over millions of years, are the main sources of "
    "archaeological evidence.", body_style))

anc_data = [
    ["Ancestor", "Period / Location", "Key Traits / Tools"],
    ["Homo habilis\n(Handy Man)", "2–6 million years ago;\nOlduvai Gorge, Tanzania & Kenya", "Earliest chopper stone tools; lived in Africa."],
    ["Homo erectus\n(Upright Man)", "~2 million years ago;\nEastern African Rift Valley", "Invented handaxes and cleavers; FIRST hominin to exit Africa; spread to Europe and Asia between 2 and 0.5 million years ago."],
    ["Homo neanderthalensis", "Till ~40,000 years ago;\nEurope and Southwest Asia", "Made Middle Palaeolithic flake tools."],
    ["Homo sapiens\n(Modern Humans)", "Evolved ~300,000 years ago\nin Africa; now global", "Developed complex technologies; symbolic communication; spread globally including Australia and Americas (50,000–12,000 years ago)."],
]
story.append(table(anc_data, [4*cm, 4.5*cm, 7.5*cm], header_color=HexColor('#3A5F8A'),
    row_colors=[HexColor('#EEF4FB'), white]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "A second major wave of migration out of Africa took place around <b>125,000 years ago</b>, associated "
    "with early <i>Homo sapiens</i>, who are now spread all over the earth.", body_style))

# ── 5. PERIODS IN EARLY HUMAN HISTORY ─────────────────────────────────────
story.append(Paragraph("5. Periods in Early Human History", h1_style))
periods_data = [
    ["Period", "Key Features"],
    ["Palaeolithic\n(Old Stone Age)", "Hunting-gathering lifestyle; use of simple stone tools (handaxes, cleavers, scrapers, borers, points); lived in caves or open camps. Later: bow and arrow; microblade tools; symbolic communication; cave paintings; beads of stone, bone, and shell; burin/engraver tool for carving on bones and shells."],
    ["Mesolithic\n(Middle Stone Age)", "Transitional phase (~12,000 years ago); Earth's climate became warmer; forests and grasslands expanded; microlithic (tiny) tools; fishing became the main subsistence activity; first-ever population explosion in human history; Bhimbetka (MP) — World Heritage Site with painted rock shelters."],
    ["Neolithic Revolution\n(New Stone Age)", "Gradual shift to agriculture and settled life (the Neolithic Revolution); domestication of select animals and plants; polished stone tools; earthenware pottery; first village settlements — foundations of urban revolution. Transition happened at different times in different regions."],
    ["Chalcolithic\n(Copper & Stone Age)", "Use of copper along with stone tools; early metallurgy (extraction and shaping of metal objects). Mehrgarh people became Chalcolithic by ~4000 BCE."],
    ["Bronze Age", "Development of bronze metallurgy (mixing copper and tin); expansion of trade, towns, and early civilisations."],
    ["Iron Age", "Widespread use of iron metallurgy; stronger tools and weapons; more advanced societies."],
]
story.append(table(periods_data, [4*cm, 12*cm], header_color=HexColor('#7B4F00'),
    row_colors=[HexColor('#FDF8EE'), white]))
story.append(Spacer(1, 6))

# ── 6. PALAEOLITHIC HUNTER-GATHERERS ──────────────────────────────────────
story.append(Paragraph("6. Palaeolithic Hunter-Gatherers in India", h1_style))
story.append(Paragraph(
    "The Stone Age is divided into three stages — Palaeolithic (palaeo = old; lithic = stone), Mesolithic, "
    "and Neolithic. In the Indian subcontinent, the <b>oldest human settlement dates to ~2 million years ago</b>. "
    "Key sites include:", body_style))
for site in [
    "<b>Attirampakkam</b> (Tamil Nadu) — dated to ~1.5–1.7 million years ago; animal fossils, handaxes, cleavers.",
    "<b>Isampur</b> (Karnataka) — dated to ~1.2 million years ago; quartzite and limestone scrapers, choppers.",
    "<b>Hathnora</b> (Madhya Pradesh) — important Middle Palaeolithic site.",
    "<b>Bhimbetka</b> (Madhya Pradesh) — World Heritage Site; hundreds of painted rock shelters with Mesolithic and earlier occupation; cave art showing humans and animals.",
    "<b>Kurnool District</b> (Andhra Pradesh) — microlithic tools and bone points.",
]:
    story.append(Paragraph(f"• {site}", bullet_style))

story.append(Paragraph("Tool Evolution", h3_style))
story.append(Paragraph(
    "Lower Palaeolithic: handaxes and cleavers used to chop meat, dig tubers, scrape skin, and cleave bones "
    "for marrow. Middle Palaeolithic: smaller tools — scrapers, borers, and points — for improved projectile "
    "hunting. Upper Palaeolithic/Microlithic: bow and arrow; parallel-sided blade and microblade tools from "
    "glassy rocks; burin/engraver tools; decorative beads of stone, bone, and shell; cave paintings; "
    "pigments for body decoration.", body_style))

# ── 7. NEOLITHIC REVOLUTION ────────────────────────────────────────────────
story.append(Paragraph("7. The Neolithic Revolution", h1_style))
story.append(Paragraph(
    "As hunter-gatherers gained familiarity with seasons and food resources, there was a gradual transition "
    "to a food-producing way of life — the <b>Neolithic Revolution</b>. Its defining feature was the "
    "<b>domestication</b> of select animals and plants, new breeds through cultivation and husbandry, "
    "earthenware pottery, use of polished stone tools, and the establishment of the first village settlements.", body_style))

story.append(Paragraph("Regional Timelines for Transition to Agriculture", h3_style))
agri_data = [
    ["Region", "Key Crop(s)", "Approximate Timing"],
    ["West Asia", "Wheat and barley", "Farming began ~12,000 years ago; copper tools ~4500 BCE"],
    ["West Africa", "Pearl millet", "Pottery → livestock → cultivation → sedentism (later)"],
    ["India (general)", "Millets", "Pottery, livestock, cultivation, sedentism"],
    ["India – Ganga Plains", "Rice", "Later than peninsular India"],
    ["North China (Yellow River)", "Millets", "~7000 BCE Neolithic cultures"],
    ["South China (Yangtze)", "Rice", "~7000 BCE Neolithic cultures"],
]
story.append(table(agri_data, [4*cm, 4.5*cm, 7.5*cm], header_color=HexColor('#2E7D32'),
    row_colors=[HexColor('#EEF8EE'), white]))
story.append(Spacer(1, 6))

story.append(Paragraph("Neolithic Period in the Indian Subcontinent", h3_style))
story.append(Paragraph(
    "<b>Mehrgarh</b> (on the Bolan River, present-day Pakistan) is the oldest Neolithic site and earliest "
    "agricultural village in the subcontinent, dating to ~<b>7000 BCE</b>. Features: handmade sun-dried "
    "brick houses; granaries; burials with ornaments of lapis lazuli, carnelian, and shells; cultivation of "
    "wheat and barley; raising of sheep, goats, and zebu humped cattle; copper objects (making them "
    "Chalcolithic by ~4000 BCE). This laid the basis for the Bronze Age Sindhu–Sarasvati civilisation "
    "around <b>3500 BCE</b>.", body_style))
story.append(Paragraph(
    "By <b>2500 BCE</b>, most of the Indian subcontinent was occupied by Neolithic agricultural communities "
    "growing cereals, millets, and pulses, sometimes interacting with contemporary Chalcolithic cultures.", body_style))

# ── 8. SINDHU-SARASVATI CIVILISATION ──────────────────────────────────────
story.append(Paragraph("8. Sindhu–Sarasvati Civilisation (Harappan Civilisation)", h1_style))
story.append(Paragraph(
    "The Neolithic way of life that emerged at Mehrgarh spread into the middle and upper Indus valley. "
    "Some settlements mastered copper extraction by <b>~4000 BCE</b>, becoming the earliest Chalcolithic "
    "sites — the beginning of the Bronze Age in the subcontinent.", body_style))

harp_data = [
    ["Phase", "Period", "Key Features"],
    ["Pre-Harappan / Early Harappan", "7000–2600 BCE", "Regional pottery styles; semi-precious stone beads; shell bangles; terracotta objects; copper working; perimeter walls around settlements; early use of seals; possible origins of the Harappan script. Bhirrana and Kunal on dried Sarasvati belt — pre-Harappan phases begin 7000–5500 BCE."],
    ["Mature Harappan", "2600–1900 BCE", "Full urban civilisation: well-planned cities, water management, drainage, standard weights and measures, inscribed seals, the undeciphered Harappan (Sindhu Lipi) script."],
    ["Late Harappan", "1900–1300 BCE", "Gradual decline of urban features."],
]
story.append(table(harp_data, [4*cm, 3.5*cm, 8.5*cm], header_color=HexColor('#7B2D2D'),
    row_colors=[HexColor('#FDF3F3'), white]))
story.append(Spacer(1, 6))

story.append(Paragraph("Crafts and Economy", h3_style))
for item in [
    "Pottery — a major craft and economic product; unique regional styles in vessel shapes and painted designs.",
    "Copper work, shell work, and semi-precious stone bead production (evidence from Harappa, Kunal in Haryana, Datrana in Gujarat).",
    "Agriculture — the Kalibangan ploughed fields show double-crop cultivation (horizontal and vertical furrows), like modern Rabi and Kharif patterns.",
    "Standard weights and measurement — binary multiple system (1, 2, 4, 8, 16...) for small weights; multiples of ten for large. Cubical stone weights found at multiple sites.",
    "Water management — Early Harappans built 'gabarbands' (check dams). Dholavira (Kachchh): elaborate water harvesting with dams, canals, and deep stone/mud-brick tanks. Lothal: huge dockyard of burnt bricks.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

# ── 9. BRONZE AGE CIVILISATIONS OUTSIDE INDIA ─────────────────────────────
story.append(Paragraph("9. Bronze Age Civilisations Outside India", h1_style))
story.append(Paragraph(
    "Four major early world civilisations emerged independently in fertile river plains, roughly "
    "contemporaneously. Mesopotamia and the Indus–Ghaggar-Sarasvati valleys were geographically close, "
    "which facilitated strong contacts and trade. Egypt and China had little direct evidence of contact "
    "with the Sindhu–Sarasvati civilisation.", body_style))
civ_data = [
    ["Civilisation", "River(s)", "Modern Region", "Key Dating"],
    ["Sindhu–Sarasvati\n(Harappan)", "Indus + Ghaggar-Sarasvati", "Pakistan / NW India", "~3500–1300 BCE"],
    ["Mesopotamian", "Euphrates + Tigris", "Iraq, Kuwait, parts of Turkey & Iran", "~3500 BCE onwards"],
    ["Egyptian", "Nile", "Egypt", "~3100 BCE onwards"],
    ["Chinese", "Huang He (Yellow R.) + Yangtze", "China", "~7000 BCE Neolithic;\n~1600 BCE Bronze Age"],
]
story.append(table(civ_data, [4*cm, 3.5*cm, 4.5*cm, 4*cm], header_color=HexColor('#555500'),
    row_colors=[HexColor('#FAFAEE'), white]))
story.append(Spacer(1, 6))

# ── 9a. MESOPOTAMIAN ──────────────────────────────────────────────────────
story.append(Paragraph("9a. Mesopotamian Civilisation", h2_style))
story.append(Paragraph(
    "Mesopotamia (Greek: 'land in between') — the region drained by the Euphrates and Tigris rivers in "
    "West Asia (modern Iraq, Kuwait, parts of Turkey and southwestern Iran). The crescent-shaped foothills "
    "of the Zagros and Taurus mountains stretching from the Mediterranean to the Persian Gulf are called "
    "the <b>'Fertile Crescent'</b>. Farming began ~12,000 years ago; copper tools arrived ~4500 BCE. "
    "The earliest city-based civilisation emerged here.", body_style))

story.append(Paragraph("The Four Major Mesopotamian City-State Civilisations", h3_style))
mes_data = [
    ["Civilisation", "Period", "Key Developments"],
    ["Sumerians", "~3500 BCE onwards", "Earliest city-based civilisation at Ur and other cities in Sumer (southern Iraq). First to build dams and canals for irrigation; used mud and burnt bricks. Built ziggurats (stepped pyramid-shaped temples) as centres of economic and religious life. Economic activities tied to temple authority. Invented the wheeled cart and sailboat. Number system based on 60 (60-min hour, 60-sec min, 360-degree circle). Invented cuneiform writing (~3200 BCE) — marks pressed into clay tablets with a wedge-shaped reed stylus. Used widely across Mesopotamia by 3000 BCE."],
    ["Akkadians", "2334 BCE onwards", "City-state of Akkad (central Mesopotamia). Spoke a different language but used the same cuneiform script. Sargon — an important king — documented trade with Dilmun (Bahrain), Magan (Oman), and Meluhha (identified with the Sindhu–Sarasvati civilisation). Trade goods: semiprecious stone beads, ivory, timber, gold dust, and copper. Established the world's first dynastic empire. Period of creative literature (Epic of Gilgamesh — one of the earliest written stories)."],
    ["Assyrians", "2154–1700 BCE", "City-state of Assur (northern Mesopotamia). Supplanted Akkadians. Dominance spread across Mesopotamia and into neighbouring western and southern regions."],
    ["Babylonians", "1900 BCE onwards", "Babylonia (central Mesopotamia). King Hammurabi (1792 BCE) — conquered neighbouring regions; compiled the Code of Hammurabi: rules and regulations for civil and social conduct — a foundational model for future legal systems. Babylonian dominance declined by 1400 BCE due to attacks by the Hittites (Indo-European people from Anatolia/modern Turkey), environmental degradation, and internal problems."],
]
story.append(table(mes_data, [3*cm, 3*cm, 10*cm], header_color=HexColor('#3A5F8A'),
    row_colors=[HexColor('#EEF4FB'), white]))
story.append(Spacer(1, 6))

# ── 9b. EGYPTIAN ──────────────────────────────────────────────────────────
story.append(Paragraph("9b. Egyptian Civilisation", h2_style))
story.append(Paragraph(
    "One of the earliest civilisations; known for rich historical records and lasting influence on other "
    "civilisations. Egypt was known to Greeks and Romans; Herodotus wrote about it in the 5th century BCE. "
    "History is also reconstructed from <b>papyrus</b> (paper made from the papyrus plant inner trunk) "
    "scrolls. Libraries dating to 2000 BCE stored papyrus scrolls — these contain some of the world's "
    "earliest stories, including versions of 'Sindbad the Sailor', Aesop-like fables, and 'Cinderella'.", body_style))

egypt_data = [
    ["Period", "Dates", "Key Features"],
    ["Neolithic", "5500 BCE", "Early farming communities"],
    ["Chalcolithic", "4000 BCE", "Copper tools introduced"],
    ["Bronze Age / Early Egypt", "3100 BCE", "City-states emerge (~3000 BCE); Nile floods deposited kemet (rich black mud) for crops. Farmers dug ditches to divert Nile water — led to collective effort and local government."],
    ["Old Kingdom", "2686–2181 BCE", "Pharaohs emerged as powerful rulers; pyramids built (mastabas stacked to form pyramids). Step Pyramid at Saqqara — prominent example. Belief in ka (spiritual double) led to mummification. Hieroglyphic writing. Social hierarchy: Pharaoh → Government officials, nobles, priests → Free landholders, artisans, merchants → Serfs and slaves."],
    ["Middle Kingdom", "2030–1650 BCE", "Libraries; rich papyrus literature"],
    ["New Kingdom", "1570–1069 BCE", "Height of Egyptian power; Cleopatra (69–30 BCE) became queen at age 18; Egyptian women had more rights than Greek or Roman women — could own property and run businesses."],
]
story.append(table(egypt_data, [3.5*cm, 3*cm, 9.5*cm], header_color=HexColor('#7B2D2D'),
    row_colors=[HexColor('#FDF3F3'), white]))
story.append(Spacer(1, 6))

story.append(Paragraph("Key Features of Egyptian Civilisation", h3_style))
for feat in [
    "<b>Calendar:</b> Three seasons of four months each (inundation/autumn, Peret/winter, Shemu/summer); based on the rising of Sirius (Dog Star). Year = 365 days (12 × 30 + 5 extra days) — highly accurate though ~¼ day short per year.",
    "<b>Mummification:</b> Removing internal organs (except the heart), drying with natron, oiling, wrapping in linen, placing in a coffin and burying with rituals — to preserve the body so the ka could live on after death.",
    "<b>Hieroglyphic script:</b> Deciphered in 1822 by French linguist Jean-François Champollion using the Rosetta Stone (found in 1799 by Pierre Bouchard) — a giant black stone with three types of writing including Greek.",
    "<b>Leisure and culture:</b> Swimming, canoeing, board games, music, dancing; festivals dedicated to gods and the pharaoh, e.g. the Sed festival (celebrating a king's 30th year on the throne).",
]:
    story.append(Paragraph(f"• {feat}", bullet_style))

# ── 9c. CHINESE ────────────────────────────────────────────────────────────
story.append(Paragraph("9c. Chinese Civilisation", h2_style))
story.append(Paragraph(
    "The Chinese civilisation flourished along the <b>Huang He (Yellow River)</b> and the <b>Yangtze</b>. "
    "Both river valleys were centres of early Neolithic cultures dating to ~<b>7000 BCE</b>. Around "
    "<b>2000 BCE</b>, copper/bronze metallurgy arrived. Urban centres began emerging only around "
    "<b>1600 BCE</b> with the first Chinese Bronze Age territorial empire.", body_style))

china_data = [
    ["Dynasty / Period", "Dates", "Key Features"],
    ["Neolithic cultures", "~7000 BCE", "Huang He and Yangtze river valley settlements; pottery; cultivation."],
    ["Bronze Age begins", "~2000 BCE", "Copper/bronze metallurgy; Neolithic settlements threshold Bronze Age."],
    ["Shang dynasty", "1600–1046 BCE", "First Chinese Bronze Age territorial empire. Jade objects (ritual and prestige items; jade carved into fish shapes — produced musical sound when struck). Bronze metallurgy for weapons, tools, ritual vessels. Oracle bones — symbols on animal bones and tortoise shells heated until cracked; cracks used to foretell the future. Earliest source of information about China."],
    ["Zhou dynasty", "1046–256 BCE", "Kings also priests; believed to be appointees of heaven but could be dismissed if people didn't prosper. Public officials chosen by examination in archery, horsemanship, calculations, writing, and music. Metal-based medium of exchange. Walls built from 680 BCE to protect against nomadic raids — precursor to the Great Wall."],
    ["Iron Age / Qin dynasty", "221–206 BCE", "Iron popular from ~600 BCE. 'China' probably comes from Qin (Ch'in). First imperial dynasty to unify China."],
    ["Han dynasty", "206 BCE–220 CE", "Silk became a major export item — the entire trade route became known as the 'Silk Route'. First country to introduce paper currency. First to develop civil services through public examination. Money economy developed by 5th century BCE."],
]
story.append(table(china_data, [3.5*cm, 3*cm, 9.5*cm], header_color=HexColor('#555555'),
    row_colors=[HexColor('#F5F5F5'), white]))
story.append(Spacer(1, 6))

story.append(Paragraph("Great Wall of China", h3_style))
story.append(Paragraph(
    "Built over ~2000 years. Several walls built from 680 BCE by Zhou and other dynasties as protection "
    "against violent raids by nomadic tribes. Later joined together to make an effective defence mechanism. "
    "Expansion and repair continued till the 17th century CE.", body_style))

story.append(Paragraph("Chinese Script", h3_style))
story.append(Paragraph(
    "The Chinese script is <b>logographic</b> — characters represent entire words or morphemes (smallest "
    "meaningful units of language), rather than sounds. Characters often resemble the objects or ideas "
    "they represent (e.g. person, tree).", body_style))

# ── 10. HOW CIVILISATIONS INTERACTED ──────────────────────────────────────
story.append(Paragraph("10. How Early Civilisations Interacted", h1_style))
story.append(Paragraph(
    "Major Bronze Age civilisations emerged independently in river plains but shared common features. "
    "The closest interaction was between the Mesopotamian and Harappan civilisations:", body_style))
for item in [
    "Akkadian king Sargon's tablets document trade with Dilmun (Bahrain), Magan (Oman), and <b>Meluhha</b> (generally identified as the Sindhu–Sarasvati civilisation).",
    "Goods traded with Harappans: semiprecious stone beads, ivory, timber, gold dust, and probably copper.",
    "Both civilisations developed irrigation infrastructure: Sumerians developed canal irrigation; Harappans built gabarbands (check dams) and the sophisticated water harvesting system at Dholavira.",
    "Cuneiform writing was contemporary with the Harappan script; unlike cuneiform, the Harappan script remains undeciphered.",
    "Egyptian and Chinese civilisations had little tangible direct contact with the Sindhu–Sarasvati civilisation.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

# ── 11. COMMON FEATURES OF BRONZE AGE CIVILISATIONS ───────────────────────
story.append(Paragraph("11. Common Features of Bronze Age Civilisations", h1_style))
common_data = [
    ["Feature", "Details"],
    ["River-valley origin", "All four emerged in fertile river plains: Sindhu–Sarasvati, Euphrates–Tigris, Nile, Huang He–Yangtze."],
    ["Agriculture", "Backbone of economy; irrigation was essential. Each civilisation developed unique irrigation solutions."],
    ["Urban centres", "Cities with planned layouts, administrative systems, and specialised crafts."],
    ["Writing systems", "All four developed writing systems to record transactions, laws, and social activities."],
    ["Trade", "Long-distance interregional trade networks linked these civilisations."],
    ["Social hierarchy", "Structured social systems with rulers at the top; priests, officials, artisans, farmers, and labourers."],
    ["Craft and metallurgy", "Pottery, metalworking, textiles, and construction were central crafts."],
    ["Religion", "Polytheistic belief systems; temples/religious structures were centres of socio-cultural and economic life."],
]
story.append(table(common_data, [4*cm, 12*cm], header_color=HexColor('#6A3C96'),
    row_colors=[HexColor('#F5EEF8'), white]))
story.append(Spacer(1, 6))

# ── 12. CONCLUSION ────────────────────────────────────────────────────────
story.append(Paragraph("12. Conclusion — Before We Move On", h1_style))
for pt in [
    "Early human history refers to the long period before writing; studied mainly through archaeological evidence: tools, fossils, and cave art.",
    "Early humans evolved in Africa and gradually migrated to different parts of the world.",
    "During the Palaeolithic period, humans were hunter-gatherers using stone tools (handaxes, cleavers, scrapers), living in caves or open camps.",
    "In the Mesolithic period, humans developed microlithic tools and began occupying temporary settlements near rivers and lakes.",
    "The Neolithic period marked a major shift to agriculture and domestication of animals, leading to permanent villages, pottery making, and weaving.",
    "The Chalcolithic period witnessed the use of copper along with stone tools and the growth of early farming communities.",
    "These developments led to the emergence of Bronze Age civilisations, characterised by urban centres, trade, writing, administration, and social organisation.",
    "Major early world civilisations — Sindhu–Sarasvati, Mesopotamia, Egypt, and China — developed independently in fertile river valleys and made significant contributions in agriculture, writing, architecture, administration, and culture.",
]:
    story.append(Paragraph(f"• {pt}", bullet_style))

story.append(Spacer(1, 12))
story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#AAAAAA'), spaceAfter=6))
story.append(Paragraph("End of Chapter 4 Summary", footer_style))

doc.build(story)
print("PDF created:", output_path)

