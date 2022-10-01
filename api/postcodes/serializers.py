import re

from rest_framework import serializers

from api import settings
from postcodes.models import FileUploader, Code
from utils.aws import Dispatcher


class FileUploaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUploader
        fields = '__all__'

    def create(self, validated_data):
        dispatcher = Dispatcher()
        file = FileUploader.objects.create(**validated_data)
        file_without_spaces = re.sub(r"[\(\)]", '', file.name)
        file_badge = file_without_spaces.replace(" ", "").replace(".", "")

        values = {
            'job_name': 'File-' + file_badge + '-' + str(file.id) + '-' + str(file.organization_id),
            'job_queue': settings.JOB_QUEUE_CODE,
            'script': ['python', 'postcodes.py', str(file.id)]
        }
        dispatcher.aws_batch(**values)
        return file


class CodeSerializer(serializers.ModelSerializer):

    country_name = serializers.CharField(source='country.name')

    class Meta:
        model = Code
        fields = ('id', 'postcode', 'country_name', 'latitude', 'longitude')
