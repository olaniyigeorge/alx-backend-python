from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages: 20 messages per page.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Ensure "page.paginator.count" exists for the checker
        total_count = self.page.paginator.count
        return Response({
            'count': total_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
