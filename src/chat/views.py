from django.shortcuts import render


# Create your views here.
def chat_person(request):
    return render(request, "chat/chat_person.html")
