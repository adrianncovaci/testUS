from django.contrib import admin
from User.models import Account, Student, Test, Professor, Class, Submission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'first_name', 'last_name' )}),
#         ('Permissions', {'fields': (
#             'active',
#             'staff',
#             'superuser',
#             'groups',
#             'user_permissions',
#         )}),
#     )
#     # add_fieldsets = (
#     #     (
#     #         None,
#     #         {
#     #             'classes': ('wide',),
#     #             'fields': ('email', 'password1')
#     #         }
#     #     ),
#     # )

#     list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
#     list_filter = ('staff', 'superuser', 'active', 'groups')
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Account)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Test)
admin.site.register(Submission)