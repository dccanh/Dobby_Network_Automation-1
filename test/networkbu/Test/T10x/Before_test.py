import sys
sys.path.append('../../')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from Helper.t10x.config.read_config import *
from Helper.t10x.common import get_config, save_config
from Helper.t10x.ls_path import *

url = get_config('URL', 'url')
stage = get_config('GENERAL', 'stage')
version = get_config('GENERAL', 'version')
a = str(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
sheet_name = stage + '_' + version + '_' + a
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(gg_credential_path, scope)
client = gspread.authorize(creds)

# Duplicate GG sheet
sheet = client.open("[DOB] Report Automation")
sheet.duplicate_sheet(source_sheet_id=2012030512, insert_sheet_index=1, new_sheet_name=sheet_name)

sheet = client.open("[DOB] Report Automation").get_worksheet(0)


# Update Start time
sheet.update_cell(5, 7, a)
sheet.update_cell(4, 7, stage)

# Update URL
sheet.update_cell(13, 5, url)
sheet.update_cell(12, 5, version)

sheet_title = client.open("[DOB] Report Automation")
third = sheet.update_cell(54, 5, sheet_title.get_worksheet(4).title)
second = sheet.update_cell(55, 5, sheet_title.get_worksheet(3).title)
first = sheet.update_cell(56, 5, sheet_title.get_worksheet(2).title)
now = sheet.update_cell(57, 5, sheet_title.get_worksheet(1).title)


# Save google sheet name
save_config(config_path, 'REPORT', 'sheet_name', sheet_name)