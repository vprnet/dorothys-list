import markdown
import math
import arrow
from config import ABSOLUTE_PATH
from urllib import urlretrieve
from mutagen.mp3 import MP3
from sheet import get_google_sheet
from query import generate_thumbnail

SPREADSHEET_KEY = '19qKia2C2WKgQs4qbez_WHDoX1yVm6vvCDjXhJJyh8fo'


def above_the_fold():
    """Gets header content"""

    sheet_content = get_google_sheet(SPREADSHEET_KEY)[0]
    content = {}
    content['headline'] = sheet_content['headline']
    content['image'] = sheet_content['pictureurl']
    content['highlight'] = markdown.markdown(sheet_content['highlight'])
    paragraphs = sheet_content['copy'].split('++')
    content['copy'] = [markdown.markdown(par) for par in paragraphs]
    return content


def this_years_books():
    sheet_content = get_google_sheet(SPREADSHEET_KEY, sheet_id='o9170sw')

    with open(ABSOLUTE_PATH + "main/audio.txt", "r+") as f:
        try:
            audio_lengths = eval(f.read())
        except SyntaxError:
            audio_lengths = {}

    for book in sheet_content:
        if book['summary']:
            book['summary'] = markdown.markdown(book['summary'])
        if book['imageurl']:
            book['imageurl'] = generate_thumbnail(book['imageurl'],
                preserve_ratio=True, size=(358, 358))
        if book['airdate']:
            date_list = [int(x) for x in book['airdate'].split('/')]
            date = arrow.get(date_list[2], date_list[0], date_list[1])
            book['airdate'] = date
            book['date'] = date.format('dddd, MMMM, D')
            if (date - arrow.now()).days < 0:
                book['past'] = True
            else:
                book['past'] = False
        if book['audiourl']:
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

    sorted_books = sorted(sheet_content, key=lambda k: k['airdate'])

    return sorted_books


def last_years_books():
    sheet_content = get_google_sheet(SPREADSHEET_KEY, sheet_id='ou6a4hm')

    for book in sheet_content:
        book['summary'] = markdown.markdown(book['summary'])
        if book['airdate']:
            date_list = [int(x) for x in book['airdate'].split('/')]
            date = arrow.get(date_list[2], date_list[0], date_list[1])
            if (date - arrow.now()).days < 0:
                book['past'] = True
            else:
                book['past'] = False

    return sheet_content