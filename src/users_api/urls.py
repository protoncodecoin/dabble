from django.urls import path

from . import views

urlpatterns = [
    path("creators/", views.CreatorList.as_view()),
    # path(
    #     "rest-auth/registration/",
    #     views.CustomRegisterView.as_view(),
    #     name="custom_registration",
    # ),
]
