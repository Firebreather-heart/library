from django.test import TestCase
from django.urls import reverse
from matplotlib import category 
from .models import Book, Category
# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name = 'test category',
        )
    
    def test_category_list_view(self):
        res = self.client.get(reverse('get_categories'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.cat)
        self.assertEqual(Category.objects.count(), 1)

class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name='test book',
            category = Category.objects.create(name='test category'),
            author = 'test author',
            desc = 'test description',
        )

        self.book2 = Book.objects.create(
            name='test book 2' ,
            category = Category.objects.create(name='test category'),
            author = 'test author 2',
            desc = 'test description 2',
        )

    def test_get_book_paginator_view(self):
        res = self.client.get(reverse('books'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'test book 1')
        self.assertContains(res, 'test book 2')
    
    def test_getbookapiview(self):
        res = self.client.get(reverse('get_book', args=[self.book.id]))
        self.assertContains(res, 'test book')
        self.assertContains(res, 'test author')
        
    
        
