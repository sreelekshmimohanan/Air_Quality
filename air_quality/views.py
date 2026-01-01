from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404 
# FILE UPLOAD AND VIEW
from  django.core.files.storage import FileSystemStorage
# SESSION
from django.conf import settings
from .models import *
from django.contrib import messages

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')


def reg(request):
    return render(request,'register.html')


def addreg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print('POST data:', request.POST)  # Debug print
        if not all([name, email, phone, password]):
            return render(request, 'register.html', {'message': "All fields are required!", 'error': True})
        try:
            ins = register(name=name, email=email, phone=phone, password=password)
            ins.save()
            return render(request, 'register.html', {'message': "Successfully Registered"})
        except Exception as e:
            return render(request, 'register.html', {'message': f"Error: {e}", 'error': True})
    return render(request, 'register.html')

def login(request):
     return render(request,'login.html')
    



def addlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email=='admin@gmail.com' and password =='admin':
        request.session['logint']=email
        return render(request,'index.html')
    elif register.objects.filter(email=email,password=password).exists():
        user=register.objects.get(email=email,password=password)
        request.session['uid']=user.id
        return render(request,'index.html')
    else:
        return render(request,'login.html')
    



def logout(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
          del request.session[key]
    return redirect(first)

def viewuser(request):
    data=register.objects.all()
    return render(request,'viewuser.html',{'data':data})

def upload(request):
    return render(request,'upload.html')

def addupload(request):
    if request.method == 'POST' and request.FILES['fileupload']:
        fileupload = request.FILES['fileupload']
        fs = FileSystemStorage()
        filename = fs.save(fileupload.name, fileupload)
        uploaded_file_url = fs.url(filename)
        user_id=request.session['uid']
        ins=Upload(user_id=user_id,fileupload=uploaded_file_url)
        ins.save()
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')