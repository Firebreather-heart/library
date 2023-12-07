from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
import uuid
# Create your models here.


class Category(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    created = models.DateField(auto_now=True)
    search_vector = SearchVectorField(null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, force_insert= ..., using=... ) -> None:
        self.name = self.name.lower()
       # self.search_vector = SearchVector('name',)
        return super().save()


class Book(models.Model):
    name = models.CharField(db_index=True, max_length=100)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name="book_category"
    )
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default='general')
    desc = models.CharField(max_length=1000)
    date_added = models.DateField(auto_now=True)
    payload = models.FileField(upload_to='books/', blank=True)
    image = models.ImageField(
        upload_to='book-cover/', blank=True, null=True)
    search_vector = SearchVectorField(null=True)
    # idx = models.BigIntegerField(default=0,)

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self,force_insert = ... , using=...):
        #self.search_vector = SearchVector('name', 'author', 'desc')
        # last = Book.objects.last().idx
        # self.idx = last + 1
        return super().save()
