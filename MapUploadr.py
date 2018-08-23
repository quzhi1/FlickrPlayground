import csv
import json
import os
import webbrowser
from os.path import basename

import flickrapi

# Initialize flickrapi
with open('api_key.txt', 'r') as apiKeyFile:
    lines = apiKeyFile.readlines()
    api_key = lines[0].strip()
    api_secret = lines[1]
flickr = flickrapi.FlickrAPI(api_key, api_secret)

# Open csv file for output
if not os.path.exists('target'):
    os.makedirs('target')
TitleLookupTableFile = csv.writer(open("target/TitleLookupTableFile.csv", "w"))

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='write'):
    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='write')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

print('Step 2: Upload and write csv')
map_dir = '/Users/zhiqu/PersonalToolNodeJs/public/resources/map1/'
counter = 0
for file_name in os.listdir(map_dir):
    if file_name.endswith(".jpg"):
        resp = flickr.upload(filename=map_dir + file_name,
                             title=file_name,
                             description='East Asia Map of year ' + file_name[:-4])
        image_id = resp.findtext('photoid')
        json_res = flickr.photos.getSizes(photo_id=image_id, format='json')
        parsed_json = json.loads(json_res)
        size_list = parsed_json['sizes']['size']
        url = ''
        for size_item in size_list:
            if size_item['label'] == 'Original':
                url = size_item['source']
        TitleLookupTableFile.writerow([basename(file_name), image_id, url])
        counter += 1
        if counter % 10 == 0:
            print('Done uploading image (', counter, 'out of 2180)')
