from django.db import models
import uuid
# Create your models here.


class Category(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    created = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
    
    def save(self, ) -> None:
        self.name = self.name.lower()
        return super().save( )


class Book(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name="book_category"
    )
    author = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    date_added = models.DateField(auto_now=True)
    payload = models.FileField(upload_to='books/', blank=True)
    image = models.ImageField(
        upload_to='book-cover/', blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'
