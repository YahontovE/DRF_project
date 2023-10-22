from  rest_framework.pagination import PageNumberPagination


class CoursePaginator(PageNumberPagination):
    page_size = 1

class LessonPaginator(PageNumberPagination):
    page_size = 2