from django.urls import path

from pages.views import ContactCreateView, AboutView, HomeView, LoginView, RegisterView, FlipView


app_name = 'contact'

urlpatterns = [
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('blog/', AboutView.as_view(), name='blog'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('flip/', FlipView.as_view(), name='flip'),
    path('', HomeView.as_view(), name='home')
]