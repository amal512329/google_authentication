"""
URL configuration for book_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from app.views import FacebookLogin,GoogleLoginView,UserRedirectView ,GoogleOAuthAuthorizationView,token_exchange_form



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path("rest/google/", GoogleLoginView.as_view(), name="google_login"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),  
    path('google-auth/', GoogleOAuthAuthorizationView.as_view(), name='google-auth'),
    path('google-token/',token_exchange_form,name="google-token"),
    # path('token-exchange-form/', TokenExchangeFormView.as_view(), name='token-exchange-form'),
    
   
]
