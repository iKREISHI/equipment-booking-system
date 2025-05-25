from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    • page=<номер страницы>, начинается с 1
    • page_size=<сколько элементов вернуть>, по умолчанию 20,
      максимум 100 (чтобы никто не запросил «всех» одним вызовом)
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
