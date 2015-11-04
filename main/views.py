from main import app
from flask import render_template, request
from get_content import above_the_fold, this_years_books, last_years_books
from config import FREEZER_BASE_URL


@app.route('/')
def index():
    page_title = "#DorothysList"
    page_url = FREEZER_BASE_URL.rstrip('/') + request.path
    above_fold = above_the_fold()
    new_books = this_years_books()
    old_books = last_years_books()

    social = {
        'title': "Dorothy's List",
        'subtitle': "VPR's Book Club For Kids",
        'img': 'http://mediad.publicbroadcasting.net/p/vpr/files/201510/dorothy-facebook-image.jpeg',
        'description': "Each month VPR highlights a book nominated for the Dorothy Canfield Fisher Children's Book Award.",
        'twitter_text': "Read along with Dorothy's List, a VPR book club for kids:",
        'twitter_hashtag': 'books,reading'
    }

    return render_template('content.html',
        page_url=page_url,
        page_title=page_title,
        social=social,
        above_fold=above_fold,
        new_books=new_books,
        old_books=old_books)
