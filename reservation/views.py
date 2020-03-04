from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

########################## C
@login_required
def new(request,room_type):
    min_date = datetime.now().strftime("%Y-%m-%d") # 오늘부터 
    max_date = (datetime.now() +timedelta(days=14)).strftime("%Y-%m-%d") # 14일 후까지 가능
    return render(request, 'reservation/new.html', {'room_type':room_type, 'min_date':min_date, 'max_date':max_date})

# ajax 통신
def check(request):
    room_type = request.POST.get('room_type', None)
    room_date = request.POST.get('room_date', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    
    message= "통신 성공"
    print(room_type)
    print(room_date)
    context = { 'message': message,
                'room_type': room_type,
                'room_date': room_date
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

# C
@login_required
def create(request):
    reservation = Reservation() # 객체 만들기
    reservation.user = request.GET['user']  # 내용 채우기
    reservation.room_type = request.GET['room_type']  # 내용 채우기
    reservation.room_date= request.GET['room_date'] # 내용 채우기

    # 시간 구하기
    reservation.room_start_time = request.GET['room_start_time']  # 내용 채우기
    reservation.room_finish_time= request.GET['room_finish_time'] # 내용 채우기
    reservation.pub_date = timezone.datetime.now() # 내용 채우기

    # 하루 2건 검사


    # 하루 4시간 검사


    reservation.save() # 객체 저장하기

    # 새로운 예약 url 주소로 이동
    return redirect('/reservation/' + str(reservation.id))

########################## R
def home(request):
    reservations = Reservation.objects # 객체 묶음 가져오기
    return render(request, 'reservation/home.html', {'reservations':reservations})
    # render라는 함수를 통해 페이지를 띄워줄 건데, home.html 파일을 띄워줄 것이고 
    # 이 때, reservations 객체도 함께 넘겨주도록 하겠다.

# R 
def detail(request, reservation_id) : 
    reservation_detail = get_object_or_404(Reservation, pk= reservation_id) # 특정 객체 가져오기(없으면 404 에러)
    return render(request, 'reservation/detail.html', {'reservation':reservation_detail})

########################## U
def edit(request,reservation_id):
    reservation = get_object_or_404(Reservation, pk= reservation_id) # 특정 객체 가져오기(없으면 404 에러)
    min_date = datetime.now().strftime("%Y-%m-%d") # 오늘부터 
    max_date = (datetime.now() +timedelta(days=14)).strftime("%Y-%m-%d") # 14일 후까지 가능
    return render(request, 'reservation/edit.html', {'reservation':reservation, 'min_date':min_date, 'max_date':max_date})

# U
def update(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk= reservation_id) # 특정 객체 가져오기(없으면 404 에러)
    reservation.room_type = request.GET['room_type']  # 내용 채우기
    reservation.room_date= request.GET['room_date'] # 내용 채우기
    reservation.room_start_time = request.GET['room_start_time']  # 내용 채우기
    reservation.room_finish_time= request.GET['room_finish_time'] # 내용 채우기
    reservation.save() # 객체 저장하기

    # 새로운 예약 url 주소로 이동
    return redirect('/reservation/' + str(reservation.id))

########################## D
def delete(request, reservation_id):
    reservation= get_object_or_404(Reservation, pk= reservation_id) # 특정 객체 가져오기(없으면 404 에러)
    reservation.delete()
    return redirect('home') # home 이름의 url 로

########################## MY 예약
@login_required
def myreservation(request):
    today = datetime.now().strftime("%Y-%m-%d") # 오늘날짜
    reservations = Reservation.objects.all()
    reservation_list = reservations.filter(user=request.user.username, pub_date__gte=today) # 내 예약들
    return render(request, 'reservation/myreservation.html',{'reservation_list':reservation_list}) 
    