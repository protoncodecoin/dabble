from django.urls import path

from .import views_html

app_name = "library"

urlpatterns = [
    path("<int:id>/<slug:slug>/<str:category>/", views_html.detail_book, name="book_detail"),
]