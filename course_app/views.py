import json
from urllib import response
from django.core import serializers as d_serializers

from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics
from rest_framework.views import APIView

from course_app.models import (
    Course,
    CourseClassRouting,
    CourseEnrollmentPayment,
    CourseStudentEnrollment,
    CourseNotice,
    GroupCourse,
    CourseStaff,
    CourseClassLink
)

from course_app.serializers import (
    CourseClassRoutineSerializer,
    CourseEnrollmentPaymentSerializer,
    CourseEnrollmentSerializer,
    CourseSerializer,
    CourseNoticeSerializer,
    CourseClassLinkSerializer,
    CourseStaffSerializer,
    CourseGroupSerializer,
    CourseCreateSerializer, TeacherCourseSerializer
)

from group_app.models import Group, GroupMember
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import datetime

# Create your views here.
from user_app.models import User


class CourseVeiwset(viewsets.ViewSet):
    """Course Viewset"""
    queryset = Course.objects.prefetch_related('group_course').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """course List"""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def all_course_of_group(self, request, group_pk):
        """all course"""
        group_course = Course.objects.filter(group_course__group=group_pk).prefetch_related('group_course')
        if group_course.exists():
            serializer = CourseGroupSerializer(group_course, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"message": "Group Not Found"}, status.HTTP_404_NOT_FOUND)

    def single_course(self, request, course_pk):
        """single course"""
        single_course_instance = Course.objects.filter(pk=course_pk).exists()
        if single_course_instance:
            single_course = Course.objects.prefetch_related('group_course').get(pk=course_pk)
            if single_course:
                serilizer = CourseGroupSerializer(single_course)
                return Response(serilizer.data, status.HTTP_200_OK)
            else:
                return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)

    def single_course_update(self, request, course_pk, *args, **kwargs):
        """Single Course Update"""
        course_instance = Course.objects.filter(pk=course_pk, coursestaff__staff=request.user,
                                                coursestaff__role="Admin").exists()
        if course_instance:
            course = Course.objects.get(pk=course_pk, coursestaff__staff=request.user, coursestaff__role="Admin")
            if course:
                partial = kwargs.pop('partial', True)
                serializer = self.serializer_class(course, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Course Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group or course does not match"}, status.HTTP_400_BAD_REQUEST)

    def single_course_by_group(self, request, group_pk, course_pk):
        """single course"""
        single_course_instance = Course.objects.filter(group_course__group=group_pk, pk=course_pk).exists()
        if single_course_instance:
            single_course = Course.objects.prefetch_related('group_course').get(group_course__group=group_pk,
                                                                                pk=course_pk)
            if single_course:
                serilizer = CourseGroupSerializer(single_course)
                return Response(serilizer.data, status.HTTP_200_OK)
            else:
                return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)

    def search_course(self, request):
        """search course"""
        search = request.GET.get("name")
        if search is not None:
            qs = self.queryset
            result = qs.filter(Q(name__icontains=search)).distinct()
            serializer = self.serializer_class(result, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "Not Found"}, status.HTTP_404_NOT_FOUND)

    def create(self, request, group_pk):
        """Course Create"""
        group_instance = Group.objects.filter(pk=group_pk)
        if group_instance:
            group = Group.objects.get(pk=group_pk)
            if group.creator == request.user:
                serializer = CourseCreateSerializer(data=request.data)
                if serializer.is_valid():
                    course = Course.objects.create(
                        name=serializer.validated_data.get('name'),
                        cover_pic=serializer.validated_data.get('cover_pic'),
                        # profile_pic= serializer.validated_data.get('profile_pic'),
                        hour_per_class=serializer.validated_data.get('hour_per_class'),
                        class_per_week=serializer.validated_data.get('class_per_week'),
                        total_class=serializer.validated_data.get('total_class'),
                        total_class_hour=serializer.validated_data.get('total_class_hour'),
                        start_date=serializer.validated_data.get('start_date'),
                        end_date=serializer.validated_data.get('end_date'),
                        course_topic=serializer.validated_data.get('course_topic'),
                        course_outcome=serializer.validated_data.get('course_outcome'),
                        course_reward=serializer.validated_data.get('course_reward'),
                        enrollment_requirement=serializer.validated_data.get('enrollment_requirement'),
                        course_responsibility=serializer.validated_data.get('course_responsibility'),
                        course_enroll_start_date=serializer.validated_data.get('course_enroll_start_date'),
                        course_enroll_end_date=serializer.validated_data.get('course_enroll_end_date'),
                        enrollment_fee=serializer.validated_data.get('enrollment_fee'),
                        payment_procedure=serializer.validated_data.get('payment_procedure'),
                        max_student=serializer.validated_data.get('max_student'),
                        disclaimer_from_group=serializer.validated_data.get('disclaimer_from_group'),
                        course_availability=serializer.validated_data.get('course_availability'),
                        student_count=serializer.validated_data.get('student_count')
                    )
                    # CourseStaff.objects.create(course=course, staff=request.user, role="Admin")
                    GroupCourse.objects.create(course=course, group=group)
                    CourseClassRouting.objects.create(
                        course=course,
                        sat=serializer.validated_data.get('sat'),
                        sun=serializer.validated_data.get('sun'),
                        mon=serializer.validated_data.get('mon'),
                        tue=serializer.validated_data.get('tue'),
                        wed=serializer.validated_data.get('wed'),
                        thu=serializer.validated_data.get('thu'),
                        fri=serializer.validated_data.get('fri')
                    )
                    course_serializer = CourseSerializer(course)
                    return Response(course_serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message", "Not Authorized"}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "No Group Found"}, status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, group_pk, course_pk, *args, **kwargs):
        """Course Update"""
        group_course = Course.objects.filter(group_course__group=group_pk, pk=course_pk).exists()
        if group_course:
            course = Course.objects.get(group_course__group=group_pk, pk=course_pk)
            if course:
                partial = kwargs.pop('partial', True)
                serializer = self.serializer_class(course, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Course Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group or course does not match"}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, group_pk, course_pk):
        """Course Delete"""
        group_course = Course.objects.filter(group_course__group=group_pk, pk=course_pk).exists()
        if group_course:
            course = Course.objects.get(group_course__group=group_pk, pk=course_pk)
            if course:
                course.delete()
                return Response({"message": "{} is deleted successfully".format(course)}, status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Course Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group or course does not match"}, status.HTTP_400_BAD_REQUEST)


class CourseUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class CourseEnrollmentViewset(viewsets.ModelViewSet):
    """Course Engrollment"""
    queryset = CourseStudentEnrollment.objects.all().select_related('course', 'student')
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        """Enrollment List"""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, course_pk):
        """Enrollment Create"""
        # course_instance = get_object_or_404(Course, pk=course_pk)
        enroll_instance = CourseStudentEnrollment.objects.filter(course=course_pk, student=request.user).exists()
        if enroll_instance:
            return Response({"message": "This student already enrolled this course"}, status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                'course': course_pk,
                'student': request.user.pk
            }
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                course = serializer.validated_data['course']
                current_date = datetime.date.today()
                if current_date <= course.course_enroll_end_date:
                    if course.student_count >= course.max_student:
                        return Response({"message": "Student is full"}, status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.save()
                        course.student_count += 1
                        course.save()
                        return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Course is expired'}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, course_pk, student_pk):
        """Enrollment Detail"""
        enroll_ins = CourseStudentEnrollment.objects.filter(
            course=course_pk,
            student=student_pk
        ).exists()

        if enroll_ins:
            enroll = CourseStudentEnrollment.objects.get(
                course=course_pk,
                student=student_pk
            )
            if enroll:
                serializer = self.serializer_class(enroll)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Enrollment is not Found"},
                    status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "Enrollment not found"},
                status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, course_pk, student_pk, *args, **kwargs):
        """Enrollment Update"""
        partial = kwargs.pop('partial', True)
        enroll_ins = CourseStudentEnrollment.objects.filter(
            course=course_pk,
            student=student_pk
        ).exists()

        if enroll_ins:
            enroll = CourseStudentEnrollment.objects.get(
                course=course_pk,
                student=student_pk
            )

            if enroll.student == request.user.is_superuser:
                serializer = self.serializer_class(
                    enroll,
                    data=request.data,
                    partial=partial
                )

                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,
                        status.HTTP_200_OK
                    )
                return Response(
                    serializer.errors,
                    status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"message": "You must be authorized"},
                    status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Enrollment not found"},
                status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, course_pk, enroll_pk):
        """Enrollment Delete"""
        enroll_ins = CourseStudentEnrollment.objects.filter(
            pk=enroll_pk,
            course_id=course_pk
        ).exists()

        if enroll_ins:
            enroll = CourseStudentEnrollment.objects.get(
                pk=enroll_pk,
                course_id=course_pk
            )

            enroll.delete()
            return Response(
                {"message": "Enroll is deleted successfully"},
                status.HTTP_204_NO_CONTENT
            )

        return Response(
            {"message": "Enrollment not found"},
            status.HTTP_404_NOT_FOUND
        )


