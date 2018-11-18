from django.contrib import admin

from app.models import Company, Users, Project, WorkType, Work, UserCompany, Task


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'alias')
    search_fields = ('name', 'alias')
    ordering = ('name',)


admin.site.register(Company, CompanyAdmin)


class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('company', )


admin.site.register(WorkType, WorkTypeAdmin)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'phone', 'gender', 'birthday')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    ordering = ('user',)
    list_filter = ('type', 'gender')


admin.site.register(Users, UsersAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('company', )


admin.site.register(Project, ProjectAdmin)


class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'user')
    ordering = ('company',)
    list_filter = ('company', )


admin.site.register(UserCompany, UserCompanyAdmin)


class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'supervisor', 'address', 'notes')
    search_fields = ('project__name', )
    ordering = ('-id', '-created_at')
    list_filter = ('supervisor', )


admin.site.register(Work, WorkAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'work', 'assigned_to', 'address', 'date_time', 'type', 'status')
    search_fields = ('work', )
    ordering = ('-id', '-created_at')
    list_filter = ('status', 'type', 'work__supervisor')


admin.site.register(Task, TaskAdmin)
