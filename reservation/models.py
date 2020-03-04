from django.db import models
from django.utils import timezone

# Create your models here.
class Reservation(models.Model): # Resrvation 라는 이름의 객체 틀(Model) 생성
    user = models.CharField(max_length=10) # 예약자학번
    room_type = models.CharField(max_length=10) # 방 종류
    room_date =  models.DateField(max_length=20) # 예약 날짜
    room_start_time = models.FloatField() # 시작 시간 0900
    room_finish_time = models.FloatField() # 종료 시간 2100
    pub_date = models.DateTimeField(default=timezone.now) # pub_date 라는 날짜 시간 데이터 저장