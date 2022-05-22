from operator import mod
from django.db import models

from core_app.models import BaseModel
from user_app.models import User
from group_app.models import Group


# Course
class Course(BaseModel):
    name = models.CharField(max_length=100)
    cover_pic = models.ImageField(upload_to='course_cover_pic', null=True, blank=True)
    hour_per_class = models.CharField(max_length=100)
    class_per_week = models.CharField(max_length=100)
    total_class = models.CharField(max_length=100)
    total_class_hour = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    course_topic = models.CharField(max_length=255)
    course_outcome = models.TextField()
    course_reward = models.CharField(max_length=255)
    enrollment_requirement = models.TextField()
    course_responsibility = models.TextField()
    course_enroll_start_date = models.DateField()
    course_enroll_end_date = models.DateField()
    enrollment_fee = models.CharField(max_length=100)
    payment_procedure = models.CharField(max_length=100)
    max_student = models.PositiveBigIntegerField(default=0)
    disclaimer_from_group = models.TextField()
    course_availability = models.BooleanField(default=False)
    student_count = models.PositiveBigIntegerField(default=0)
    #added for like
    liked_by = models.ManyToManyField(User, related_name='course_liked_by')

    def __str__(self):
        return self.name


# Course Staff
class CourseStaff(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_staff_course')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_staff_user')
    role = models.CharField(max_length=150)

    def as_json(self):
        return dict(
            id=self.id,
            course=self.course,
            staff=self.staff,
            role=self.role)


# Course Student Enrollment
class CourseStudentEnrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(("Paid"), default=False)


# Course Enrollment Payment
class CourseEnrollmentPayment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    number = models.CharField(max_length=25)
    transaction_id = models.CharField(max_length=120)
    amount = models.PositiveBigIntegerField()
    payment_date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


# Course Notice
class CourseNotice(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    notice = models.TextField()


# Course Class Link
class CourseClassLink(BaseModel):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    url_link = models.URLField(max_length=250)


# Group Course
class GroupCourse(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='course_group')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='group_course')


# Course Class Routine
class CourseClassRouting(BaseModel):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    sat = models.CharField(max_length=100, null=True, blank=True)
    sun = models.CharField(max_length=100, null=True, blank=True)
    mon = models.CharField(max_length=100, null=True, blank=True)
    tue = models.CharField(max_length=100, null=True, blank=True)
    wed = models.CharField(max_length=100, null=True, blank=True)
    thu = models.CharField(max_length=100, null=True, blank=True)
    fri = models.CharField(max_length=100, null=True, blank=True)

