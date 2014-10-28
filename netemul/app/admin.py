from django.contrib import admin
from app.models import Blog
from app.models import User_login
from app.models import UserProfile

admin.site.register(Blog)
admin.site.register(User_login)
admin.site.register(UserProfile)

