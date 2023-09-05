from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 999
    page_size_query_param = 'limit'
    max_page_size = 999