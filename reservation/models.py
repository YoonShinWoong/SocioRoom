from django.db import models
from django.utils import timezone

# Create your models here.
class Reservation(models.Model): # Resrvation 라는 이름의 객체 틀(Model) 생성
    room_type = models.CharField(max_length=10) # 방 종류
    room_date =  models.CharField(max_length=10) # 예약 날짜
    room_start_time = models.CharField(max_length=10) # 시작 시간
    room_finish_time = models.CharField(max_length=10) # 종료 시간
    pub_date = models.DateTimeField(default=timezone.now) # pub_date 라는 날짜 시간 데이터 저장