import requests

# Define the OAuth2 credentials
client_id = '173313288818-ffl1o43k50drnqb6lf8v8jikee0tooqs.apps.googleusercontent.com'
client_secret = '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'
redirect_uri = 'https://accounts.google.com/o/oauth2/token'

# Define the authorization code you received from the OAuth2 authentication process
authorization_code = '4%2F0AfJohXkKnfnFE_q4XoJea5MCoojqnvb2PeH2M5aOZENr6yeoxtdHRHLG_4GAEWFRhPixMQ'

# Define the URL for token exchange
token_url = 'https://accounts.google.com/o/oauth2/token'

# Prepare the data for the POST request
payload = {
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}

# Make the POST request to exchange the code for tokens
response = requests.post(token_url, data=payload)

# Check if the request was successful
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get('access_token')
    id_token = token_data.get('id_token')
    print(f'Access Token: {access_token}')
    print(f'ID Token: {id_token}')
else:
    print(f'Error: {response.status_code}')
    print(response.text)