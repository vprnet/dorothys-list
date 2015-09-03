import markdown
import math
import arrow
from config import ABSOLUTE_PATH
from urllib import urlretrieve
from mutagen.mp3 import MP3
from sheet import get_above_fold, get_this_year, get_2013_2015
from query import generate_thumbnail


def above_the_fold():
    """Gets header content"""

    sheet_content = get_above_fold()
    content = {}
    content['headline'] = sheet_content[0]['Headline']
    content['image'] = sheet_content[0]['Picture URL']
    content['highlight'] = markdown.markdown(sheet_content[0]['Highlight'])
    paragraphs = sheet_content[0]['Copy'].split('++')
    content['copy'] = [markdown.markdown(par) for par in paragraphs]
    return content


def this_years_books():
    sheet_content = get_this_year()

    with open(ABSOLUTE_PATH + "main/audio.txt", "r+") as f:
        try:
            audio_lengths = eval(f.read())
        except SyntaxError:
            audio_lengths = {}

    for book in sheet_content:
        if book['Summary']:
            book['summary'] = markdown.markdown(book['Summary'])
        if book['Image URL']:
            book['imageurl'] = generate_thumbnail(book['Image URL'],
                preserve_ratio=True, size=(358, 358))
        if book['Air Date']:
            date_list = [int(x) for x in book['Air Date'].split('/')]
            date = arrow.get(date_list[2], date_list[0], date_list[1])
            book['Air Date'] = date
            book['date'] = date.format('dddd, MMMM, D')
            if (date - arrow.now()).days < 0:
                book['past'] = True
            else:
                book['past'] = False
        if book['Title']:
            book['title'] = book['Title']
        if book['Author']:
            book['author'] = book['Author']
        if book['Age Range']:
            book['agerange'] = book['Age Range']
        if book['Post URL']:
            book['posturl'] = book['Post URL']
        if book['Audio URL']:
            book['audiourl'] = book['Audio URL']
            url = book['audiourl']
            if url in audio_lengths and audio_lengths[url]:
                book['audiolength'] = audio_lengths[url]
            else:
                filename, headers = urlretrieve(url)
                audio = MP3(filename)
                book['audiolength'] = math.floor(audio.info.length)
            audio_lengths[url] = book['audiolength']

    with open(ABSOLUTE_PATH + "main/audio.txt", "w") as f:
        f.write(str(audio_lengths))

    sorted_books = sorted(sheet_content, key=lambda k: k['Air Date'])

    return sorted_books


def last_years_books():

    sheet_content = get_2013_2015()

    with open(ABSOLUTE_PATH + "main/audio.txt", "r+") as f:
        try:
            audio_lengths = eval(f.read())
        except SyntaxError:
            audio_lengths = {}


    for book in sheet_content:
        if book['Summary']:
            book['summary'] = markdown.markdown(book['Summary'])
        if book['Image URL']:
            book['imageurl'] = book['Image URL']
        if book['Air Date']:
            date_list = [int(x) for x in book['Air Date'].split('/')]
            date = arrow.get(date_list[2], date_list[0], date_list[1])
            book['Air Date'] = date
            book['date'] = date.format('dddd, MMMM, D')
            if (date - arrow.now()).days < 0:
                book['past'] = True
            else:
                book['past'] = False
        if book['Title']:
            book['title'] = book['Title']
        if book['Author']:
            book['author'] = book['Author']
        if book['Post URL']:
            book['posturl'] = book['Post URL']
        if book['Audio URL']:
            book['audiourl'] = book['Audio URL']
            url = book['audiourl']
            if url in audio_lengths and audio_lengths[url]:
                book['audiolength'] = audio_lengths[url]
            else:
                filename, headers = urlretrieve(url)
                audio = MP3(filename)
                book['audiolength'] = math.floor(audio.info.length)
            audio_lengths[url] = book['audiolength']

    with open(ABSOLUTE_PATH + "main/audio.txt", "w") as f:
        f.write(str(audio_lengths))

    sorted_books = sorted(sheet_content, key=lambda k: k['Air Date'])


    return sorted_books
