from rest_framework import serializers
from .models import Book, Category 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'name','author','id','desc','image','date_added','category','genre','payload'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Category 
        fields = ['name']