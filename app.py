from flask import Flask, render_template, abort

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
    }
]

@app.route("/")
def home():
    return render_template("index.html", batches=BATCHES)

@app.route("/batches/<slug>")
def batch_page(slug):
    batch = next((b for b in BATCHES if b["slug"] == slug), None)
    if batch is None:
        abort(404)
    return render_template("batches/" + slug + ".html", batch=batch)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
