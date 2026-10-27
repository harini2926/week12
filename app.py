from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()

        # Validate all fields
        if not name or not email or not course:
            return render_template(
                "register.html",
                error="Please fill in all fields."
            )

        # Redirect to success page
        return redirect(
            url_for(
                "success",
                name=name,
                email=email,
                course=course
            )
        )

    return render_template("register.html")


@app.route("/success")
def success():
    name = request.args.get("name", "Unknown")
    email = request.args.get("email", "Not provided")
    course = request.args.get("course", "Not provided")

    return render_template(
        "success.html",
        name=name,
        email=email,
        course=course
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)