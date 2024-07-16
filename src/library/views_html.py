from django.shortcuts import render


def library(request):
    return render(request, "library/library.html", {"selection": "library"})


def detail_book(request, id, slug, category):
    return render(
        request,
        "library/detail_page.html",
        {
            "id": id,
            "slug": slug,
            "category": category,
        },
    )
