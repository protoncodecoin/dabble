from datetime import timedelta
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
import redis

from rest_framework.decorators import api_view
from rest_framework.response import Response


from anime_api import models
from users_api.models import CreatorProfile
from .views_serializer import (
    SimpleDesignSerializer,
    SimpleAnimeSerializer,
    SimpleAnimeSerializerWithTrends,
    SimpleWrittenStory,
    SimpleVideoSerializer,
    SimpleTextSerializer,
    SimplePhotographySerializer,
)

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def index(request):

    return render(
        request, "anime_api/index.html", {"page": "home", "selection": "home"}
    )


def profile(request, id, slug):
    return render(
        request,
        "anime_api/profile.html",
        {
            "id": id,
            "slug": slug,
            "section": "profile",
            "selection": "profile",
        },
    )


def dashboard(request):
    return render(request, "anime_api/dashboard.html", {"selection": "dashboard"})


@api_view(["POST"])
def detail_post_count(request, content_type, id):
    """Keep track of the number of views of a post"""
    post = None
    content_type_mapping = {
        # "series": models.Series,
        "anime": models.Anime,
        "writtenstory": models.WrittenStory,
        "creator": CreatorProfile,
        "video": models.Video,
        "design": models.Design,
        "text": models.Text,
    }

    target_content = content_type_mapping.get(content_type)

    if target_content == models.Anime:
        post = get_object_or_404(models.Anime, id=id)
        total_views = r.incr(f"anime:{post.id}:views")

        # increment total anime views by 1
        r.zincrby("anime_ranking", 1, post.id)

        # increment general post by one
        # r.zincrby("post_ranking", 1, post.id)

        return Response({"total_views": total_views, "post": post})

    elif target_content == models.WrittenStory:
        post = get_object_or_404(models.WrittenStory, id=id)
        total_views = r.incr(f"writtenstories:{post.id}:views")

        # increment total writtenstory views by 1
        r.zincrby("writtenstory_ranking", 1, post.id)

        # increment general post by one
        # r.zincrby("post_ranking", 1, post.id)

        return Response({"total_views": total_views, "post": post})

    # elif target_content == models.CreatorProfile:
    #     post = get_object_or_404(models.CreatorProfile, id=id)

    #     total_views = r.incr(f"creatorProfile:{post}:views")
    #     # increment total creatorprofile views by 1
    #     r.zincrby("creatorProfile", 1, post.id)

    #     # increment general post by one
    #     # r.zincrby("post_ranking", 1, post.id)

    #     return render(
    #         request,
    #         "anime_api/post_detail.html",
    #         {
    #             # "total_views": total_views,
    #             "post": post,
    #         },
    #     )

    elif target_content == models.Video:
        post = get_object_or_404(models.Video, id=id)
        total_views = r.incr(f"video:{post.id}:views")

        # increment total video views by 1
        r.zincrby("video_ranking", 1, post.id)

        # increment general post by one
        # r.zincrby("post_ranking", 1, post.id)
        # return render(
        #     request,
        #     "anime_api/post_detail.html",
        #     {
        #         "total_views": total_views,
        #         "post": post,
        #         "selction": "detail",
        #     },
        # )
        return Response({"total_views": total_views, "post": post})

    elif target_content == models.Text:
        post = get_object_or_404(models.Text, id=id)
        total_views = r.incr(f"text:{post.id}:views")
        # increment total text views by 1
        r.zincrby("text_ranking", 1, post.id)

        # increment general post by one
        # r.zincrby("post_ranking", 1, post.id)

        # return render(
        #     request,
        #     "anime_api/post_detail.html",
        #     {
        #         "total_views": total_views,
        #         "post": post,
        #         "selction": "detail",
        #     },
        # )
        return Response({"total_views": total_views, "post": post})

    elif target_content == models.Design:
        post = get_object_or_404(models.Design, id=id)
        total_views = r.incr(f"design:{post}:views")

        # increment total design views by 1
        r.zincrby("design_ranking", 1, post.id)

        # increment general post by one
        # r.zincrby("post_ranking", 1, post.id)

        # return render(
        #     request,
        #     "anime_api/post_detail.html",
        #     {
        #         "total_views": total_views,
        #         "post": post,
        #         "selction": "detail",
        #     },
        # )
        return Response({"total_views": total_views, "post": post})

    elif target_content == models.Photography:
        post = get_object_or_404(models.Photography, id=id)
        total_views = r.incr(f"photograhpy:{post}:views")

        # increment total design views by 1
        r.zincrby("photography_ranking", 1, post.id)

        return Response({"total_views": total_views, "post": post})

    return render(request, "anime_api/post_detail.html")


