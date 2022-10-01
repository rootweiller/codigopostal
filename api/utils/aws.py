from api import settings
import boto3


class Dispatcher:
    """
    class to dispatcher different platforms and providers
    """

    def __init__(self):
        self.client = boto3.client(
            'batch',
            aws_access_key_id=settings.AWS_ACCESS_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

    def aws_batch(self, **kwargs):
        response = self.client.submit_job(
            jobName=kwargs['job_name'],
            jobQueue=kwargs['job_queue'],
            jobDefinition=settings.JOB_DEFINITION,
            containerOverrides={
                'vcpus': 1,
                'memory': 3600,
                'command': kwargs['script']
            },
            timeout={
                'attemptDurationSeconds': 1800
            },
        )
        return response
