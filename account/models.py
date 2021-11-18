from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.CharField(max_length=20, primary_key = True, verbose_name ='사용자 아이디')
    first_name = None
    last_name = None

class Serial(models.Model):
    serial_number = models.CharField(primary_key = True, max_length=50,verbose_name='서버에 등록된 시리얼 넘버')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='등록 날짜')
    deleted_date = models.DateTimeField(null=True,verbose_name='만료 날짜')
    class Meta:
        db_table = 'serial_number_list'
        
class Device(models.Model):
    serial_number = models.ForeignKey(Serial, unique=True ,on_delete=models.CASCADE, related_name='device')
    gps_module_info = models.CharField(max_length=100,verbose_name='GPS 모듈 정보')
    camera_module_info = models.CharField(max_length=100,verbose_name='카메라 모듈 정보')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='기기 소유주') # to be determined
    class Meta:
        db_table = 'device_info_list'
        
class Status(models.Model):
    device_id = models.ForeignKey(Device, unique=True, on_delete=models.CASCADE, related_name='status')
    mode = models.CharField(max_length=1, default='N', verbose_name='디바이스 모드 normal/emergency')
    latitude = models.FloatField(default=0.0, verbose_name='위도')
    longitude = models.FloatField(default=0.0, verbose_name='경도')
    altitude = models.FloatField(default=0.0, verbose_name='고도')
    latest_updated_time = models.DateTimeField(auto_now=True, verbose_name='최근 업데이트한 시간')
    ONF = models.BooleanField(default=True, verbose_name='디바이스 On/Off 상태 정보')
    #IP = models.CharField(default='', verbose_name='IP정보', max_length=50)
    IP = models.GenericIPAddressField(null=True, verbose_name='IP정보')
    class Meta:
        db_table = 'device_status_list'

        
class Permission(models.Model):
    user_id = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='기기에 연결된 사용자', related_name='permission_user_id')
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='기기에 연결된 디바이스', related_name='permission_device_id')
    ROLE_PROTECTOR = "protector"
    ROLE_PROTEGE = "protege"
    ROLE_OBSERVER = "observer" 
    ROLE_OTHER = "other"
    ROLE_CHOICES = (
        (ROLE_PROTECTOR, "Protector"),
        (ROLE_PROTEGE, "Protege"),
        (ROLE_OBSERVER, "Observer"),
        (ROLE_OTHER, "Other"),
    )
    role = models.CharField(
        choices=ROLE_CHOICES, max_length=10,
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='수정날짜')
    # deleted_date = models.DateTimeField(null=True, verbose_name='연결해제날짜')
    class Meta:
        db_table = 'permission_list'
        unique_together = (('user_id', 'device_id'),)
        
class Attachment(models.Model):
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='등록 기기')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='owner user')
    TYPE_VIDEO = "video"
    TYPE_AUDIO = "audio"
    TYPE_IMAGE = "image" 
    TYPE_OTHER = "other"
    TYPE_CHOICES = (
        (TYPE_VIDEO, "Video"),
        (TYPE_AUDIO, "Audio"),
        (TYPE_IMAGE, "Image"),
        (TYPE_OTHER, "Other"),
    )
    tyep = models.CharField(
        choices = TYPE_CHOICES, max_length=10,
    )
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    def file_path_for_db(instance, filename): # user와 날짜에 따른 경로 생성을 위한 함수
        pass
    recorded_path = models.FileField(upload_to=file_path_for_db)
    
class History(Status):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='history테이블에 기록된 시간')
    class Meta:
        db_table = 'device_status_history_list'
        unique_together = (('user_id', 'created_time'),)
    
    