from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Har bir sahifada 10 ta element
    page_size_query_param = 'page_size'
    max_page_size = 100
   
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('data', data),
            ('pagination', OrderedDict([
                ('total', self.page.paginator.count),
                ('per_page', self.page.paginator.per_page),
                ('current_page', self.page.number),
                ('last_page', self.page.paginator.num_pages),
                ('next_page_url', self.get_next_link()),
                ('prev_page_url', self.get_previous_link()),
            ]))
        ]))

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

def get_paginated_response_schema(serializer):
    return inline_serializer(
        name=f'Paginated{serializer.__name__}',
        fields={
            'data': serializer(many=True),
            'pagination': inline_serializer(
                name='Pagination',
                fields={
                    'total': serializers.IntegerField(),
                    'per_page': serializers.IntegerField(),
                    'current_page': serializers.IntegerField(),
                    'last_page': serializers.IntegerField(),
                    'next_page_url': serializers.URLField(allow_null=True),
                    'prev_page_url': serializers.URLField(allow_null=True),
                }
            )
        }
    )


