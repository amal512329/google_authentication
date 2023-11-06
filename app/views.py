from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
import jwt
import json
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