class CourseNoticeViewset(viewsets.ModelViewSet):
    """Course Notice"""
    queryset = CourseNotice.objects.all()
    serializer_class = CourseNoticeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, course_pk):
        """All Notice"""
        course_notices = CourseNotice.objects.filter(course=course_pk).order_by('-id')
        if course_notices.exists():
            serializer = self.serializer_class(course_notices, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "Course or Notice not found"}, status.HTTP_404_NOT_FOUND)

    def create(self, request, course_pk):
        """Notice Create"""
        course = Course.objects.filter(pk=course_pk).exists()
        if course:
            data = request.data
            data['course'] = course_pk
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Course Not Found"}, status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, course_pk, notice_pk):
        """Detail Notice"""
        course_notice = CourseNotice.objects.filter(course=course_pk, pk=notice_pk).exists()
        if course_notice:
            notice = CourseNotice.objects.get(course=course_pk, pk=notice_pk)
            if notice:
                serializer = self.serializer_class(notice)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({"message": "Notice is not found "}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Course or Notice does not found"}, status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, course_pk, notice_pk, *args, **kwargs):
        """Update Notice"""
        course_notice = CourseNotice.objects.filter(course=course_pk, pk=notice_pk).exists()
        if course_notice:
            partial = kwargs.pop('partial', True)
            notice = CourseNotice.objects.get(course=course_pk, pk=notice_pk)
            if notice:
                serializer = self.serializer_class(notice, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Notice not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Course or Notice does not found"}, status.HTTP_404_NOT_FOUND)

    def destroy(self, request, group_pk, course_pk, notice_pk):
        """Notice Delete"""
        group_course = GroupCourse.objects.filter(course=course_pk, group=group_pk).exists()
        if group_course:
            notice_ins = CourseNotice.objects.filter(pk=notice_pk, course_id=course_pk).exists()
            if notice_ins:
                notice = CourseNotice.objects.get(pk=notice_pk, course_id=course_pk)
                notice.delete()
                return Response({"message": "{} is deleted successfully".format(notice)}, status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Notice Not Found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group does not match"}, status.HTTP_400_BAD_REQUEST)


class CourseClassLinkViewset(viewsets.ModelViewSet):
    queryset = CourseClassLink.objects.all()
    serializer_class = CourseClassLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, course_pk):
        course_instance = CourseClassLink.objects.filter(course=course_pk).exists()
        if not course_instance:
            class_link_data = request.data
            class_link_data['course'] = course_pk
            serializer = self.serializer_class(data=class_link_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Course Already Exists"}, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, course_pk):
        course_instance = CourseClassLink.objects.filter(course=course_pk).exists()
        if course_instance:
            class_link = CourseClassLink.objects.get(course=course_pk)
            serializer = self.serializer_class(class_link)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({"message": "Course Class Link Not Found"}, status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, course_pk, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        course_instance = CourseClassLink.objects.filter(course=course_pk).exists()
        if course_instance:
            class_link = CourseClassLink.objects.get(course=course_pk)
            serializer = self.serializer_class(class_link, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Course Class Link Not Found"}, status.HTTP_404_NOT_FOUND)


class CourseStaffViewset(viewsets.ModelViewSet):
    """Course Trainer"""
    queryset = CourseStaff.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = CourseStaffSerializer

    def create(self, request, group_pk, course_pk):
        """Course Trainer Create"""
        course_instance = Course.objects.filter(group_course__group=group_pk, pk=course_pk)
        if course_instance:
            course = Course.objects.get(group_course__group=group_pk, pk=course_pk)
            if course:
                staff_data = request.data
                group_member = GroupMember.objects.filter(member=staff_data['staff'], group=group_pk).exists()

                if group_member:
                    staff_member = CourseStaff.objects.filter(course=course, staff=staff_data['staff']).exists()
                    if not staff_member:
                        staff_data['course'] = course.pk
                        staff_data['role'] = 'Teacher'
                        serializer = self.serializer_class(data=staff_data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"message": "Staff already Exists"}, status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message": "You are not a group member"}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Course Does Not Found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Course or Group not found"}, status.HTTP_404_NOT_FOUND)

    def list(self, request, group_pk, course_pk):
        """Course Trainer course list"""
        course_instance = Course.objects.filter(group_course__group=group_pk, pk=course_pk)
        if course_instance:
            course = Course.objects.get(group_course__group=group_pk, pk=course_pk)
            if course:
                teacher = CourseStaff.objects.filter(course=course, role="Teacher")
                if teacher.exists():
                    serializer = self.serializer_class(teacher, many=True)
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response({"message": "Teacher not found"}, status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "Course not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Course or Group not found"}, status.HTTP_404_NOT_FOUND)

    def single_staff(self, request, course_pk):
        staff_instance = CourseStaff.objects.filter(course=course_pk, staff=request.user).exists()
        if staff_instance:
            staff = CourseStaff.objects.get(course=course_pk, staff=request.user)
            serializer = self.serializer_class(staff)
            data = serializer.data
            data['enabled'] = staff.enable
            return Response(data, status.HTTP_200_OK)
        else:
            return Response({"message": "Staff not found"}, status.HTTP_404_NOT_FOUND)


class CourseEnrollmentPaymentViewset(viewsets.ModelViewSet):
    """Payment for Course Enrollment"""
    queryset = CourseEnrollmentPayment.objects.select_related('course', 'student')
    serializer_class = CourseEnrollmentPaymentSerializer
    permission_class = [permissions.IsAuthenticated]

    def course_enroll_payment(self, request, course_pk):
        """Make Payment for Course Enrollment. Student must be enrolled for payment."""
        course_instance = Course.objects.filter(pk=course_pk).exists()
        if course_instance:
            course = Course.objects.get(pk=course_pk)
            enroll_instance = CourseStudentEnrollment.objects.filter(course=course, student=request.user).exists()
            if course and not enroll_instance:

                data = request.data
                data['course'] = course.pk
                data['student'] = request.user.pk
                data['amount'] = course.enrollment_fee
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    CourseStudentEnrollment.objects.create(course=course, student=request.user)
                    course.student_count += 1
                    course.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Enrollment already Exists"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Course not found"}, status.HTTP_404_NOT_FOUND)

    def course_enrollment_payment_list(self, request, course_pk):
        """All Payment List for desired course enrollment"""
        enrollments = CourseEnrollmentPayment.objects.filter(course=course_pk)
        if enrollments.exists():
            serializer = self.serializer_class(enrollments, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "Enrollment does not found"}, status.HTTP_404_NOT_FOUND)


class CourseClassRoutineViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CourseClassRouting.objects.all()
    serializer_class = CourseClassRoutineSerializer

    def retreive(self, request, course_pk):
        routine_instance = CourseClassRouting.objects.filter(course=course_pk).exists()
        print("Routine: ", routine_instance)
        if routine_instance:
            routine = CourseClassRouting.objects.get(course=course_pk)
            serializer = CourseClassRoutineSerializer(routine)
            print("Serializer Data: ", serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "Routine Not Found"}, status.HTTP_404_NOT_FOUND)


class CourseClassRoutineView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CourseClassRouting.objects.all()
    serializer_class = CourseClassRoutineSerializer
    lookup_field = 'course_id'


class AllCourseView(generics.ListAPIView):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')

            if len(search):
                queryset = Course.objects.filter(name__icontains=search)
            else:
                queryset = Course.objects.all()
        except:
            queryset = Course.objects.all()

        return queryset


class GroupCourseView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        try:
            search = self.request.query_params.get('search')

            if len(search):
                queryset = Course.objects.filter(name__icontains=search, group_course__group_id=group_id)
            else:
                queryset = Course.objects.filter(group_course__group_id=group_id)
        except:
            queryset = Course.objects.filter(group_course__group_id=group_id)

        return queryset


class CourseStaffView(generics.ListCreateAPIView):
    queryset = CourseStaff.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = CourseStaffSerializer

    def create(self, request, *args, **kwargs):
        try:
            course_instance = GroupCourse.objects.get(group__id=kwargs['group_pk'], course__id=kwargs['course_pk'])
            message = []
            for row in request.data:
                staffs = CourseStaff.objects.create(course=course_instance.course,
                                                    staff=User.objects.get(id=row['staff']), role=row['role'],
                                                    enable=False)

                message.append(staffs)

            return Response({'message': len(message)}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)


