from flask import Flask, render_template, abort, send_from_directory

app = Flask(__name__)

# LOYAL_SECURITY_HEADERS_V1
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )
    response.headers["Content-Security-Policy-Report-Only"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-src https://www.youtube-nocookie.com; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response



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
        "slug": "stylish-photo-pose",
        "name": "Stylish Photo Pose Batch",
        "description": "Best Photo Poses, Stylish Attitude और Professional Look सीखें।",
        "category": "Creative Skills"
    },
    {
        "slug": "biology-foundation-4-amrita",
        "name": "Biology Foundation Batch 4.0 — Amrita Ma’am",
        "description": "Live bilingual Biology foundation batch with 5 free mock tests.",
        "category": "Teaching Exams"
    },
    {
        "slug": "upsc-crash-course-2026",
        "name": "UPSC Crash Course 2026 — KGS",
        "description": "KGS UPSC Crash Course 2026 की जानकारी और मूल कोर्स पेज।",
        "category": "UPSC"
    },
    {
        "slug": "up-si-2026-27",
        "name": "UP SI 2026–27 Offline Batch — Prayagraj",
        "description": "Offline Hindi-medium UP SI preparation. Fee ₹6,500.",
        "category": "State Exams"
    },
    {
        "slug": "economics-foundation",
        "name": "Economics Foundation by Khan Sir",
        "description": "Economics Foundation Batch. Fee ₹200.",
        "category": "UPSC"
    },
    {
        "slug": "history-foundation",
        "name": "History Foundation by Khan Sir",
        "description": "History Foundation Batch. Fee ₹200.",
        "category": "UPSC"
    },
    {
        "slug": "jee-2027-dropper-phase-2",
        "name": "JEE 2027 Dropper Yearlong Offline Batch — Phase II, Prayagraj",
        "description": "JEE 2027 Dropper Yearlong Batch. Offline bilingual classroom in Prayagraj.",
        "category": "Engineering Exams"
    },
    {
        "slug": "upsc-hindi-literature-optional",
        "name": "UPSC Hindi Literature Optional Paper — Online Batch",
        "description": "UPSC Hindi Literature Optional Paper preparation batch.",
        "category": "UPSC"
    },
    {
        "slug": "bpsc-73-foundation-11",
        "name": "73rd BPSC Foundation Batch 11 — Musallahpur",
        "description": "73rd BPSC Foundation Batch 11 for Prelims, Mains and Interview preparation.",
        "category": "State Exams"
    },
    {
        "slug": "upsc-foundation-2028-online",
        "name": "UPSC Foundation Batch 2028 — Hindi Medium (Online)",
        "description": "UPSC Foundation 2028 Hindi-medium online preparation for Prelims and Mains.",
        "category": "UPSC"
    },
    {
        "slug": "upsc-foundation-2028-offline-delhi",
        "name": "UPSC Pre + Mains Foundation Batch 2028 — Hindi Medium",
        "description": "UPSC Prelims and Mains Foundation Batch 2028, offline Azadpur centre.",
        "category": "UPSC"
    },
    {
        "slug": "sbi-po-clerk-target-2026",
        "name": "SBI PO/Clerk (Pre + Mains) Target Batch 2026",
        "description": "Bilingual SBI PO and Clerk Target Batch 2026.",
        "category": "Banking Exams"
    },
    {
        "slug": "super-tet-primary-2026",
        "name": "Super TET Primary Teacher Batch 2026",
        "description": "Super TET 2026 preparation for Primary Teacher recruitment.",
        "category": "Teaching Exams"
    },
    {
        "slug": "rrb-group-d-rail-sarthi-2026",
        "name": "RRB Group D — रेल सारथी बैच 2026",
        "description": "RRB Group D Rail Sarthi Batch 2026, Hindi-medium railway preparation.",
        "category": "Railway Exams"
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



@app.route("/sw.js")
def loyal_service_worker():
    response = send_from_directory(
        "static", "sw.js", mimetype="application/javascript"
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Service-Worker-Allowed"] = "/"
    return response




@app.route("/.well-known/assetlinks.json")
def loyal_assetlinks():
    response = send_from_directory(
        "static/.well-known",
        "assetlinks.json",
        mimetype="application/json"
    )
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
