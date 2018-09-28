#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.request import Request
import json
import sys
from datetime import datetime 

#URL = "https://www.asus.com/Networking/RTAC66U/HelpDesk_BIOS/"
URL = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=global&pdhashedid=LzShv8ma7TrQB4eO&model=RT-AC66U&callback=supportpdpage"

def parse_firmware_version_info(jsonstr):
    data = json.loads(jsonstr)
    if data['Status'] == 'SUCCESS':
        objects = data['Result']['Obj']
        firmwareSets = [o['Files'] for o in objects if o['Name'] == 'Firmware']
        releasedate_and_titles = [(f['ReleaseDate'], f['Title']) for fs in firmwareSets for f in fs]
        releases = get_todays_releases(releasedate_and_titles)
        if releases != []:
            print(releases)
    else:
        print('Got Error response from server')
        sys.exit(1)

def get_todays_releases(date_and_titles):
    today = datetime.today().date()
    return [dt for dt in date_and_titles if datetime.strptime(dt[0], '%Y/%m/%d').date() == today]

if __name__ == '__main__':
    r = Request(URL, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'})
    response = urlopen(r)
    jsonstr = response.read().decode('utf-8').replace('supportpdpage(', '', 1)[:-1]
    parse_firmware_version_info(jsonstr)

