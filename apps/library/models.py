from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    shelf_location = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='books/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.available_copies > 0


class BookIssue(models.Model):
    ISSUED = 'issued'
    RETURNED = 'returned'
    OVERDUE = 'overdue'
    LOST = 'lost'

    STATUS_CHOICES = [
        (ISSUED, 'Issued'),
        (RETURNED, 'Returned'),
        (OVERDUE, 'Overdue'),
        (LOST, 'Lost'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_books')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ISSUED)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'book_issues'

    def __str__(self):
        return f"{self.book.title} -> {self.borrower.get_full_name()} ({self.status})"

    def calculate_fine(self, fine_per_day=10):
        from datetime import date
        if self.status == self.RETURNED and self.return_date:
            if self.return_date > self.due_date:
                days_overdue = (self.return_date - self.due_date).days
                return days_overdue * fine_per_day
        elif self.status == self.ISSUED:
            today = date.today()
            if today > self.due_date:
                days_overdue = (today - self.due_date).days
                return days_overdue * fine_per_day
        return 0
