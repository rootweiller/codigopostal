from django.contrib import admin

from postcodes.models import FileUploader, Code


class FileUploaderAdmin(admin.ModelAdmin):

    list_display = ('name', 'file')

    class Meta:
        model = FileUploader
        fields = '__all__'


class CodeAdmin(admin.ModelAdmin):

    list_display = ('country', 'postcode', 'latitude', 'longitude')

    class Meta:
        model = Code
        fields = '__all__'


admin.site.register(FileUploader, FileUploaderAdmin)
admin.site.register(Code, CodeAdmin)
