from django.contrib import admin
from course_app.models import (
    CourseEnrollmentPayment, 
    Course, 
    CourseStaff, 
    CourseNotice, 
    CourseClassLink, 
    GroupCourse,
    CourseEnrollmentPayment, 
    CourseStudentEnrollment,
    CourseClassRouting
    )

from django.shortcuts import get_object_or_404
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'cover_pic', 
        'hour_per_class', 
        'class_per_week', 
        'total_class',
        'total_class_hour', 
        'start_date', 
        'end_date',
        'course_topic',
        'course_outcome', 
        'course_reward', 
        'enrollment_requirement',
        'course_responsibility', 
        'course_enroll_start_date', 
        'course_enroll_end_date', 
        'enrollment_fee',
        'payment_procedure', 
        'max_student', 
        'disclaimer_from_group', 
        'course_availability',
        'student_count'
        ]


@admin.register(CourseStaff)
class CourseStaffAdmin(admin.ModelAdmin):
    list_display = [
        'course', 
        'staff', 
        'role'
        ]


@admin.register(CourseStudentEnrollment)
class CourseStudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'course', 
        'student', 
        'is_paid'
        ]


@admin.register(CourseNotice)
class CourseNoticeAdmin(admin.ModelAdmin):
    list_display = [
        'course', 
        'notice'
        ]


@admin.register(CourseClassLink)
class CourseClassLinkAdmin(admin.ModelAdmin):
    list_display = [
        'course', 
        'url_link'
        ]


@admin.register(GroupCourse)
class GroupCourseAdmin(admin.ModelAdmin):
    list_display = [
        'group', 
        'course'
        ]


class CoursePaymentAdmin(admin.ModelAdmin):
    actions = ['make_paid']
    list_display = [
        'course', 
        'student', 
        'payment_method', 
        'number', 
        'transaction_id', 
        'amount', 
        'payment_date',
        'is_verified'
        ]
    list_filter = [
        'is_verified', 
        'payment_date', 
        'course'
        ]

    
    
    @admin.action(description='Mark selected enrollment as Paid')
    def make_paid(self, request, queryset):
        queryset.update(is_verified=True)
        for obj in queryset:
            enroll_instance = CourseStudentEnrollment.objects.filter(course=obj.course, student=obj.student).exists()
            if enroll_instance:
                enroll = CourseStudentEnrollment.objects.get(course=obj.course, student=obj.student)
                if enroll:
                    enroll.is_paid = True
                    enroll.save()
            
            
        


admin.site.register(CourseEnrollmentPayment, CoursePaymentAdmin)
admin.site.register(CourseClassRouting)

