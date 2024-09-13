from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.utils.urls import replace_query_param

class PagePaginationCustom(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'first': self.get_first_link(),
                'last': self.get_last_link(),
                'prev': self.get_previous_link(),
                'next': self.get_next_link()
            },
            'meta': {
                'current_page': self.page.number,
                'next_page': self.get_next_page(),
                'previous_page': self.get_previous_page(),
                'last_page': self.page.paginator.num_pages,
                'from': self.page.start_index(),
                'to': self.page.end_index(),
                'total': self.page.paginator.count,
                'path': self.request.build_absolute_uri()
            },
            'data': data
        })

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages + 1 - self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def get_next_page(self):
        next_page = self.page.number + 1
        if self.page.paginator.num_pages < next_page:
            return None
        else:
            return next_page

    def get_previous_page(self):
        previous_page = self.page.number - 1
        if previous_page < 1:
            return None
        else:
            return previous_page