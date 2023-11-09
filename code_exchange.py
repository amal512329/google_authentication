# Define the URL with query parameters
client_id = '173313288818-g2vhqrbrm79copjnheoi513pggf51dsm.apps.googleusercontent.com'  # Replace with your actual client ID
client_secret = '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'  # Replace with your actual client secret
authorization_code = '4%2F0AfJohXmene0ByrYXBbHL8_MCX3NsjPmAPuPFGr9g9lwymEzydAFuGjwessTmFCIYfJaPjg'  # Replace with your actual authorization code

token_exchange_url = (
        'https://oauth2.googleapis.com/token'
        f'?client_id={client_id}'
        f'&client_secret={client_secret}'
        f'&code={authorization_code}'
        f'&grant_type=authorization_code'
        f'&redirect_uri=http://127.0.0.1:8000/rest/google/'
    )

print(token_exchange_url)