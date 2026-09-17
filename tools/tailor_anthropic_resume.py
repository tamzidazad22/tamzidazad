from copy import deepcopy
from pathlib import Path
from shutil import copy2

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph


SOURCE = Path(
    "/Users/tamzidazad/Documents/2026/Resume 2026/Low commitment roles/"
    "Tamzid_Azad_Entrepreneurship_Ecosystem_Resume_2026.docx"
)
OUTPUT = Path(
    "/Users/tamzidazad/Documents/My Website/output/applications/anthropic/"
    "Tamzid_Azad_Startup_Partnerships_Lead_Anthropic.docx"
)

FONT_FAMILY = "Baskerville"


REPLACEMENTS = {
    "ENTREPRENEURSHIP ECOSYSTEM BUILDER | INCUBATORS | STARTUP PARTNERSHIPS | EDUCATOR":
        "STARTUP PARTNERSHIPS | ACCELERATORS | ECOSYSTEM PROGRAMS | TECHNOLOGY OPERATOR",
    "Entrepreneurship ecosystem builder, educator, and technology operator with 10+ years across university venture programs, corporate innovation, and scaling businesses. Founding team member of Schulich Startups; led partnerships with the City of Toronto, Microsoft, Google, and Shopify; designed an internal incubator for 2,500 employees; and coached founders from early ideas toward product-market fit. Brings hands-on zero-to-one, commercialization, and partnership experience to help entrepreneurs build with discipline.":
        "Startup partnerships and ecosystem leader with 10+ years across university venture programs, corporate innovation, and scaled technology. Founding team member of Schulich Startups; built programs with the City of Toronto, Microsoft, Google, and Shopify; designed a 2,500-employee incubator; and supported founders through validation and commercialization. Combines ecosystem relationships with hands-on product, GTM, and technical enablement experience.",
    "CORE STRENGTHS: INCUBATOR DESIGN | FOUNDER COACHING | UNIVERSITY-INDUSTRY PARTNERSHIPS | VENTURE PROGRAMMING | COMMERCIALIZATION":
        "CORE STRENGTHS: STARTUP PARTNERSHIPS | ACCELERATOR PROGRAMS | FOUNDER ENABLEMENT | CROSS-FUNCTIONAL GTM | PRODUCT ADOPTION",
    "Design and deliver applied learning in communication, industry engagement, and career strategy, using guest speakers, panels, simulations, and one-to-one coaching to connect students with practice.":
        "Design and deliver applied learning for business and technical audiences through workshops, simulations, guest speakers, panels, and coaching across entrepreneurship, product, innovation, fintech, and AI.",
    "Designed training platforms and built industry collaborations supporting 150+ student-led startups with founder development, mentorship, and ecosystem access.":
        "Designed founder programs and industry collaborations supporting 150+ student-led startups with training, mentorship, ecosystem access, and product feedback.",
    "Managed the Digital Main Street partnership with the City of Toronto, Microsoft, Google, and Shopify, helping 500+ small businesses adopt digital tools during COVID-19.":
        "Managed the Digital Main Street partnership across the City of Toronto, Microsoft, Google, and Shopify, helping 500+ small businesses adopt digital tools during COVID-19.",
    "Designed the platform, methodologies, toolkits, roadshows, and partnership model for an internal incubator launched to 2,500 employees.":
        "Designed and launched the program model, partner approach, toolkits, and roadshows for an internal incubator reaching 2,500 employees.",
    "Set strategy for a CAD 2B payments portfolio, launched Jonas Pay, designed cross-functional operating processes, and grew Mobile POS adoption by 90 clients in eight months.":
        "Set strategy for a CAD 2B payments portfolio, launched Jonas Pay, and enabled sales, implementation, and support teams with operating processes and technical-product training; grew Mobile POS by 90 clients in eight months.",
    "Led a cross-functional product team and payment partnerships that delivered approximately 200% year-over-year growth to 600K monthly transactions across digital hospitality platforms.":
        "Led a cross-functional product team and payment-partner integrations that delivered approximately 200% year-over-year growth to 600K monthly transactions across digital hospitality platforms.",
    "Led the student entrepreneurship community as President of Schulich Ventures Club (2020-2021), creating a home for aspiring founders and venture-minded students.":
        "President, Schulich Ventures Club (2020-2021); managed ProductTank Dhaka within a 200+ city global community; founded and ran a public-speaking training organization (2013-2018).",
}

