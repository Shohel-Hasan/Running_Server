from rest_framework import serializers

from user_app.models import User
from user_app.serializers import UserSerializer
from social_app.models import CommentModel
from social_app.serializers import CommentSerializer
from course_app.models import (
    Course,
    CourseClassRouting,
    CourseEnrollmentPayment,
    CourseStaff,
    CourseStudentEnrollment,
    CourseNotice,
    CourseClassLink
)


class CourseClassRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseClassRouting
        fields = "__all__"


# Course Model Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class TeacherCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = CourseStaff
        fields = '__all__'


# Course Model Serializer for Create Course
class CourseCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    cover_pic = serializers.ImageField()
    hour_per_class = serializers.CharField(max_length=100)
    class_per_week = serializers.CharField(max_length=100)
    total_class = serializers.CharField(max_length=100)
    total_class_hour = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    course_topic = serializers.CharField(max_length=255)
    course_outcome = serializers.CharField()
    course_reward = serializers.CharField(max_length=255)
    enrollment_requirement = serializers.CharField()
    course_responsibility = serializers.CharField()
    course_enroll_start_date = serializers.DateField()
    course_enroll_end_date = serializers.DateField()
    enrollment_fee = serializers.CharField(max_length=100)
    payment_procedure = serializers.CharField(max_length=100)
    max_student = serializers.IntegerField(default=0)
    disclaimer_from_group = serializers.CharField()
    course_availability = serializers.BooleanField(default=False)
    student_count = serializers.IntegerField(default=0)
    sat = serializers.CharField(max_length=100, required=False)
    sun = serializers.CharField(max_length=100, required=False)
    mon = serializers.CharField(max_length=100, required=False)
    tue = serializers.CharField(max_length=100, required=False)
    wed = serializers.CharField(max_length=100, required=False)
    thu = serializers.CharField(max_length=100, required=False)
    fri = serializers.CharField(max_length=100, required=False)


# Course Model Serializer for Group Course
class CourseGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group_id = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    group_cover_pic = serializers.SerializerMethodField()
    group_profile_pic = serializers.SerializerMethodField()
    group_about = serializers.SerializerMethodField()
    group_verify = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    liked_by = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'user',
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
            'student_count',
            'group_id',
            'owner_id',
            'group_name',
            'group_cover_pic',
            'group_profile_pic',
            'group_about',
            'group_verify',
            'comments',
            'like_count',
            'liked_by'
        )

    def get_group_id(self, obj):
        for group in obj.group_course.all():
            return group.group.id

    def get_owner_id(self, obj):
        for group in obj.group_course.all():
            return group.group.creator.id

    def get_group_name(self, obj):
        for group in obj.group_course.all():
            return group.group.name

    def get_group_cover_pic(self, obj):
        for group in obj.group_course.all():
            return group.group.cover_pic.url

    def get_group_profile_pic(self, obj):
        for group in obj.group_course.all():
            return group.group.profile_pic.url

    def get_group_about(self, obj):
        for group in obj.group_course.all():
            return group.group.about

    def get_group_verify(self, obj):
        for group in obj.group_course.all():
            return group.group.is_verified

    def get_comments(self, obj):
        comments = CommentModel.objects.filter(parent__isnull=True, course=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_like_count(self, instance):
        return instance.liked_by.count()


# CourseEnrollment Model Serializer
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_academic_discipline = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    student_first_name = serializers.SerializerMethodField()
    student_profession = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    course_cover_pic = serializers.SerializerMethodField()
    course_student_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseStudentEnrollment
        fields = (
            'id',
            'course',
            'student',
            'is_paid',
            'student_academic_discipline',
            'student_email',
            'student_first_name',
            'student_profession',
            'course_name',
            'course_cover_pic',
            'course_student_count',
        )

    def get_student_academic_discipline(self, obj):
        student = obj.student.academic_discipline
        return student

    def get_student_email(self, obj):
        student = obj.student.email
        return student

    def get_student_first_name(self, obj):
        student = obj.student.first_name
        return student

    def get_student_profession(self, obj):
        student = obj.student.profession
        return student

    def get_course_name(self, obj):
        course = obj.course.name
        return course

    def get_course_cover_pic(self, obj):
        try:
            course = obj.course.cover_pic.url
            return course
        except:
            course = ''
            return course

    def get_course_student_count(self, obj):
        course = obj.course.student_count
        return course


# CourseNotice Model Serializer
class CourseNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseNotice
        fields = (
            'id',
            'course',
            'notice',
        )


# CourseClassLink Model Serializer
class CourseClassLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseClassLink
        fields = (
            'id',
            'course',
            'url_link',
        )


# CourseStaff Model Serializer
class CourseStaffSerializer(serializers.ModelSerializer):
    staff_academic_discipline = serializers.SerializerMethodField()
    staff_email = serializers.SerializerMethodField()
    staff_first_name = serializers.SerializerMethodField()
    staff_profession = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    course_cover_pic = serializers.SerializerMethodField()
    course_student_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseStaff
        fields = (
            'id',
            'course',
            'staff',
            'role',
            'staff_academic_discipline',
            'staff_email',
            'staff_first_name',
            'staff_profession',
            'course_name',
            'course_cover_pic',
            'course_student_count',
        )

    def get_staff_academic_discipline(self, obj):
        staff = obj.staff.academic_discipline
        return staff

    def get_staff_email(self, obj):
        staff = obj.staff.email
        return staff

    def get_staff_first_name(self, obj):
        staff = obj.staff.first_name
        return staff

    def get_staff_profession(self, obj):
        staff = obj.staff.profession
        return staff

    def get_course_name(self, obj):
        course = obj.course.name
        return course

    def get_course_cover_pic(self, obj):
        try:
            course = obj.course.cover_pic.url
            return course
        except:
            course = ''
            return course

    def get_course_student_count(self, obj):
        course = obj.course.student_count
        return course


# CourseEnrollmentPayment Model Serializer
class CourseEnrollmentPaymentSerializer(serializers.ModelSerializer):
    student_academic_discipline = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    student_first_name = serializers.SerializerMethodField()
    student_profile_pic = serializers.SerializerMethodField()
    student_profession = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    course_cover_pic = serializers.SerializerMethodField()
    course_student_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseEnrollmentPayment
        fields = (
            'id',
            'course',
            'course_name',
            'student_profile_pic',
            'course_cover_pic',
            'course_student_count',
            'student',
            'student_academic_discipline',
            'student_email',
            'student_first_name',
            'student_profession',
            'payment_method',
            'number',
            'transaction_id',
            'amount',
            'payment_date',
            'is_verified',
        )

    def get_student_academic_discipline(self, obj):
        student = obj.student.academic_discipline
        return student

    def get_student_email(self, obj):
        student = obj.student.email
        return student

    def get_student_first_name(self, obj):
        student = obj.student.first_name
        return student

    def get_student_profile_pic(self, obj):
        try:
            student = obj.student.general_info_user.profile_pic.url
            return student
        except:
            return ''

    def get_student_profession(self, obj):
        student = obj.student.profession
        return student

    def get_course_name(self, obj):
        course = obj.course.name
        return course

    def get_course_cover_pic(self, obj):
        try:
            course = obj.course.cover_pic.url
            return course
        except:
            course = ''
            return course

    def get_course_student_count(self, obj):
        course = obj.course.student_count
        return course
