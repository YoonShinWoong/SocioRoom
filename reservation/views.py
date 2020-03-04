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
    # 요일 가져오기
    today =  datetime.now()
    today_day = today.weekday()

    weekday_mark = 0
    # 토, 일 경우 -> 다음주와 돌아오는 그 다음주까지 예약가능
    if today_day>=5:
        weekday_mark = 7-today_day # 주말차이 표시
        today_day -= 7
    date_diff = 4-today_day
    return render(request, 'reservation/new.html', {'room_type':room_type, 'date_diff':date_diff, 'weekday_mark':weekday_mark})

# ajax 통신
def check(request):
    room_type_vr = request.POST.get('room_type', None)
    room_date_vr = request.POST.get('room_date', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    room_start_time_vr = request.POST.get('room_start_time', None)
    room_finish_time_vr = request.POST.get('room_finish_time', None)
    
    reservations = Reservation.objects.all()
    reserve_date = datetime.strptime(room_date_vr, "%Y-%m-%d ").date()
    check_error = 0 # 정상

    print(room_type_vr, room_date_vr, room_start_time_vr, room_finish_time_vr)

    # 하루 2건 검사
    if reservations.filter(user=request.user.username, room_date=reserve_date).count() >= 2:
        message="해당일에 이미 2건의 예약을 하셨습니다"
        check_error = 1
        context = { 'message': message,
                    'check_error': check_error}
        return HttpResponse(json.dumps(context), content_type="application/json")


    # 겹치는 시간 있는지 체크
    message="이미 예약된 시간입니다"

    # <1> 오른쪽 겹치기
    if reservations.filter(room_type=room_type_vr,room_date=reserve_date, room_finish_time__gt=room_start_time_vr, room_start_time__lt=room_finish_time_vr ).count() != 0:
        check_error = 1   
        context = { 'message': message,
                    'check_error': check_error}
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <2> 사이 들어가기
    if reservations.filter(room_type=room_type_vr,room_date=reserve_date, room_start_time__lte=room_start_time_vr, room_finish_time__gte=room_finish_time_vr ).count() != 0:
        check_error = 1   
        context = { 'message': message,
                    'check_error': check_error}
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <3> 오른쪽 포개지기
    if reservations.filter(room_type=room_type_vr,room_date=reserve_date, room_start_time__lt=room_finish_time_vr, room_finish_time__gt=room_start_time_vr ).count() != 0:
        check_error = 1   
        context = { 'message': message,
                    'check_error': check_error}
        return HttpResponse(json.dumps(context), content_type="application/json")
    # <4> 밖에 감싸기
    if reservations.filter(room_type=room_type_vr,room_date=reserve_date, room_start_time__gte=room_start_time_vr, room_finish_time__lte=room_finish_time_vr ).count() != 0:
        check_error = 1   
        context = { 'message': message,
                    'check_error': check_error}
        return HttpResponse(json.dumps(context), content_type="application/json")

    # <4> 가능
    context = { 'message': message,
                'check_error': check_error}
    return HttpResponse(json.dumps(context), content_type="application/json")

# C
@login_required
def create(request):
    reserve_date = datetime.strptime(request.GET['room_date'], "%Y-%m-%d ").date()

    # 만들기
    reservation = Reservation() # 객체 만들기
    reservation.user = request.GET['user']  # 내용 채우기
    reservation.room_type = request.GET['room_type']  # 내용 채우기
    reservation.room_date= reserve_date # 내용 채우기

    # 시간 구하기
    reservation.room_start_time = request.GET['room_start_time']  # 내용 채우기
    reservation.room_finish_time= request.GET['room_finish_time'] # 내용 채우기
    reservation.pub_date = timezone.datetime.now() # 내용 채우기
    reservation.save() # 객체 저장하기

    # 내 예약 주소
    return redirect('/reservation/my')               

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
    if reservation.user == request.user.username:
        reservation.delete()
    return redirect('/reservation/my')                
    
########################## MY 예약
@login_required
def myreservation(request):
    today = datetime.now().strftime("%Y-%m-%d") # 오늘날짜
    reservations = Reservation.objects.all()
    reservation_list = reservations.filter(user=request.user.username, room_date__gte=today) # 내 예약들
    return render(request, 'reservation/myreservation.html',{'reservation_list':reservation_list}) 
    