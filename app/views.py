from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
import jwt
import json
import requests
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse,HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from .forms import TokenExchangeForm
import requests


# Create your views here.

class IndexViews(TemplateView):
    template_name = 'index.html' 


def Usersignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['firts_name']
            password1 = request.POST['passowrd1']
            password2 = request.POST['password2']

            if password1==password2:
                messages.info(request,'Password does not match')
                return redirect('/signup')



class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter



class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
   
    def complete_login(self, request, app, token, response, **kwargs):
        try:
            # Parse the response as JSON
            response_data = json.loads(response)
            access_token = response_data.get('access_token')
            if not access_token:
                raise OAuth2Error("Missing access_token in response")
        except json.JSONDecodeError as e:
            # If the response is not valid JSON, assume it's just an access token
            access_token = response
            # You should make an additional request to the Google API to obtain user information
            identity_data = self.get_identity_data_using_access_token(access_token)
        else:
            # If it's valid JSON, try to extract the id_token
            id_token = response_data.get('id_token')
            if id_token is None:
                raise OAuth2Error("Missing id_token in response")
            
            identity_data = jwt.decode(
                id_token,
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                issuer=self.id_token_issuer,
                audience=app.client_id,
            )

        login = self.get_provider().sociallogin_from_response(request, identity_data)
        return login

    def get_identity_data_using_access_token(self, access_token):
         # Make a request to Google's user information endpoint to obtain user data
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}


        try:
            response = requests.get(user_info_url, headers=headers)
            response_data = response.json()

        except Exception as e:
            raise OAuth2Error(f"Error retrieving user data: {e}")

        return response_data

class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "http://127.0.0.1:8000/"


class GoogleLoginView(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/rest/google/"
    client_class = OAuth2Client


class GoogleOAuthAuthorizationView(View):
    def get(self, request):
        # Define the OAuth 2.0 parameters
        scope = "openid"  # scopes
        access_type = "offline"  # access type to "offline" for refresh tokens
        include_granted_scopes = "true"  #  Include granted scopes in the response
        response_type = "code"  #  authorization code and ID token
        state = "state_parameter_passthrough_value"  # Optional: Protect against CSRF attacks
        redirect_uri = "http://127.0.0.1:8000/rest/google/"  #  redirect URI
        client_id = "173313288818-g2vhqrbrm79copjnheoi513pggf51dsm.apps.googleusercontent.com"  # Replace with your OAuth client ID

        # Construct the authorization URL
        authorization_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"scope={scope}&"
            f"access_type={access_type}&"
            f"include_granted_scopes={include_granted_scopes}&"
            f"response_type={response_type}&"
            f"state={state}&"
            f"redirect_uri={redirect_uri}&"
            f"client_id={client_id}"
        )

        # Redirect the user to the Google OAuth authorization URL
        return redirect(authorization_url)



class GoogleTokenExchangeView(APIView):
    
     def post(self, request):
        # Define the token exchange URL
        token_exchange_url = 'https://oauth2.googleapis.com/token?'

        # Define the request data as form data
        data = {
            'code': '4%2F0AfJohXkX24kwl15mfDeLi_NfYMYdek6IZHUfKAeM-oFUU8iioC9GXwi38OT1ZFNIpU596w',
            'client_id': '173313288818-g2vhqrbrm79copjnheoi513pggf51dsm.apps.googleusercontent.com',
            'client_secret': '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',
            'redirect_uri': 'http://127.0.0.1:8000/rest/google/',
            'grant_type': 'authorization_code',
        }

        # Send the request to the Google token exchange endpoint
        response = requests.post(token_exchange_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            id_token = token_data.get('id_token')
            return Response({'access_token': access_token, 'id_token': id_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token exchange failed'}, status=response.status_code)


class TokenExchangeFormView(View):
    def get(self, request):
        return render(request, 'token_exchange_form.html')
    

def token_exchange_form(request):

   # Define the URL with query parameters
    client_id = '173313288818-g2vhqrbrm79copjnheoi513pggf51dsm.apps.googleusercontent.com'  #  client ID
    client_secret = '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'  #  client secret
    authorization_code = '4%2F0AfJohXk_ethxWzcsDIxh_9j1Re5JU5O7jZlCBFNmse8jpHAb4lilsRf9WgEQRVJMZRSJlg'  #  authorization code

    token_exchange_url = (
        'https://oauth2.googleapis.com/token'
        f'?client_id={client_id}'
        f'&client_secret={client_secret}'
        f'&code={authorization_code}'
        f'&grant_type=authorization_code'
        f'&redirect_uri=http://127.0.0.1:8000/rest/google/'
    )

    # csrf_token = get_token(request)
    
    csrf_token = request.COOKIES.get('csrftoken')
    

    response = requests.post(token_exchange_url, headers={'X-CSRFToken': csrf_token})

   
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')
        return JsonResponse({'access_token': access_token, 'id_token': id_token})
    else:
        return JsonResponse({'error': 'Token exchange failed'}, status=response.status_code)
