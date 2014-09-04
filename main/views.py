from main import app
from flask import render_template
from get_content import above_the_fold, last_years_books


@app.route('/')
def index():
    page_title = "#DorothysList"
    above_fold = above_the_fold()
    old_books = last_years_books()

    social = {
        'title': "Dorothy's List",
        'subtitle': "VPR's Book Club For Kids",
        'img': 'http://www.vpr.net/apps/dorothys-list/static/img/dorothys-list-collage.png',
        'description': "Each month VPR highlights a book nominated for the Dorothy Canfield Fisher Children's Book Award.",
        'twitter_text': "Read along with Dorothy's List, a VPR book club for kids:",
        'twitter_hashtag': 'books,reading'
    }

    return render_template('content.html',
        page_title=page_title,
        social=social,
        above_fold=above_fold,
        old_books=old_books)
