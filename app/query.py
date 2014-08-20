#!/usr/bin/python
import markdown
import math
from urllib import urlretrieve
from mutagen.mp3 import MP3
from google_spreadsheet.api import SpreadsheetAPI
from config import GOOGLE_SPREADSHEET


def list_sheets(key=False):
    """The API sheet_key is not the same as the key in the URL. This function
    just prints out all sheet keys"""
    api = SpreadsheetAPI(GOOGLE_SPREADSHEET['USER'],
        GOOGLE_SPREADSHEET['PASSWORD'],
        GOOGLE_SPREADSHEET['SOURCE'])
    spreadsheets = api.list_spreadsheets()
    if key:
        worksheets = api.list_worksheets(key)
        print worksheets
    else:
        for sheet in spreadsheets:
            print sheet


def get_google_sheet(sheet_key=False, sheet_id='od6'):
    """Uses python_google_spreadsheet API to interact with sheet"""
    api = SpreadsheetAPI(GOOGLE_SPREADSHEET['USER'],
        GOOGLE_SPREADSHEET['PASSWORD'],
        GOOGLE_SPREADSHEET['SOURCE'])
    sheet = api.get_worksheet(sheet_key, sheet_id)
    sheet_object = sheet.get_rows()
    return sheet_object


def above_the_fold():
    sheet_content = get_google_sheet(sheet_key=GOOGLE_SPREADSHEET['KEY'])[0]
    content = {}
    content['headline'] = sheet_content['headline']
    content['image'] = sheet_content['pictureurl']
    content['highlight'] = markdown.markdown(sheet_content['highlight'])
    paragraphs = sheet_content['copy'].split('++')
    content['copy'] = [markdown.markdown(par) for par in paragraphs]
    return content


def last_years_books():
    sheet_content = get_google_sheet(sheet_key=GOOGLE_SPREADSHEET['KEY'],
        sheet_id='ou6a4hm')
    with open("app/audio.txt", "r+") as f:
        audio_lengths = eval(f.read())
        audio_dict = {}
        for book in sheet_content:
            book['summary'] = markdown.markdown(book['summary'])
            url = book['audiourl']
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
