from django.contrib import admin
from . import models # ๐ ํด๋น model์ด ์กด์ฌํ๋ ํ์ผ์ import
@admin.register(models.User) # ๐ ๋ฐ์ฝ๋ ์ดํฐ๋ก ๋ฑ๋ก
class CustomUserAdmin(admin.ModelAdmin):
    pass