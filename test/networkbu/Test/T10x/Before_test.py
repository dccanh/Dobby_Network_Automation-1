import sys
sys.path.append('../')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from Helper.t10x.config.read_config import *
from Helper.t10x.common import get_config

stage = get_config('GENERAL', 'stage')
version = get_config('GENERAL', 'version')
a = str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
sheet_name = stage + '_' + version + '_' +a
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('dn8c_cred.json', scope)
client = gspread.authorize(creds)

# Duplicate GG sheet
sheet = client.open("[DOB] Report Automation")
sheet.duplicate_sheet(source_sheet_id=2012030512, insert_sheet_index=1, new_sheet_name=sheet_name)

sheet = client.open("[DOB] Report Automation").get_worksheet(0)
# Update Start time
sheet.update_cell(5, 7, a)
sheet.update_cell(4, 7, stage)

# Update URL
sheet.update_cell(13, 5, url_login)
sheet.update_cell(12, 5, version)

third = sheet.update_cell(54, 5, sheet.cell(55, 5).value)
second = sheet.update_cell(55, 5, sheet.cell(56, 5).value)
first = sheet.update_cell(56, 5, sheet.cell(57, 5).value)
now = sheet.update_cell(57, 5, sheet_name)

# sheet0 = client.open("[VPEA] Report Automation").get_worksheet(0)
# sheet_name = sheet0.update_cell(3, 8, sheet_name)
