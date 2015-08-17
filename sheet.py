import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def get_above_fold():
    json_key = json.load(open('access.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key["client_email"], json_key['private_key'], scope)
    authorization = gspread.authorize(credentials)
    spreadsheet = authorization.open("Dorothy's List")
    worksheet = spreadsheet.get_worksheet(0)

    return worksheet.get_all_records()

def get_this_year():
    json_key = json.load(open('access.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key["client_email"], json_key['private_key'], scope)
    authorization = gspread.authorize(credentials)
    spreadsheet = authorization.open("Dorothy's List")
    worksheet = spreadsheet.get_worksheet(1)

    return worksheet.get_all_records()

def get_2013_2014():
    json_key = json.load(open('access.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key["client_email"], json_key['private_key'], scope)
    authorization = gspread.authorize(credentials)
    spreadsheet = authorization.open("Dorothy's List")
    worksheet = spreadsheet.get_worksheet(2)

    return worksheet.get_all_records()
