from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model

from chat.models import GroupMessage, Message

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.pagination import ChatPagination
from chat.serializers import MessageSerializer


# Create your views here.
@login_required
def chat_person(request):

    # retrieve chat history
    latest_messages = GroupMessage.objects.all().order_by("-id")[:20]
    latest_messages = reversed(latest_messages)

    friends = Message.objects.filter(from_user=request.user)
    friends_list = list()

    for friend in friends:
        if friend.to_who not in friends_list:
            friends_list.append(friend.to_who)

    print(friends_list)

    return render(
        request,
        "chat/chatpage.html",
        {
            "selection": "chat",
            "latest_messages": latest_messages,
            "friends": friends_list,
        },
    )


class MessageAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = ChatPagination

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get("other")
        other_user = None

        queryset = Message.objects.all()

        if other_user_id:
            try:
                other_user = get_user_model().objects.get(id=other_user_id)
                print(other_user, "this is the other user")
            except get_user_model().DoesNotExist():
                return Response({"message": "User does not exist"})

        if user:
            queryset = queryset.filter(
                Q(from_user=user, to_who=other_user)
                | Q(to_who=user, from_user=other_user)
            )
            return queryset
        return Response({"message": "no messages found"})
