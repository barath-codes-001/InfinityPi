from flask import Flask, render_template, request, send_file
import gmpy2
from gmpy2 import mpfr, get_context
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os

app = Flask(__name__)

# -----------------------------
# Pi Calculation (Chudnovsky)
# -----------------------------
def calculate_pi(digits):
    bits = int(digits * 3.32192809489) + 100
    get_context().precision = bits

    C = 426880 * gmpy2.sqrt(mpfr(10005))

    M = 1
    L = 13591409
    X = 1
    K = 6
    S = mpfr(L)

    terms = digits // 14 + 1

    for i in range(1, terms):
        M = (M * (K**3 - 16 * K)) // (i**3)
        L += 545140134
        X *= -262537412640768000
        S += mpfr(M * L) / X
        K += 12

    return str(C / S)


# -----------------------------
# Home Page
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        try:
            digits = int(request.form["digits"])

            if digits <= 0:
                return render_template(
                    "index.html",
                    error="Please enter a number greater than 0."
                )

            pi = calculate_pi(digits)

            file_type = request.form["filetype"]

            if file_type == "txt":

                filename = f"pi_{digits}_digits.txt"

                with open(filename, "w") as f:
                    f.write(pi)

                return send_file(
                    filename,
                    as_attachment=True
                )

            elif file_type == "pdf":

                filename = f"pi_{digits}_digits.pdf"

                doc = SimpleDocTemplate(filename)
                styles = getSampleStyleSheet()

                story = []

                story.append(
                    Paragraph(
                        f"<b>Pi to {digits} Digits</b>",
                        styles["Heading1"]
                    )
                )

                story.append(
                    Paragraph(
                        pi,
                        styles["BodyText"]
                    )
                )

                doc.build(story)

                return send_file(
                    filename,
                    as_attachment=True
                )

        except Exception as e:
    import traceback
    traceback.print_exc()   # This prints the full error to Render logs

    return render_template(
        "index.html",
        error=f"{type(e).__name__}: {e}"
    )

    return render_template("index.html")


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)