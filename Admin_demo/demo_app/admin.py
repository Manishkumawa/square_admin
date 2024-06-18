from django.contrib import admin

# Register your models here.

from demo_app.models import UserData

'''
admin.site.site_title = "Square Insurance Panel"
admin.site.site_header = "Square Insurance Administration"
admin.site.index_title = "Site administration"
'''


  
   
admin.site.register(UserData)


