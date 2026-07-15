from flask import Flask, render_template, request, send_file
from decimal import Decimal, getcontext
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

app = Flask(__name__)

# -------------------------
# Pi Calculator
# -------------------------
def calculate_pi(digits):
    getcontext().prec = digits + 5

    C = 426880 * Decimal(10005).sqrt()

    M = 1
    L = 13591409
    X = 1
    K = 6
    S = Decimal(L)

    terms = digits // 14 + 1

    for i in range(1, terms):
        M = (M * (K**3 - 16 * K)) // (i**3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12

    return str(C / S)


# -------------------------
# Save TXT
# -------------------------
def create_txt(pi, digits):
    path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt"
    ).name

    with open(path, "w", encoding="utf-8") as file:
        file.write(f"Pi to {digits} digits\n\n")
        file.write(pi)

    return path


# -------------------------
# Save PDF
# -------------------------
def create_pdf(pi, digits):
    path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ).name

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    doc.build([
        Paragraph(f"<b>Pi to {digits} digits</b>", styles["Heading1"]),
        Paragraph(pi, styles["BodyText"])
    ])

    return path


# -------------------------
# Home
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    try:
        digits = int(request.form.get("digits", 0))
    except ValueError:
        return render_template(
            "index.html",
            error="Enter a valid number."
        )

    if digits < 1:
        return render_template(
            "index.html",
            error="Digits must be greater than zero."
        )

    if digits > 100000:
        return render_template(
            "index.html",
            error="Maximum allowed is 100000 digits."
        )

    filetype = request.form.get("filetype")

    pi = calculate_pi(digits)

    if filetype == "pdf":
        filepath = create_pdf(pi, digits)
        download_name = f"pi_{digits}.pdf"
    else:
        filepath = create_txt(pi, digits)
        download_name = f"pi_{digits}.txt"

    return send_file(
        filepath,
        as_attachment=True,
        download_name=download_name
    )


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)