REMOVALS = {
    "Develop workshops and practical programming across entrepreneurship, product, innovation, fintech, and AI.",
    "Managed the ProductTank Dhaka chapter within a global product community spanning 200+ cities; founded and managed a public-speaking training organization from 2013 to 2018.",
}

ROLE_LINES = {
    "DOODLEPAD | Founder\tToronto | 2025 - Present":
        ("Founder", "DOODLEPAD", "Toronto | 2025 - Present"),
    "SCHULICH SCHOOL OF BUSINESS, YORK UNIVERSITY | Instructor (part-time)\tToronto | Jan 2026 - Present":
        ("Instructor (part-time)", "SCHULICH SCHOOL OF BUSINESS", "Toronto | Jan 2026 - Present"),
    "SCHULICH STARTUPS, SCHULICH SCHOOL OF BUSINESS | Founding Team Member & Program Manager\tToronto | Dec 2019 - Jan 2021":
        ("Founding Team Member & Program Manager", "SCHULICH STARTUPS", "Toronto | Dec 2019 - Jan 2021"),
    "TELENOR GROUP / GRAMEENPHONE | Product Lead, New Business Innovation\tNorway & Bangladesh | Nov 2016 - Aug 2019":
        ("Product Lead, New Business Innovation", "TELENOR GROUP / GRAMEENPHONE", "Norway & Bangladesh | Nov 2016 - Aug 2019"),
    "JONAS SOFTWARE, CONSTELLATION SOFTWARE | Senior Product Manager, POS & Payments\tToronto | Feb 2024 - Apr 2026":
        ("Senior Product Manager, POS & Payments", "JONAS SOFTWARE, CONSTELLATION SOFTWARE", "Toronto | Feb 2024 - Apr 2026"),
    "COMPASS DIGITAL, COMPASS GROUP | Product Manager, Checkout & Payments\tToronto | Dec 2021 - Jan 2024":
        ("Product Manager, Checkout & Payments", "COMPASS DIGITAL, COMPASS GROUP", "Toronto | Dec 2021 - Jan 2024"),
    "ROBI AXIATA | Product Manager, Internet of Things & Digital Services\tBangladesh | Aug 2015 - Nov 2016":
        ("Product Manager, Internet of Things & Digital Services", "ROBI AXIATA", "Bangladesh | Aug 2015 - Nov 2016"),
}


def replace_paragraph_text(paragraph, value):
    if not paragraph.runs:
        paragraph.add_run(value)
        return
    paragraph.runs[0].text = value
    for run in paragraph.runs[1:]:
        run.text = ""


def remove_paragraph(paragraph):
    element = paragraph._element
    element.getparent().remove(element)
    paragraph._p = paragraph._element = None


def apply_font(run, font_name=FONT_FAMILY):
    run.font.name = font_name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font_name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font_name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), font_name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:cs"), font_name)


def rewrite_role_line(paragraph, title, company, location_date):
    for run in paragraph.runs:
        run.text = ""
    title_run = paragraph.add_run(title)
    title_run.bold = True
    company_run = paragraph.add_run(f" | {company}")
    company_run.bold = True
    date_run = paragraph.add_run(f"\t{location_date}")
    date_run.bold = False
    for run in (title_run, company_run, date_run):
        apply_font(run)
    paragraph.paragraph_format.tab_stops.clear_all()
    paragraph.paragraph_format.tab_stops.add_tab_stop(
        Inches(7.36), WD_TAB_ALIGNMENT.RIGHT
    )


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
copy2(SOURCE, OUTPUT)
document = Document(OUTPUT)

