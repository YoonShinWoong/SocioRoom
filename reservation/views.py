from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from django.utils import timezone

########################## C
def new(request):
    return render(request, 'reservation/new.html')

# C
def create(request):
    reservation = Reservation() # 객체 만들기
    reservation.room_type = request.GET['room_type']  # 내용 채우기
    reservation.room_date= request.GET['room_date'] # 내용 채우기
    reservation.room_start_time = request.GET['room_start_time']  # 내용 채우기
    reservation.room_finish_time= request.GET['room_finish_time'] # 내용 채우기
    reservation.pub_date = timezone.datetime.now() # 내용 채우기
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
    return render(request, 'reservation/edit.html', {'reservation':reservation})

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