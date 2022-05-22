from django.urls import path
from . import views
from .views import CourseStaffView, AllCourseView, CourseTeachersView, TeachersCourseView, StudentCourseView, \
    TeachersCourseAcceptView, GroupCourseView, CourseClassRoutineView, CourseUpdateDeleteView, CourseStaffRemoveView

app_name = 'course_app'

# Course All Action
course_create = views.CourseVeiwset.as_view({
    'post': 'create'
})

course_list = views.CourseVeiwset.as_view({
    'get': 'list'
})
search_course = views.CourseVeiwset.as_view({
    'get': 'search_course'
})

course_by_group = views.CourseVeiwset.as_view({
    'get': 'all_course_of_group'
})

single_course_by_group = views.CourseVeiwset.as_view({
    'get': 'single_course_by_group',
    'patch': 'partial_update',
    'delete': 'destroy'
})

single_course = views.CourseVeiwset.as_view({
    'get': 'single_course'
})

single_course_update = views.CourseVeiwset.as_view({
    'patch': 'single_course_update'
})
# Course Staff/Trainer Action
trainer_create = views.CourseStaffViewset.as_view({
    'post': 'create'
})
trainer_list = views.CourseStaffViewset.as_view({
    'get': 'list'
})
single_staff = views.CourseStaffViewset.as_view({
    'get': 'single_staff'
})

# Enrollment Action 
enrollment_create = views.CourseEnrollmentViewset.as_view({
    'post': 'create'
})

enrollment_list = views.CourseEnrollmentViewset.as_view({
    'get': 'list'
})

enrollment_detail = views.CourseEnrollmentViewset.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Notice Action
notice_list = views.CourseNoticeViewset.as_view({
    'get': 'list'
})
notice_create = views.CourseNoticeViewset.as_view({
    'post': 'create'
})
notice_detail = views.CourseNoticeViewset.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Course Class Link
course_class_link_create = views.CourseClassLinkViewset.as_view({
    'post': 'create'
})
course_class_link = views.CourseClassLinkViewset.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})

# Course Payment
course_enroll_payment = views.CourseEnrollmentPaymentViewset.as_view({
    'post': 'course_enroll_payment'
})

course_enrollment_payment_list = views.CourseEnrollmentPaymentViewset.as_view({
    'get': 'course_enrollment_payment_list'
})

# Course Class Routine
course_routine_list = views.CourseClassRoutineViewset.as_view({
    'get': 'retreive'
})

urlpatterns = [
    # Course URL
    # Course ALL http://127.0.0.1:8000/course/all/?search=
    path(
        'all/',
        AllCourseView.as_view(),
        name='course-list'
    ),

    # Course ALL http://127.0.0.1:8000/course/1/all/?search=
    path(
        '<int:group_id>/all/',
        GroupCourseView.as_view(),
        name='course-list'
    ),

    # Search Course http://127.0.0.1:8000/course/search-course/
    path(
        'search-course/',
        search_course,
        name='course-search'
    ),

    # Course Create http://127.0.0.1:8000/course/group/1/course-create/
    path(
        'group/<int:group_pk>/course-create/',
        course_create,
        name='course-create'
    ),

    # Course by group http://127.0.0.1:8000/course/group/1/group-courses/
    path(
        'group/<int:group_pk>/group-courses/',
        course_by_group,
        name='course-list'
    ),

    # Single course by group http://127.0.0.1:8000/course/group/1/1/
    path(
        'group/<int:group_pk>/<int:course_pk>/',
        single_course_by_group,
        name='single-course-by-group'
    ),

    # Single course get http://127.0.0.1:8000/course/single-course/1/
    path(
        'single-course/<int:course_pk>/',
        single_course,
        name='single-course'
    ),
    # Single course Update http://127.0.0.1:8000/course/single-course/1/
    path(
        'single-course/update/<int:id>/',
        CourseUpdateDeleteView.as_view(),
        name='single-course-update'
    ),

    # Course Class Link URL
    # Course Class Link create http://127.0.0.1:8000/course/1/1/class-link-create/
    path(
        '<int:course_pk>/class-link-create/',
        course_class_link_create,
        name='course-class-link-create'
    ),

    # Course Class Link Detail http://127.0.0.1:8000/course/1/1/detail/
    path(
        '<int:course_pk>/class-link-detail/',
        course_class_link,
        name='course-class-link'
    ),

    # Course Staff/Trainer URL
    # Create Course Trainer http://127.0.0.1:8000/course/1/1/trainer-create/
    path(
        '<int:group_pk>/<int:course_pk>/trainer-create/',
        CourseStaffView.as_view(),
        name='course-trainer-create'
    ),
    path(
        '<int:id>/trainer-remove/',
        CourseStaffRemoveView.as_view(),
        name='course-trainer-remove'
    ),
    # Course All Trainer http://127.0.0.1:8000/course/1/1/trainers/
    path(
        '<int:group_pk>/<int:course_pk>/trainers/',
        trainer_list,
        name='course-trainer-create'
    ),

    # Single Staff http://127.0.0.1:8000/course/1/staff/single-staff/
    path(
        '<int:course_pk>/staff/single-staff/',
        single_staff,
        name='single-staff'
    ),

    # Enrollment URL
    # All Enrollment http://127.0.0.1:8000/course/enrollment/all/
    path(
        'enrollment/all/',
        StudentCourseView.as_view(),
        name="enrollment-list"
    ),

    # Create Enrollment http://127.0.0.1:8000/course/1/enrollment/create/
    path(
        '<int:course_pk>/enrollment/create/',
        enrollment_create,
        name="enrollment-create"
    ),

    # Single Enrollment http://127.0.0.1:8000/course/1/enrollment/2/
    path(
        '<int:course_pk>/enrollment/<int:student_pk>/',
        enrollment_detail,
        name="enrollment-detail"
    ),

    # Course Payment
    # Make Course Enrollment Payment URL http://127.0.0.1:8000/course/1/enrollment/1/course-enrollment-payment/
    path(
        '<int:course_pk>/enrollment/course-enrollment-payment/',
        course_enroll_payment,
        name='course-enroll-payment'
    ),

    # Course Enrollment Payment List http://127.0.0.1:8000/course/1/enrollment/payment-all/
    path(
        '<int:course_pk>/enrollment/payment-all/',
        course_enrollment_payment_list,
        name="course-enrollment-payment-list"
    ),

    # Notice URL
    # All Notice http://127.0.0.1:8000/course/1/1/notice/all/
    path(
        '<int:course_pk>/notice/all/',
        notice_list,
        name='notice_list'
    ),

    # Create Notice http://127.0.0.1:8000/course/1/1/notice/create/
    path(
        '<int:course_pk>/notice/create/',
        notice_create,
        name='notice_create'
    ),

    # Single Notice http://127.0.0.1:8000/course/1/1/notice/2/
    path(
        '<int:course_pk>/notice/<int:notice_pk>/',
        notice_detail,
        name='notice-detail'
    ),

    # Course Class Routine List http://127.0.0.1:8000/course/1/class-routine/
    path(
        '<int:course_id>/class-routine/',
        CourseClassRoutineView.as_view(),
        name='class-routine'
    ),
    path('<int:course_pk>/teachers/', CourseTeachersView.as_view()),
    path('teachers-courses/', TeachersCourseView.as_view()),
    path('<int:course_staff_id>/teachers-courses-accept/', TeachersCourseAcceptView.as_view()),

]