seen = set()
removed = set()
for paragraph in list(document.paragraphs):
    original = paragraph.text
    if original in REPLACEMENTS:
        replace_paragraph_text(paragraph, REPLACEMENTS[original])
        seen.add(original)
    elif original in REMOVALS:
        remove_paragraph(paragraph)
        removed.add(original)

missing = set(REPLACEMENTS) - seen
if missing:
    raise RuntimeError(f"Expected paragraphs were not found: {sorted(missing)}")

missing_removals = REMOVALS - removed
if missing_removals:
    raise RuntimeError(f"Expected paragraphs were not found for removal: {sorted(missing_removals)}")

schulich_role = next(
    paragraph
    for paragraph in document.paragraphs
    if paragraph.text.startswith("SCHULICH SCHOOL OF BUSINESS, YORK UNIVERSITY")
)
schulich_role.insert_paragraph_before(
    "DOODLEPAD | Founder\tToronto | 2025 - Present",
    style="Resume Role",
)
schulich_bullet = next(
    paragraph
    for paragraph in document.paragraphs
    if paragraph.text.startswith("Design and deliver applied learning")
)
doodlepad_bullet_xml = deepcopy(schulich_bullet._p)
schulich_role._p.addprevious(doodlepad_bullet_xml)
doodlepad_bullet = Paragraph(doodlepad_bullet_xml, schulich_role._parent)
replace_paragraph_text(
    doodlepad_bullet,
    "Building an operating system for homeschooling families and microschools that connects curriculum planning, resources, student practice, and progress tracking into personalized learning journeys; launched an initial product and attracted early adopters.",
)
doodlepad_recognition_xml = deepcopy(schulich_bullet._p)
schulich_role._p.addprevious(doodlepad_recognition_xml)
doodlepad_recognition = Paragraph(doodlepad_recognition_xml, schulich_role._parent)
replace_paragraph_text(
    doodlepad_recognition,
    "Selected for the YSpace Incubator and Google for Startups ($25K in credits); 2026 Schulich Startup Night alumni finalist and recipient of the YSpace Rising Star and Zeifmans Acceler8 awards.",
)

seen_roles = set()
for paragraph in document.paragraphs:
    original_role_line = paragraph.text
    if original_role_line in ROLE_LINES:
        rewrite_role_line(paragraph, *ROLE_LINES[original_role_line])
        seen_roles.add(original_role_line)

missing_roles = set(ROLE_LINES) - seen_roles
if missing_roles:
    raise RuntimeError(f"Expected role lines were not found: {sorted(missing_roles)}")

for style in document.styles:
    if hasattr(style, "font"):
        style.font.name = FONT_FAMILY
        style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), FONT_FAMILY)
        style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), FONT_FAMILY)
        style._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FONT_FAMILY)
        style._element.get_or_add_rPr().rFonts.set(qn("w:cs"), FONT_FAMILY)

for paragraph in document.paragraphs:
    for run in paragraph.runs:
        apply_font(run)

compact_styles = {
    "Normal": 9.25,
    "Resume Role": 9.25,
    "Resume Bullet": 9.25,
    "Resume Compact": 9.25,
}
for style_name, font_size in compact_styles.items():
    document.styles[style_name].font.size = Pt(font_size)

document.styles["Resume Role"].paragraph_format.space_before = Pt(3.25)
document.styles["Resume Role"].paragraph_format.space_after = Pt(1)
document.styles["Resume Bullet"].paragraph_format.space_after = Pt(1.5)
document.styles["Resume Section"].paragraph_format.space_before = Pt(7.5)
document.styles["Resume Section"].paragraph_format.space_after = Pt(4.5)
document.styles["Resume Compact"].paragraph_format.space_after = Pt(1.5)

for paragraph in document.paragraphs:
    if paragraph.style.name in compact_styles:
        for run in paragraph.runs:
            run.font.size = Pt(compact_styles[paragraph.style.name])

document.core_properties.title = "Tamzid Azad - Startup Partnerships Lead - Anthropic"
document.core_properties.subject = "Tailored resume for Anthropic Startup Partnerships Lead"
document.save(OUTPUT)
print(OUTPUT)
