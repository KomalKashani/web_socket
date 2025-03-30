from django.contrib import admin
from app.models import Chat,Group

# Register your models here.
@admin.register(Chat)
class ChatAdminModel(admin.ModelAdmin):
    list_display = ['id','content','timestamp','group']

@admin.register(Group)
class GroupAdminModel(admin.ModelAdmin):
    list_display = ['id','name']