from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RecommendationPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data, count):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": count,
                "results": data,
            }
        )
