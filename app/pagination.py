from rest_framework import pagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15

class CustomPagination(pagination.PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    page_query_param = 'page'