class CourseStaffRemoveView(generics.DestroyAPIView):
    queryset = CourseStaff.objects.all()
    permission_class = [permissions.IsAuthenticated]
    serializer_class = CourseStaffSerializer
    lookup_field = 'id'


class CourseTeachersView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]
    queryset = CourseStaff.objects.all()

    def list(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_pk')
        current_course = Course.objects.get(id=course_id)
        current_teachers = CourseStaff.objects.filter(course=current_course, enable=True)
        teachers = []
        for teacher in current_teachers:
            try:
                teachers.append({
                    'id': teacher.staff.id,
                    'staff_id': teacher.id,
                    'first_name': teacher.staff.first_name,
                    'academic_discipline': teacher.staff.academic_discipline,
                    'profession': teacher.staff.profession,
                    'profile_pic': teacher.staff.general_info_user.profile_pic.url
                })
            except:
                teachers.append({
                    'id': teacher.staff.id,
                    'staff_id': teacher.id,
                    'first_name': teacher.staff.first_name,
                    'academic_discipline': teacher.staff.academic_discipline,
                    'profession': teacher.staff.profession
                })
        return Response(teachers)


class TeachersCourseView(generics.ListAPIView):
    """
    List of courses that a teacher is the instructor of
    """
    # queryset = CourseStaff.objects.all()
    serializer_class = TeacherCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CourseStaff.objects.filter(staff=self.request.user)
        return queryset


class TeachersCourseAcceptView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        course_staff_id = self.kwargs.get('course_staff_id')
        current_course_staff = CourseStaff.objects.get(id=course_staff_id)
        current_course_staff.enable = True
        current_course_staff.save()

        return Response({
            'message': 'Created',
        }, status=status.HTTP_201_CREATED)


class StudentCourseView(generics.ListAPIView):
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = CourseStudentEnrollment.objects.filter(student=self.request.user)
        return queryset
