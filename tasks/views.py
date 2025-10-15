from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm, CategoryForm, PriorityForm, NoteForm, SubTaskForm


@login_required(login_url='/accounts/login/')
def home(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status="Completed").count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    in_progress_tasks = Task.objects.filter(status="In Progress").count()
    upcoming = Task.objects.filter(deadline__gte=timezone.now()).order_by('deadline')[:5]

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "upcoming": upcoming,
    }
    return render(request, "tasks/home.html", context)


@login_required(login_url='/accounts/login/')
def task_list(request):
    sort_option = request.GET.get('sort', 'created')

    sort_mapping = {
        'title': 'title',
        'deadline': 'deadline',
        'priority': 'priority__name',
        'status': 'status',
        'created': '-created_at',
    }

    sort_field = sort_mapping.get(sort_option, '-created_at')
    tasks = Task.objects.all().order_by(sort_field)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'current_sort': sort_option,
    })


@login_required(login_url='/accounts/login/')
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required(login_url='/accounts/login/')
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required(login_url='/accounts/login/')
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required(login_url='/accounts/login/')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})


@login_required(login_url='/accounts/login/')
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'tasks/category_list.html', {'categories': categories})


@login_required(login_url='/accounts/login/')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form, 'title': 'Create Category'})


@login_required(login_url='/accounts/login/')
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'tasks/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required(login_url='/accounts/login/')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})


@login_required(login_url='/accounts/login/')
def priority_list(request):
    priorities = Priority.objects.all().order_by('name')
    return render(request, 'tasks/priority_list.html', {'priorities': priorities})


@login_required(login_url='/accounts/login/')
def priority_create(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'tasks/priority_form.html', {'form': form, 'title': 'Create Priority'})


@login_required(login_url='/accounts/login/')
def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm(instance=priority)
    return render(request, 'tasks/priority_form.html', {'form': form, 'title': 'Edit Priority'})


@login_required(login_url='/accounts/login/')
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('priority_list')
    return render(request, 'tasks/priority_confirm_delete.html', {'priority': priority})


@login_required(login_url='/accounts/login/')
def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'tasks/note_list.html', {'notes': notes})


@login_required(login_url='/accounts/login/')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'tasks/note_form.html', {'form': form, 'title': 'Create Note'})


@login_required(login_url='/accounts/login/')
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'tasks/note_form.html', {'form': form, 'title': 'Edit Note'})


@login_required(login_url='/accounts/login/')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'tasks/note_confirm_delete.html', {'note': note})


@login_required(login_url='/accounts/login/')
def subtask_list(request):
    subtasks = SubTask.objects.all().order_by('-created_at')
    return render(request, 'tasks/subtask_list.html', {'subtasks': subtasks})


@login_required(login_url='/accounts/login/')
def subtask_create(request):
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subtask_list')
    else:
        form = SubTaskForm()
    return render(request, 'tasks/subtask_form.html', {'form': form, 'title': 'Create Subtask'})


@login_required(login_url='/accounts/login/')
def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('subtask_list')
    else:
        form = SubTaskForm(instance=subtask)
    return render(request, 'tasks/subtask_form.html', {'form': form, 'title': 'Edit Subtask'})


@login_required(login_url='/accounts/login/')
def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        subtask.delete()
        return redirect('subtask_list')
    return render(request, 'tasks/subtask_confirm_delete.html', {'subtask': subtask})
