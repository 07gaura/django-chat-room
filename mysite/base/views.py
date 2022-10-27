from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .models import Room,Topic,Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
# Create your views here.
from .forms import RoomForm,UserForm

def logutUser(request):
    logout(request)
    return redirect('home')

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user does not exist")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "user or password doesnot exist")
    context = {'page':page}
    return render(request,'base/login.html',context)

def registerUser(request):
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'base/login.html', {'form':form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__contains=q)|
                                Q(name__icontains=q)|
                                Q(description__icontains=q)
                                )
    room_counts = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms,'topics':topics,'room_counts':room_counts,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    particants = room.participants.all()
    if request.method=="POST":
        if request.user.is_authenticated:
            message = Message.objects.create(
                user = request.user,
                room = room,
                body=request.POST.get('body')
            )
        else:
            return redirect('Login')
        room.participants.add(request.user)
        return redirect('Room',pk=room.id)
    context = {"rooms":room,"messages":room_messages,'participants':particants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all().order_by('-created')
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,"room_messages":room_messages,"topics":topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        #if form.is_valid():
        #    room = form.save(commit=False)
        #    room.host = request.user
        #    room.save()
        return redirect('home')
    context = {'form':form,'topic':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='Login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("you are not allowed here!!")
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form,"topics":topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='Login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='Login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method=="POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('Profile')
    return render(request,'base/edit-user.html',{'form':form})

def topicsPage(request):
    topics = Topic.objects.all()
    return render(request,'base/topics_page.html',{"topics":topics})

def recentPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/recent_activity_page.html',{"room_messages":room_messages})