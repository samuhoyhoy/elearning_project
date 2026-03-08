from django.contrib import admin
from .models import UserProfile

# register the profile model so it shows up in Django's admin site
admin.site.register(UserProfile)

# admin login details
# username: admin
# email: admin@email.com
# password: 1234

# teacher1 login details
# username: teacher1
# email: teacher1@email.com
# password: Sunnydays3
# name: Alice Teacher

# teacher2 login details
# username: teacher2
# email: teacher2@email.com
# password: Sunnydays3
# name: Jane Teacher

# student1 login details
# username: student1
# email: student1@email.com
# password: Sunnydays3
# name: Bob Student
