from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tasks.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the database with fake data'
    
    def handle(self, *args, **options):
        fake = Faker()
        
        all_priorities = list(Priority.objects.all())
        all_categories = list(Category.objects.all())
        statuses = ["Pending", "In Progress", "Completed"]
        
        self.stdout.write("Starting data population...")
        
        if not all_priorities:
            self.stdout.write(self.style.ERROR('No priorities found! Please add priorities first.'))
            return
            
        if not all_categories:
            self.stdout.write(self.style.ERROR('No categories found! Please add categories first.'))
            return
        
        for i in range(20):  
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=statuses),
                category=fake.random_element(elements=all_categories),
                priority=fake.random_element(elements=all_priorities)
            )
            
            if fake.boolean(chance_of_getting_true=70):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=5)
                )

            if fake.boolean(chance_of_getting_true=60):
                for _ in range(fake.random_int(min=1, max=5)):
                    SubTask.objects.create(
                        parent_task=task,
                        title=fake.sentence(nb_words=4),
                        status=fake.random_element(elements=statuses)
                    )
            
            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} tasks...")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated the database with fake data!')
        )