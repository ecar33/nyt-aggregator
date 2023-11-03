from flask import render_template, request, url_for, Flask, redirect
import nytimes as nyt
import os
import re

app = Flask(__name__)
os.environ["FLASK_DEBUG"] = "1"


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/select_function", methods=["GET", "POST"])
def select_function():
    user_choice = request.form.get('choice')
    if user_choice == "article_search":
        return redirect(url_for("article_search"))

    elif user_choice == "top_stories":
        return redirect(url_for("top_stories"))

    elif user_choice == "bestselling_books":
        return redirect(url_for("bestselling_books"))
    else:
        return "<p>Something went wrong.</p>"


@app.route("/article_search")
def article_search():
    return "Welcome to article search"


@app.route("/top_stories")
def top_stories():
    return "Welcome to top stories"


@app.route("/bestselling_books")
def bestselling_books():
    return render_template("bestselling_books.html")


# Route for processing bestselling_books input and returning data
@app.route("/process_bestselling_books", methods=["GET", "POST"])
def process_bestselling_books():
    date = request.form.get('date', None)
    genre = request.form.get('genre', None)

    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if date is not None and genre is not None and date_pattern.fullmatch(date):
        books, error = nyt.bestseller_overview_search(date, genre)
        if error:
            return render_template("bestselling_books.html", error=error.r.status_code)
        else:
            return render_template("processed_bestselling_books.html", books=books, date=date, genre=genre)

    else:
        empty = True
        return render_template("bestselling_books.html", empty=empty)


if __name__ == "__main__":
    app.run(debug=True)
