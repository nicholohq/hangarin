from django import forms
from .models import Task, Category, Priority, Note, SubTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter task details', 'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(),
            'category': forms.Select(),
            'priority': forms.Select(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
        }


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter priority level (e.g. High, Medium, Low)'}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'content']
        widgets = {
            'task': forms.Select(),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note...', 'rows': 3}),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['parent_task', 'title', 'status']
        widgets = {
            'parent_task': forms.Select(),
            'title': forms.TextInput(attrs={'placeholder': 'Enter subtask title'}),
            'status': forms.Select(),
        }
