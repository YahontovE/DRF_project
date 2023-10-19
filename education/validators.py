from rest_framework.serializers import ValidationError


class Video_linkValidator:
    def __init__(self,field):
        self.field=field

    def __call__(self,value):
        tmp_val=dict(value).get(self.field)
        if 'youtube.com' not in tmp_val:
            raise ValidationError('video_link in to OK')
