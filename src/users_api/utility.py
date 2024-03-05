# from django.contrib.contenttypes.models import ContentType
# from .models import Favorite
# from .serializers import FavoriteSerializer
# from anime_api.serializers import AnimeCreateSerializer


# def create_favorite(request_user, content_id: int, target_model):
#     """
#     Abstract the process of adding and removing favorite
#     returns True if created else False
#     """
#     target_ct = ContentType.objects.get_for_model(target_model)

#     user_fav = Favorite.objects.filter(
#         user=request_user, content_type=target_ct, object_id=content_id
#     )

#     if user_fav:
#         user_fav.delete()
#         return False
#     else:
#         fav = Favorite.objects.create(
#             user=request_user, content_type=target_ct, object_id=content_id
#         )
#         serializer = FavoriteSerializer(fav, many=False)
#         return serializer
