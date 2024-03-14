from django.contrib import admin
from .models import Publisher
#import-export
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field


class PublisherResource(resources.ModelResource):
    date = Field()
    class Meta:
        model = Publisher
        fields = ('id','name','country','created', 'date')
        export_order = ('id','name','country','created', 'date')
        
    def dehydrate_date(self, obj):  #the name of the function to reformat is very specific
        return obj.created.strftime("%m/%d/%y")
        
class PublisherAdmin(ExportActionMixin, admin.ModelAdmin):#adding mixin put the export in the dropdown
    resource_class = PublisherResource

admin.site.register(Publisher, PublisherAdmin)