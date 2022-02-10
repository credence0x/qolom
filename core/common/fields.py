from django.db import models

class DefaultCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)


class DefaultDateTimeField(models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

class DefaultTimeField(models.TimeField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

class DefaultTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)


class DefaultIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['default'] = 0
        super().__init__(*args, **kwargs)