@csrf_exempt
def post_ranking(request):
    """
    Return posts by ranking. Also returns trending posts.
    """
    # get post ranking dictionary
    anime_rank = r.zrange("anime_ranking", 0, -1, desc=True)[:10]
    anime_ranking_ids = [int(id) for id in anime_rank]
    # get most viewed post
    anime_trends = models.Anime.objects.filter(id__in=anime_ranking_ids)

    anime_most_viewed = list(anime_trends)
    anime_most_viewed.sort(key=lambda x: anime_ranking_ids.index(x.id))
    anime_serializer = SimpleAnimeSerializer(anime_most_viewed, many=True)

    writtenstory_rank = r.zrange("writtenstory_ranking", 0, -1, desc=True)[:10]
    writtenstory_ranking_ids = [int(id) for id in writtenstory_rank]
    # get most viewed post
    story_trends = models.WrittenStory.objects.filter(id__in=writtenstory_ranking_ids)
    story_most_viewed = list(story_trends)
    story_most_viewed.sort(key=lambda x: writtenstory_ranking_ids.index(x.id))
    story_serializer = SimpleWrittenStory(story_most_viewed, many=True)

    video_rank = r.zrange("video_ranking", 0, -1, desc=True)[:10]
    video_ranking_ids = [int(id) for id in video_rank]
    # get most viewed post
    video_trends = models.Video.objects.filter(id__in=video_ranking_ids)
    video_most_viewed = list(video_trends)
    video_most_viewed.sort(key=lambda x: video_ranking_ids.index(x.id))
    video_serializer = SimpleVideoSerializer(video_most_viewed, many=True)

    text_rank = r.zrange("text_ranking", 0, -1, desc=True)[:10]
    text_ranking_ids = [int(id) for id in text_rank]
    # get most viewed post

    text_trends = models.Text.objects.filter(id__in=text_ranking_ids)
    text_most_viewed = list(text_trends)
    text_most_viewed.sort(key=lambda x: text_ranking_ids.index(x.id))
    text_serializer = SimpleTextSerializer(text_most_viewed, many=True)

    design_rank = r.zrange("design_ranking", 0, -1, desc=True)[:10]
    design_ranking_ids = [int(id) for id in design_rank]
    # get most viewed post
    design_trends = models.Design.objects.filter(id__in=design_ranking_ids)
    design_most_viewed = list(design_trends)

    design_most_viewed.sort(key=lambda x: design_ranking_ids.index(x.id))
    design_serializer = SimpleDesignSerializer(design_most_viewed, many=True)

    # get most viewed photography
    photography_rank = r.zrange("photography_ranking", 0, -1, desc=True)[:10]
    photography_ranking_ids = [int(id) for id in photography_rank]
    photography_trends = models.Photography.objects.filter(
        id__in=photography_ranking_ids
    )
    photography_most_viewed = list(photography_trends)

    photography_most_viewed.sort(key=lambda x: photography_ranking_ids.index(x.id))
    photography_serializer = SimplePhotographySerializer(
        photography_most_viewed, many=True
    )

    # MOST TRENDING
    week_ago = timezone.now() - timedelta(days=70)

    top_anime_trends = (
        anime_trends.annotate(
            count_likes=Count("likes", filter=Q(release_date__gte=week_ago))
            # count_likes=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(count_likes__gt=0)
        .order_by("-count_likes")
    )
    anime_trend_serializer = SimpleAnimeSerializerWithTrends(
        top_anime_trends, many=True
    )

    top_story_trends = (
        story_trends.annotate(
            count_likes=Count("likes", filter=Q(release_date__gte=week_ago))
            # count_likes=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(count_likes__gt=0)
        .order_by("-count_likes")
    )
    story_trend_serializer = SimpleWrittenStory(top_story_trends, many=True)

    top_design_trends = (
        design_trends.annotate(
            likes_count=Count("likes", filter=Q(release_date__gte=week_ago))
            # likes_count=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(likes_count__gt=0)
        .order_by("-likes_count")
    )
    design_trend_serializer = SimpleDesignSerializer(top_design_trends, many=True)

    top_video_trends = (
        video_trends.annotate(
            count_likes=Count("likes", filter=Q(release_date__gte=week_ago))
            # count_likes=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(count_likes__gt=0)
        .order_by("-count_likes")
    )
    video_trends_serializer = SimpleVideoSerializer(top_video_trends, many=True)

    top_text_trends = (
        text_trends.annotate(
            count_likes=Count("likes", filter=Q(release_date__gte=week_ago))
            # count_likes=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(count_likes__gt=0)
        .order_by("-count_likes")
    )
    text_trends_serializer = SimpleTextSerializer(top_text_trends, many=True)

    top_photography_trends = (
        photography_trends.annotate(
            count_likes=Count("likes", filter=Q(date_posted__gte=week_ago))
            # count_likes=Count("likes", filter=Q(release_date__lte=week_ago))
        )
        .filter(count_likes__gt=0)
        .order_by("-count_likes")
    )
    photography_trends_serializer = SimpleTextSerializer(
        top_photography_trends, many=True
    )

    return JsonResponse(
        {
            "anime_most_viewed": anime_serializer.data[:3],
            "writtenstory_most_viewed": story_serializer.data[:3],
            "video_most_viewed": video_serializer.data[:3],
            "text_most_viewed": text_serializer.data[:3],
            "design_most_viewed": design_serializer.data[:3],
            "photography_most_viewed": photography_serializer.data[:3],
            "anime_trends": anime_trend_serializer.data,
            "story_trends": story_trend_serializer.data,
            "design_trends": design_trend_serializer.data,
            "video_trends": video_trends_serializer.data,
            "text_trends": text_trends_serializer.data,
            "photography": photography_trends_serializer.data,
        },
        safe=False,
        status=200,
    )


@csrf_exempt
def recently_viewed(request):
    return JsonResponse({"recently_viewed": "this is the recently viewed post"})


def gallery(request):
    return render(
        request, "anime_api/gallery/gallery.html", {"selection": "exhibition"}
    )


def gallery_animation(request):
    return render(
        request,
        "anime_api/gallery/animation.html",
        {"selection": "gallery_animation", "sub_selection": "animation"},
    )


def gallery_film(request):
    return render(
        request,
        "anime_api/gallery/film.html",
        {"selection": "gallery_animation", "sub_selection": "film"},
    )


def gallery_illustration(request):
    return render(
        request,
        "anime_api/gallery/illustrations.html",
        {"selection": "gallery_animation", "sub_selection": "illustrations"},
    )


def gallery_stories(request):
    return render(
        request,
        "anime_api/gallery/stories.html",
        {"selection": "gallery_animation", "sub_selection": "written_stories"},
    )


def photography(request):
    return render(
        request,
        "anime_api/gallery/photography.html",
        {"selection": "gallery_animation", "sub_selection": "photography"},
    )


def search(request):
    return render(request, "anime_api/search.html", {"selection": "search"})


def virtualtour(request):
    return render(request, "anime_api/virtualtour.html", {"selection": "virtualtour"})
