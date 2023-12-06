from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Book, Category
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
# Create your views here.



class BookApiView(APIView):
    @swagger_auto_schema(
        responses={200: "OK"},
        operation_summary="Get all the books in the library",
        operation_description="""
                            This endpoint allows you to get all the books in the library 
                            in no particular order.
                         """
    )
    def get(self, request):
        books = Book.objects.all()
        books = {
            "books": [str([i.name, i.author, i.desc, i.category]) for i in books]}
        return Response(books, status=status.HTTP_200_OK)


class AddBookApiView(APIView):
    def get(self, request):
        return Response({'message':"GET not supported"})

    @swagger_auto_schema(
        responses={200: "OK"},
        operation_summary="Add a book to the library",
        operation_description="""
                            This endpoint allows you to add a new book to the library.
                            The details needed are, 
                            name, author, desc(a description of the book), category(the category to whivh the book belongs), payload(i.e the actual file),
                            the cover image of the book
                         """
    )
    def post(self, request,*args, **kwargs):
        rd = request.POST  # request dictionary
        try:
            request_dict = {"name": rd.get('name'), "author": rd.get('author'), "desc": rd.get('desc'),
                            "category": Category.objects.get(name=rd.get('category')),#get_object_or_404(Category, name= rd.get('category')),
                            "payload": rd.get("payload"),
                            "image": request.FILES.get('cover_image'),
                            }
            print(request_dict)
        except:
            print('an exception occured')
            request_dict = {"name": rd.get('name'), "author": rd.get('author'), "desc": rd.get('desc'),
                            "payload": rd.get("payload"),
                            "image": request.FILES.get('cover_image'),
                            }
            print('exception skipped')
        try:
            Category.objects.get(name=rd.get('category'))#get_object_or_404(Category, name=rd.get('category'))
        except:
            # Category.objects.create(name=rd.get('category'), )
            print(rd.get('name'))
            nc = Category(name=rd.get('category'))
            nc.save()
        finally:
            request_dict["category"] = Category.objects.get(name=rd.get('category'))
        try:
            book_obj = Book(*request_dict)
            book_obj.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetBookApiview(APIView):
    @swagger_auto_schema(
        responses={200: "OK", 404: "Not Found"},
        operation_summary="Get a particular book based on its uuid",
        operation_description="""
                            The uuid is the unique identifier of a book and its the only way
                            to get a particular book from the database. 
                         """
    )
    def get(self, request, id):
        book = Book.objects.get(id=id)
        bk_dict = book.__dict__
        bk_dict.pop('_state')
        return Response({"book_details": str(book.__dict__)}, status=status.HTTP_200_OK)


class GetCategoryListApiVIew(APIView):
    @swagger_auto_schema(
        responses={200: "OK"},
        operation_summary="Get a list of all book categories",
        operation_description="""
                            This endpoint gives you all the categories of books in the 
                            library, the name of the category is the required variable needed in the AddBook
                            endpoint. 
                         """
    )
    def get(self, request):
        categories = Category.objects.all()
        c_d = [i.name for i in categories]
        return Response({"categories": str(c_d)}, status=status.HTTP_200_OK)

class SearchBookApiView(APIView):
    @swagger_auto_schema(
            responses={200:'OK'},
            operation_summary="Search for a particular book"
    )
    def get(self,request,):
        q = request.GET.get('q', '')
        if q:
            s_query = SearchQuery(q)
            search_vector = SearchVector('name', 'desc', 'author')
            results = Book.objects.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, s_query)
            ).filter(
                search=s_query
            ).order_by('-rank')
        else:
            results=None
        return Response({'query':q, 'results': results})
    

class SearchCategoryApiView(APIView):
    @swagger_auto_schema(
        responses={200: 'OK'},
        operation_summary="Search for a particular category"
    )
    def get(self, request,):
        q = request.GET.get('q', '')
        if q:
            s_query = SearchQuery(q)
            search_vector = SearchVector('name',)
            results = Book.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, s_query)
            ).filter(
                search=s_query
            ).order_by('-rank')
        else:
            results = None
        return Response({'query': q, 'results': results})

class GetBookPaginatorView(APIView):
    @swagger_auto_schema(
        responses={200: "OK"},
        operation_summary="Get all the books in the library in pages",
        operation_description="""
                            The lazy loader loads the books in pages 10 books at a time
                         """
    )
    def get(self, request,):
        page = request.GET.get('page')
        qs = Book.objects.order_by('name')
        
        limit = 10
        paginator = Paginator(qs, limit)
        try:
            bks = paginator.page(page)
        except PageNotAnInteger:
            bks = paginator.page(1)
        except EmptyPage:
            bks = paginator.page(paginator.num_pages)
        
        s_data = [
                {
                    'id': item.id,
                    'name': item.name,
                    'author': item.author,
                    'photo': item.image if item.image else "",
                    'description': item.desc,
                    'category': item.category.name,
                    'date': item.date_added
                }
                for item in bks
            ]
        data = {
            'results': s_data,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'has_next': bks.has_next(),
            'has_previous': bks.has_previous(),
        }
        return Response(data)