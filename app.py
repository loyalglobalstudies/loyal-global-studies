from flask import Flask, render_template, abort, send_from_directory

app = Flask(__name__)

BATCHES = [
    {
        "slug": "bihar-stet",
        "name": "Bihar STET",
        "description": "Hindi-medium practice tests and exam preparation.",
        "category": "Teaching Exams"
    },
    {
        "slug": "upsssc-pet",
        "name": "UPSSSC PET",
        "description": "General Studies and PET exam practice.",
        "category": "State Exams"
    },
    {
        "slug": "rrb-ntpc-rajdhani",
        "name": "RRB NTPC Rajdhani",
        "description": "Railway exam preparation and batch information.",
        "category": "Railway Exams"
    },
    {
        "slug": "python-course",
        "name": "Python Programming",
        "description": "Learn Python programming step by step.",
        "category": "Computer Courses"
    },
    {
        "slug": "rrb-station-master-rail-nayak",
        "name": "RRB Station Master — रेल नायक",
        "description": "Online Hindi Medium Railway Batch 2026.",
        "category": "Railway Exams"
    },
    {
        "slug": "upsc-3-year-foundation",
        "name": "UPSC (3 Year) Foundation Batch — Hindi Medium",
        "description": "Three-year Hindi-medium UPSC Civil Services foundation course.",
        "category": "UPSC"
    },
    {
        "slug": "uppsc-ro-aro-2026",
        "name": "UPPSC RO/ARO 2026 — Pre + Mains Foundation",
        "description": "Prelims and Mains foundation preparation for UPPSC RO/ARO.",
        "category": "State Exams"
    },
    {
        "slug": "bpsc-tre-4",
        "name": "BPSC TRE 4.0 — Class 9–10 & 11–12",
        "description": "Bilingual Bihar teacher recruitment exam preparation.",
        "category": "Teaching Exams"
    },
    {
        "slug": "up-tgt-udan-science",
        "name": "UP TGT उड़ान बैच (SCIENCE)",
        "description": "Physics, Biology, Computer and Geography preparation.",
        "category": "Teaching Exams"
    },

    {
        "slug": "army-gd-tradesman",
        "name": "Army GD & Tradesman Batch",
        "description": "Army GD और Tradesman परीक्षा की bilingual online batch information.",
        "category": "Defence Exams"
    },
    {
        "slug": "biology-foundation-4-amrita",
        "name": "Biology Foundation Batch 4.0 — Amrita Ma’am",
        "description": "Live bilingual Biology foundation batch with 5 free mock tests.",
        "category": "Teaching Exams"
    },
]

@app.route("/")
def home():
    return render_template("index.html", batches=BATCHES)

@app.route("/batches/upsssc-pet-<int:year>.html")
def pet_year_page(year):
    if year not in (2021, 2022, 2023, 2024, 2025):
        abort(404)

    filename = f"pet{year}.html"
    return send_from_directory("static/legacy", filename)



@app.route("/batches/bihar-stet-full-exam.html")
def bihar_stet_full_exam():
    return send_from_directory("static/legacy", "bihar-stet-full-exam.html")


@app.route("/batches/bihar-stet-2024-practice.html")
def bihar_stet_2024_practice():
    return send_from_directory("static/legacy", "bihar-stet-2024-practice.html")


@app.route("/batches/<slug>")
def batch_page(slug):
    batch = next((b for b in BATCHES if b["slug"] == slug), None)
    if batch is None:
        abort(404)
    return render_template("batches/" + slug + ".html", batch=batch)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
