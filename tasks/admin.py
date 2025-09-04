from django.contrib import admin
from .models import Priority, Category, Task, Note, SubTask

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  
    fields = ("title", "status")
    show_change_link = True  

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)  

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "deadline", "priority", "category"]
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description")
    inlines = [SubTaskInline, NoteInline]  

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent_task_name']
    list_filter = ['status']
    search_fields = ['title']
    
    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = 'Parent Task'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['task', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'