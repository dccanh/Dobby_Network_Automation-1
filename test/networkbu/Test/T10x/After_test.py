import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

a = str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M'))

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('dn8c_cred.json', scope)
client = gspread.authorize(creds)

sheet = client.open("[DOB] Report Automation").get_worksheet(0)
# Update Report Release Date
sheet.update_cell(7, 7, a)
