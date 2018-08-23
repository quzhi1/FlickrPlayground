import webbrowser

import flickrapi

with open('api_key.txt', 'r') as apiKeyFile:
    lines = apiKeyFile.readlines()
    api_key = lines[0].strip()
    api_secret = lines[1]

flickr = flickrapi.FlickrAPI(api_key, api_secret)

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

print('Step 2: use Flickr')
resp = flickr.upload(filename='Seal.jpg', title='Seal', description='A picture of seal toy')
image_id = resp.findtext('photoid')
print('Image id', image_id)
