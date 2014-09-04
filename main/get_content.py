import markdown
import math
import arrow
from urllib import urlretrieve
from mutagen.mp3 import MP3
from sheet import get_google_sheet

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


def last_years_books():
    sheet_content = get_google_sheet(SPREADSHEET_KEY, sheet_id='ou6a4hm')
    with open("main/audio.txt", "r+") as f:
        audio_lengths = eval(f.read())
        audio_dict = {}
        for book in sheet_content:
            book['summary'] = markdown.markdown(book['summary'])
            url = book['audiourl']
            if book['airdate']:
                date_list = [int(x) for x in book['airdate'].split('/')]
                date = arrow.get(date_list[2], date_list[0], date_list[1])
                if (date - arrow.now()).days < 0:
                    book['past'] = True
                else:
                    book['past'] = False
            if url in audio_lengths and audio_lengths[url]:
                book['audiolength'] = audio_lengths[url]
            else:
                filename, headers = urlretrieve(url)
                audio = MP3(filename)
                book['audiolength'] = math.floor(audio.info.length)
            audio_dict[url] = book['audiolength']
        f.seek(0)
        f.write(str(audio_dict))
    return sheet_content
