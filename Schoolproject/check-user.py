from SchoolManage.models import CustomUser

user = CustomUser.objects.get(username='admin')  # Replace 'admin' with your username
print(user.is_staff)


