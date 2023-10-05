from django.contrib.contenttypes.models import ContentType
from .models import Favorite


def create_favorite(request_user, content_id: int, target_model):
    """
    Abstract the process of adding and removing favorite
    returns True if created else False
    """
    target_ct = ContentType.objects.get_for_model(target_model)

    user_fav = Favorite.objects.filter(
        user=request_user, content_type=target_ct, object_id=content_id
    )

    if user_fav:
        user_fav.delete()
        return False
    else:
        Favorite.objects.create(
            user=request_user, content_type=target_ct, object_id=content_id
        )
        return True
