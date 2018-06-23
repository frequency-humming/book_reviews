from django.shortcuts import render, redirect
from . models import*
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
    
    return render(request, "belt_review/index.html")

def register(request):
    error = False
    if len(request.POST['name']) < 2:
        messages.error(request, 'Name must be longer than 2 characters')
        error = True
    if any(char.isdigit() for char in request.POST['name']):
        messages.error(request, 'First Name cannot contain letters')
        error = True
    if len(request.POST['alias']) < 2:
        messages.error(request, 'Alias must be longer than 2 characters')
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Invalid email address')
        error = True
    if len(request.POST['password']) < 8:
        messages.error(request, 'Password must be at least 8 characters')
        error = True
    if request.POST['password'] != request.POST['confirmpw']:
        messages.error(request, 'Password and Confirmation must match!')
        error = True
    if error:
        return redirect("/")
    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    this_user = User.objects.create(name=request.POST['name'],alias=request.POST['alias'],email=request.POST['email'],
    password=hash1)
    request.session['id'] = this_user.id
    return redirect("/books")

def books(request):

    context = {
    'user': User.objects.get(id=request.session['id']),
    'books': Review.objects.order_by('-id')[:4],
    'titles': Book.objects.all()
    }

    return render(request, "belt_review/home.html", context)

def login(request):
    try:
        users = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, 'Invalid email')
        return redirect("/")
    if bcrypt.checkpw(request.POST['password'].encode(), users.password.encode()):
        request.session['id'] = users.id
        

    return redirect("/books")

def add(request):

    return render(request, "belt_review/add.html")

def add_book(request, id):
    this_author = Author.objects.create(name=request.POST['author'])
    this_book = Book.objects.create(title=request.POST['title'], book_author=this_author)
    this_review = Review.objects.create(content=request.POST['review'], rating=request.POST['rating'], user_review=User.objects.get(id=id),book_review=this_book)
   
    return redirect("/books/"+str(this_book.id))

def book_review(request,book):
    
    context = {

    'book': Book.objects.get(id=book),
    'reviews': Review.objects.filter(book_review=Book.objects.get(id=book)).order_by('-id')
   
    }
    return render(request, "belt_review/books.html", context)

def new_review(request,id):
   
    Review.objects.create(content=request.POST['content'],rating=request.POST['rating'],book_review=Book.objects.get(id=id),
    user_review=User.objects.get(id=request.session['id']))

    return redirect('/books/'+id)

def user(request,id):
    context = {
        'user': User.objects.get(id=id),
        'book': Review.objects.filter(user_review=User.objects.get(id=id))
    }
    return render(request,'belt_review/user.html', context)