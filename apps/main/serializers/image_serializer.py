import base64
import six
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except:
                raise ValidationError('Invalid base64 image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = 'jpg'  # yoki sizga kerakli rasm turi
            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)
