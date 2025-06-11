import base64
import six
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

def validate_image_size(value):
    max_size = 1 * 1024 * 1024  # 1MB
    if value.size > max_size:
        raise ValidationError(
            f"Rasm hajmi {filesizeformat(max_size)} dan katta bo'lishi mumkin emas. "
            f"Siz yuborgan rasm hajmi: {filesizeformat(value.size)}"
        )


class Base64ImageField(serializers.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop('max_size', 1 * 1024 * 1024)  # Default 1MB
        super().__init__(*args, **kwargs)
        self.validators.append(validate_image_size)

    def to_internal_value(self, data):
        if isinstance(data, str):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except:
                raise ValidationError('Noto‘g‘ri base64 rasm')
            
            # Rasm hajmini tekshirish
            file_extension = self.get_file_extension(header)
            if len(decoded_file) > self.max_size:
                raise ValidationError(
                    f"Rasm hajmi {filesizeformat(self.max_size)} dan katta. "
                    f"Hajmi: {filesizeformat(len(decoded_file))}"
                )
                
            file_name = str(uuid.uuid4())[:12]
            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)
            
        return super().to_internal_value(data)
    
    def get_file_extension(self, header):
        if 'image/png' in header:
            return 'png'
        elif 'image/jpeg' in header:
            return 'jpg'
        elif 'image/jpg' in header:
            return 'jpg'
        else:
            raise ValidationError('Noto‘g‘ri rasm formati')  