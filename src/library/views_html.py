from django.shortcuts import render

def detail_book(request, id, slug, category):
    return render(request, "library/detail_page.html", {"id": id, "slug": slug, "category": category,})