from django.contrib import admin
from .models import person,Item,Web



class ItemList(admin.ModelAdmin):
	list_display=['name','time','company','money']
	search_fields=['name']
class personList(admin.ModelAdmin):
	list_display=['user_name','password','email']
	search_fields=['user_name']
class WebList(admin.ModelAdmin):
	list_display=['webAddr']
# Register your models here.
admin.site.register(person,personList)
admin.site.register(Item,ItemList)
admin.site.register(Web,WebList)

