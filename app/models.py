import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

from mccontracting.values import (GENDERS, USERS_GROUPS, STATUSES, STATUS_NEW_ID, EVALUATION_TYPES,
                                  STATUS_COMPLETED_ID, USERS_GROUP_EMPLOYEES, EVALUATION_TYPE_EXCELLENT,
                                  STATUS_PROGRESS_ID, GENDER_FEMALE_ID)


class Company(models.Model):
    name = models.CharField(max_length=300)
    alias = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company'
        db_table = 'companies'
        ordering = ('name', )


class WorkType(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Work Type'
        verbose_name_plural = 'Work Types'
        unique_together = ('company', 'name')
        db_table = 'work_types'
        ordering = ('name', )

    def has_relations(self):
        return self.task_set.exists()


class Users(models.Model):
    user = models.ForeignKey(User)
    type = models.IntegerField(choices=USERS_GROUPS, default=USERS_GROUP_EMPLOYEES)

    # more data
    phone = models.CharField(max_length=50, blank=True, null=True)
    gender = models.IntegerField(choices=GENDERS, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.FileField(upload_to='avatars/', max_length=100, blank=True, null=True)
    is_supervisor = models.BooleanField(default=False)

    # social media links
    website = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.user, self.get_type_display())

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        unique_together = ('user', )
        ordering = ('user', )

    def is_female(self):
        return self.gender == GENDER_FEMALE_ID

    def get_my_company(self):
        if self.usercompany_set.exists():
            return self.usercompany_set.all()[0].company
        return None

    def get_inverse_name(self):
        return "{} {}".format(self.user.last_name, self.user.first_name)

    def get_inverse_name_short(self):
        return "{}. {}".format(self.user.last_name[:1], self.user.first_name)

    def get_regular_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def get_mobile_e164_format(self):
        phone = ''
        if self.phone:
            phone = "1{}".format(self.phone)
            phone = re.sub(r"\D", "", phone)
        return phone

    def complete_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def short_name_inverse(self):
        return "{} {}".format(self.user.last_name[0], self.user.first_name)

    def short_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name[0],)

    def download_avatar(self):
        if self.avatar:
            return self.avatar.url
        return ''

    def get_my_name_initials(self):
        if self.user:
            if self.user.first_name and self.user.last_name:
                return "{}{}".format(self.user.first_name[0], self.user.last_name[0])
        return self.user.username[:2]


class Project(models.Model):
    company = models.ForeignKey(Company)
    customer = models.ForeignKey(Users)
    name = models.CharField(max_length=300)

    def __str__(self):
        return "{} (Company: {}, Customer: {})".format(self.name, self.company, self.customer)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        db_table = 'projects'
        ordering = ('name', )


class UserCompany(models.Model):
    user = models.ForeignKey(Users)
    company = models.ForeignKey(Company)

    def __str__(self):
        return "{} - {}".format(self.user, self.company)

    class Meta:
        verbose_name = 'User Company'
        verbose_name_plural = 'Users Companies'
        unique_together = ('user', 'company')
        db_table = 'users_companies'
        ordering = ('company', )


class Work(models.Model):
    project = models.ForeignKey(Project)
    supervisor = models.ForeignKey(Users, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.project, self.address)

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'
        db_table = 'works'
        ordering = ('-id',)

    def repr_id(self):
        return str(self.id).zfill(4)

    def get_customer(self):
        return self.project.customer if self.project and self.project.customer else None

    def download_detail_url(self):
        return "/gm/download_work_detail?work_id={}".format(self.id)

    def get_my_tasks(self):
        return self.task_set.all()

    def has_relations(self):
        return self.get_my_tasks().exists()

    def get_number_tasks(self):
        return self.get_my_tasks().count()

    def get_number_tasks_completed(self):
        if self.has_relations():
            return self.get_my_tasks().filter(status=STATUS_COMPLETED_ID).count()
        return 0

    def get_number_tasks_incompleted(self):
        if self.has_relations():
            return self.get_my_tasks().exclude(status=STATUS_COMPLETED_ID).count()
        return 0

    def get_percentage_completed(self):
        total_tasks = self.get_number_tasks()
        completed_tasks = self.get_number_tasks_completed()
        if total_tasks:
            return round(completed_tasks / total_tasks * 100)
        return 0

    def get_status(self):
        status_avg = self.get_my_tasks().aggregate(avg=Avg('status'))['avg']
        return STATUSES[round(status_avg) - 1][1] if status_avg else STATUSES[0][1]

    def is_completed(self):
        return self.get_number_tasks() == self.get_number_tasks_completed()


class Task(models.Model):
    work = models.ForeignKey(Work)

    type = models.ForeignKey(WorkType, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(Users, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    status = models.IntegerField(choices=STATUSES, default=STATUS_NEW_ID)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Data will come from the app
    register_datetime = models.DateTimeField(blank=True, null=True)
    register_latitude = models.FloatField(default=0, blank=True, null=True)
    register_longitude = models.FloatField(default=0, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)

    before_photo1 = models.FileField(upload_to='photos/', blank=True, null=True)
    before_photo2 = models.FileField(upload_to='photos/', blank=True, null=True)
    before_photo3 = models.FileField(upload_to='photos/', blank=True, null=True)
    before_photo4 = models.FileField(upload_to='photos/', blank=True, null=True)

    after_photo1 = models.FileField(upload_to='photos/', blank=True, null=True)
    after_photo2 = models.FileField(upload_to='photos/', blank=True, null=True)
    after_photo3 = models.FileField(upload_to='photos/', blank=True, null=True)
    after_photo4 = models.FileField(upload_to='photos/', blank=True, null=True)

    # Customer Evaluation
    evaluation = models.IntegerField(choices=EVALUATION_TYPES, default=EVALUATION_TYPE_EXCELLENT)
    sign = models.FileField(upload_to='signs/', blank=True, null=True)

    def repr_id(self):
        return str(self.id).zfill(4)

    def get_customer(self):
        return self.work.get_customer()

    def get_date_time(self):
        return self.date_time.strftime("%m/%d/%y %I:%M%p")

    def get_register_time(self):
        return self.register_time.strftime("%m/%d/%y %I:%M%p")

    def get_end_time(self):
        return self.end_time.strftime("%m/%d/%y %I:%M%p")

    def download_photo1_before(self):
        if self.before_photo1:
            return self.before_photo1.url
        return ''

    def download_photo2_before(self):
        if self.before_photo2:
            return self.before_photo2.url
        return ''

    def download_photo3_before(self):
        if self.before_photo3:
            return self.before_photo3.url
        return ''

    def download_photo4_before(self):
        if self.before_photo4:
            return self.before_photo4.url
        return ''

    def download_photo1_after(self):
        if self.after_photo1:
            return self.after_photo1.url
        return ''

    def download_photo2_after(self):
        if self.after_photo2:
            return self.after_photo2.url
        return ''

    def download_photo3_after(self):
        if self.after_photo3:
            return self.after_photo3.url
        return ''

    def download_photo4_after(self):
        if self.after_photo4:
            return self.after_photo4.url
        return ''

    def download_signature(self):
        if self.sign:
            return self.sign.url
        return ''

    def is_new(self):
        return self.status == STATUS_NEW_ID

    def is_progress(self):
        return self.status == STATUS_PROGRESS_ID

    def is_completed(self):
        return self.status == STATUS_COMPLETED_ID
