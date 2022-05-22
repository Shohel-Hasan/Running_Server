from telnetlib import STATUS
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions, serializers, status, parsers, renderers, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

from user_app.serializers import *
from user_app.serializers import ResetPasswordSerializer, TokenSerializer
from otp import generate_otp
from researchrider import settings
from .models import *
from .serializers import UserSerializer
from django.db import transaction
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework.viewsets import ViewSet


class UserRegisterView(APIView):
    # activation_email_template = "account_activation_email.html"

    @transaction.atomic
    def post(self, request):
        email = request.data.get('email', None).lower()
        password = request.data.get('password', None)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        birthdate = request.data.get('birthdate', None)
        gender = request.data.get('gender', None)
        academic_discipline = request.data.get('academic_discipline', None)
        profession = request.data.get('profession', None)
        verification_code = generate_otp()

        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "gender": gender,
            "academic_discipline": academic_discipline,
            "profession": profession,
            "verification_code": verification_code,
        }
        serializer = UserSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()

            UserGeneralInfo.objects.create(user=user)
            UserContactInformation.objects.create(user=user)
            # ResearchSkill.objects.create(user=user)
            # ResearchArticle.objects.create(user=user)
            # ResearchWork.objects.create(user=user)
            # ResearchSummary.objects.create(user=user)
            # ResearchThoughts.objects.create(user=user)
            # UserOtherInfo.objects.create(user=user)
            # WorkingHistory.objects.create(user=user)
            # UserSkill.objects.create(user=user)
            # UserAcademicDiscipline.objects.create(user=user)
            # UserAcademicDegree.objects.create(user=user)
            # UserTraining.objects.create(user=user)
            # UserWorkShopSeminar.objects.create(user=user)

            # Here need to update don't delete those line
            # email_res = User.send_signup_mail(email, self.activation_email_template)

            # message = f'your verification code is : {verification_code}'
            # subject = 'Student Enroll Mail'
            # to = email
            #
            # email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to])
            # email.content_subtype = 'html'
            # email.send()

            email_body = f"""
               <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                <div style="width:100%;padding:20px 0">
                    <div style="border-bottom:1px solid #eee">
                    <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Research Rider</a>
                    </div>
                    <p style="font-size:1.1em">Hi,</p>
                    <p>Thank you for signing up. Use the following OTP to complete your Sign Up procedures</p>
                    <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{verification_code}</h2>
                    <p style="font-size:0.9em;">Regards,<br />Research Rider Support</p>
                    <hr style="border:none;border-top:1px solid #eee" />
                    <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                    
                    </div>
                </div>
                </div>
            """

            email = EmailMessage(
                'OTP Confirmation',
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
            )

            email.content_subtype = 'html'
            email.send(fail_silently=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOTPVerifyView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = OTPSerializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data.get('token')

            try:
                token = AppToken.objects.get(token=otp)
                user = User.objects.get(tokens__token__contains=token.token)
                user.is_active = True
                user.save()
                token.delete()

                return Response({"success": True}, status=status.HTTP_200_OK)
            except (User.DoesNotExist, AppToken.DoesNotExist):
                return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ObtainAuthToken(APIView):
    serializer_class = UserSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request):
        # email = request.data.get('email')
        data = {
            "username": request.data.get('email', None),
            "password": request.data.get('password', None),
        }
        print(data)
        authentication = authenticate(request, username=data['username'], password=data['password'])
        if authentication:
            user = User.objects.filter(email=data['username']).first()
            if user is None:
                return Response({"error": "user not found.", "logged_in": False}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"logged_in": True, "data": user.as_json()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "user not found or wrong password ."}, status=status.HTTP_400_BAD_REQUEST)


class TokenCheck(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request, format=None):
        token = request.data.get('token')
        token_ins = Token.objects.filter(key=token).exists()
        print("token_ins: ", token_ins)
        if token_ins:
            serializer = TokenSerializer(token_ins)
            return Response({"message": True}, status=status.HTTP_200_OK)
        else:
            return Response({"message:": False}, status=status.HTTP_404_NOT_FOUND)


class ForgetPasswordView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_user_obj(self, email):
        try:
            user = User.objects.get(username=email)
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        email = request.data.get("email", None)
        print("email: ", email)
        if email is None:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user_instances = User.objects.filter(email=email).exists()
        print("user_instances", user_instances)
        if user_instances:

            user_ins = User.objects.filter(email=email).get()
            verification_code = user_ins.verification_code
            print(verification_code)

            user = self.get_user_obj(email)
            serializer = ForgotPasswordTokenSerializer(user, data={}, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Here need to update don't delete those line
                # email_res = User.send_signup_mail(email, self.activation_email_template)
                message = f'your verification code is : {verification_code}'
                subject = 'password change'
                to = email

                email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to])
                email.content_subtype = 'html'
                email.send()

                # sending Mail
                # subject = 'research rider: Reset Password.'
                # email_body = "<strong> Hello ! </strong> " \
                #              "<p>You’ve requested to reset your password. Use This code for reset your password." \
                #              "</p> CODE:   <strong>" + str(serializer.data['security_code']) + "</strong><p> Thank you </p>"
                # mailer = Mailer()
                # response = mailer.send_email(recipient=email, subject=subject, html_message=email_body)
                #
                # if not response:
                #     return Response({'error': 'Email sending process failed. Please try again'},
                #                     status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": False}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, format=None):
        email = request.data.get("email", None)
        verification_code = request.data.get("verification_code", None)
        print(verification_code)

        user_ins = User.objects.filter(email=email, verification_code=verification_code).exists()
        if user_ins:
            serializer = self.serializer_class(data=request.data, partial=False)
            if serializer.is_valid():
                return Response({"message": True}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"message: ": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": False}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, format=None):

        req_user = request.user
        password = request.data.get('new_password')
        print("sdf", req_user, password)
        if not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        trim_pass = password.strip()
        print(trim_pass)
        if trim_pass == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        req_user.set_password(raw_password=trim_pass)
        req_user.save()

        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Signout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class SingleUserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, user_id, format=None):

        user_ins = User.objects.filter(id=user_id).first()
        if user_ins:
            serializer = UserSerializer(user_ins)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# get all student data
class AllUsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_queryset(self):
        users_ins = User.objects.all()
        return users_ins

    def get_serializer_context(self):
        return {'request': self.request}


# User General Info create view
class UserGeneralInfoCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        height_feet = request.data.get('height_feet', None)
        height_inch = request.data.get('height_inch', None)
        weight_kg = request.data.get('weight_kg', None)
        weight_gm = request.data.get('weight_gm', None)
        blood_group = request.data.get('blood_group', None)
        nationality = request.data.get('nationality', None)
        nid_number = request.data.get('nid_number', None)
        fathers_name = request.data.get('fathers_name', None)
        mothers_name = request.data.get('mothers_name', None)
        religion = request.data.get('religion', None)
        martial_status = request.data.get('martial_status', None)
        native_language = request.data.get('native_language', None)
        data = {
            "user": user,
            "height_feet": height_feet,
            "height_inch": height_inch,
            "weight_kg": weight_kg,
            "weight_gm": weight_gm,
            "blood_group": blood_group,
            "nationality": nationality,
            "martial_status": martial_status,
            "nid_number": nid_number,
            "fathers_name": fathers_name,
            "mothers_name": mothers_name,
            "religion": religion,
            "native_language": native_language
        }

        serializer = UserGeneralInfoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"success": "user General info inserted."}, status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserGeneralInfoGetView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserGeneralInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id == self.request.user.id:
            general_info = UserGeneralInfo.objects.filter(user_id=user_id)
        else:
            general_info = UserGeneralInfo.objects.filter(user_id=user_id, is_public=True)
        return general_info


class UserGeneralInfoUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserGeneralInfoSerializer
    queryset = UserGeneralInfo.objects.all()

    def patch(self, request, user_id, format=None):
        general_info_ins = UserGeneralInfo.objects.filter(user_id=user_id).first()
        if general_info_ins:
            serializer = UserGeneralInfoSerializer(general_info_ins, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGeneralInfoViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserGeneralInfo.objects.all()
    serializer_class = UserGeneralInfoSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_info = UserGeneralInfo.objects.get(id=self.kwargs.get('id'))
            if current_info.user == self.request.user:
                current_info.is_public = not current_info.is_public
                current_info.save()
                if current_info.profile_pic and current_info.cover_pic:
                    data = {
                        "id": current_info.id,
                        "created_date": current_info.created_date,
                        "modified_date": current_info.modified_date,
                        "enable": current_info.enable,
                        "profile_pic": current_info.profile_pic.url,
                        "cover_pic": current_info.cover_pic.url,
                        "height_feet": current_info.height_feet,
                        "height_inch": current_info.height_inch,
                        "weight_kg": current_info.weight_kg,
                        "weight_gm": current_info.weight_gm,
                        "blood_group": current_info.blood_group,
                        "marital_status": current_info.marital_status,
                        "nationality": current_info.nationality,
                        "nid_number": current_info.nid_number,
                        "fathers_name": current_info.fathers_name,
                        "mothers_name": current_info.mothers_name,
                        "religion": current_info.religion,
                        "native_language": current_info.native_language,
                        "is_public": current_info.is_public,
                        "user": current_info.user.id
                    }
                else:
                    data = {
                        "id": current_info.id,
                        "created_date": current_info.created_date,
                        "modified_date": current_info.modified_date,
                        "enable": current_info.enable,
                        "height_feet": current_info.height_feet,
                        "height_inch": current_info.height_inch,
                        "weight_kg": current_info.weight_kg,
                        "weight_gm": current_info.weight_gm,
                        "blood_group": current_info.blood_group,
                        "marital_status": current_info.marital_status,
                        "nationality": current_info.nationality,
                        "nid_number": current_info.nid_number,
                        "fathers_name": current_info.fathers_name,
                        "mothers_name": current_info.mothers_name,
                        "religion": current_info.religion,
                        "native_language": current_info.native_language,
                        "is_public": current_info.is_public,
                        "user": current_info.user.id
                    }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserNameUpdateView(generics.UpdateAPIView):
    serializer_class = UserNameUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if User.objects.get(id=self.kwargs.get('id')) == self.request.user:
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


# User General Info create view
class UserContactInfoCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        current_location = request.data.get('current_location', None)
        present_address = request.data.get('present_address')
        permanent_address = request.data.get('permanent_address')

        # some issue
        email_address = request.data.get('email_address', None)
        phone_number = request.data.get('phone_number', None)
        data = {
            "user": user,
            "current_location": current_location,
            "present_address": present_address,
            "permanent_address": permanent_address,
            "email_address": email_address,
            "phone_number": phone_number,
        }

        serializer = UserContactInfoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "user Contact info inserted."}, status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserContactInfoGetView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserContactInfoSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id == self.request.user.id:
            contact_info = UserContactInformation.objects.filter(user_id=user_id)
        else:
            contact_info = UserContactInformation.objects.filter(user_id=user_id, is_public=True)
        return contact_info


class UserContactInfoUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserContactInfoSerializer
    queryset = UserContactInformation.objects.all()

    def patch(self, request, user_id, format=None):
        general_info_ins = UserContactInformation.objects.filter(user_id=user_id).first()
        if general_info_ins:
            serializer = UserContactInfoSerializer(general_info_ins, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserContactInfoViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserContactInformation.objects.all()
    serializer_class = UserContactInfoSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_info = UserContactInformation.objects.get(id=self.kwargs.get('id'))

            if current_info.user == self.request.user:
                current_info.is_public = not current_info.is_public
                current_info.save()
                data = {
                    "id": current_info.id,
                    "created_date": current_info.created_date,
                    "modified_date": current_info.modified_date,
                    "enable": current_info.enable,
                    "city": current_info.city,
                    "country": current_info.country,
                    "present_address": current_info.present_address,
                    "permanent_address": current_info.permanent_address,
                    "email_address": current_info.email_address,
                    "phone_number": current_info.phone_number,
                    "is_public": current_info.is_public,
                    "user": current_info.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User Language Proficiency create view
class UserLanguageProficiencyCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        language_name = request.data.get('language_name', None)
        listening = request.data.get('listening')
        speaking = request.data.get('speaking')
        reading = request.data.get('reading', None)
        writing = request.data.get('writing', None)
        # need to do something when score is true
        # ielts_toefl_score = request.data.get('ielts_toefl_score', None)
        data = {
            "user": user,
            "language_name": language_name,
            "listening": listening,
            "speaking": speaking,
            "reading": reading,
            "writing": writing,
            # "ielts_toefl_score": ielts_toefl_score,
        }

        serializer = UserLanguageProficiencySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "user Language proficiency data inserted."}, status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserLanguageProficiencyDeleteView(ViewSet):
    def destroy(self, request, user_id, language_proficiency_id):

        language_proficiency_ins = UserLanguageProficiency.objects.filter(id=language_proficiency_id,
                                                                          user_id=user_id).exists()
        if language_proficiency_ins:

            UserLanguageProficiency.objects.filter(id=language_proficiency_id, user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserLanguageProficiencyViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserLanguageProficiency.objects.all()
    serializer_class = UserLanguageProficiencySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_language = UserLanguageProficiency.objects.get(id=self.kwargs.get('id'))

            if current_language.user == self.request.user:
                current_language.is_public = not current_language.is_public
                current_language.save()
                data = {
                    "id": current_language.id,
                    "created_date": current_language.created_date,
                    "modified_date": current_language.modified_date,
                    "enable": current_language.enable,
                    "language_name": current_language.language_name,
                    "listening": current_language.listening,
                    "speaking": current_language.speaking,
                    "reading": current_language.reading,
                    "writing": current_language.writing,
                    "is_public": current_language.is_public,
                    "user": current_language.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserLanguageProficiencyGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLanguageProficiencySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            language_proficiency_instances = UserLanguageProficiency.objects.filter(user_id=user_id)
        else:
            language_proficiency_instances = UserLanguageProficiency.objects.filter(user_id=user_id, is_public=True)
        return language_proficiency_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserLanguageProficiencyUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLanguageProficiencySerializer
    queryset = UserLanguageProficiency.objects.all()

    def patch(self, request, user_id, contact_id, format=None):
        language_proficiency_info_ins = UserLanguageProficiency.objects.filter(user_id=user_id, id=contact_id).first()
        if language_proficiency_info_ins:
            serializer = UserLanguageProficiencySerializer(language_proficiency_info_ins, data=request.data,
                                                           partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


# User Language Proficiency create view
class UserLanguageScoreCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        print(user)
        name = request.data.get('name', None)
        ielts_toefl_score = request.data.get('ielts_toefl_score', None)
        data = {
            "user": user,
            "name": name,
            "ielts_toefl_score": ielts_toefl_score,
        }

        serializer = UserIeltsToeflScoreSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "user Language score data inserted."}, status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserLanguageScoreViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = IeltsToeflScore.objects.all()
    serializer_class = UserIeltsToeflScoreSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_score = IeltsToeflScore.objects.get(id=self.kwargs.get('id'))

            if current_score.user == self.request.user:
                current_score.is_public = not current_score.is_public
                current_score.save()
                data = {
                    "id": current_score.id,
                    "created_date": current_score.created_date,
                    "modified_date": current_score.modified_date,
                    "enable": current_score.enable,
                    "name": current_score.name,
                    "ielts_toefl_score": current_score.ielts_toefl_score,
                    "is_public": current_score.is_public,
                    "user": current_score.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserLanguageScoreGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserIeltsToeflScoreSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            language_score_ins = IeltsToeflScore.objects.filter(user_id=user_id)
        else:
            language_score_ins = IeltsToeflScore.objects.filter(user_id=user_id, is_public=True)
        return language_score_ins

    def get_serializer_context(self):
        return {'request': self.request}


class UserLanguageScoreUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserIeltsToeflScoreSerializer
    queryset = IeltsToeflScore.objects.all()

    def patch(self, request, user_id, score_id, format=None):
        language_score_ins = IeltsToeflScore.objects.filter(user_id=user_id, id=score_id).first()
        if language_score_ins:
            serializer = UserIeltsToeflScoreSerializer(language_score_ins, data=request.data,
                                                       partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserLanguageScoreDeleteView(ViewSet):
    def destroy(self, request, user_id, score_id):

        language_score_ins = IeltsToeflScore.objects.filter(id=score_id,
                                                            user_id=user_id).exists()
        if language_score_ins:

            IeltsToeflScore.objects.filter(id=score_id,
                                           user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


# User Research Skill create view
class UserResearchSkillCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        area_of_research_interest = request.data.get('area_of_research_interest', None)
        key_research_skill = request.data.get('key_research_skill', None)
        data = {
            "user": user,
            "area_of_research_interest": area_of_research_interest,
            "key_research_skill": key_research_skill,
        }

        serializer = ResearchSkillSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Data": serializer.data, "success": "user research skill inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserResearchSkillGetView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchSkillSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            user_research_skill_ins = ResearchSkill.objects.filter(user_id=user_id)
        else:
            user_research_skill_ins = ResearchSkill.objects.filter(user_id=user_id, is_public=True)

        return user_research_skill_ins


class UserResearchSkillUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchSkillSerializer
    queryset = ResearchSkill.objects.all()

    def patch(self, request, user_id, format=None):
        research_skill_ins = ResearchSkill.objects.filter(user_id=user_id).first()
        if research_skill_ins:
            serializer = ResearchSkillSerializer(research_skill_ins, data=request.data,
                                                 partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchSkillDeleteView(ViewSet):
    def destroy(self, request, user_id, score_id):

        research_skills_ins = ResearchSkill.objects.filter(id=score_id,
                                                           user_id=user_id).exists()
        if research_skills_ins:

            ResearchSkill.objects.filter(id=score_id,
                                         user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchSkillViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchSkill.objects.all()
    serializer_class = ResearchSkillSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_research = ResearchSkill.objects.get(id=self.kwargs.get('id'))

            if current_research.user == self.request.user:
                current_research.is_public = not current_research.is_public
                current_research.save()
                data = {
                    "id": current_research.id,
                    "created_date": current_research.created_date,
                    "modified_date": current_research.modified_date,
                    "enable": current_research.enable,
                    "area_of_research_interest": current_research.area_of_research_interest,
                    "key_research_skill": current_research.key_research_skill,
                    "is_public": current_research.is_public,
                    "user": current_research.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserResearchArticleCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        article_name = request.data.get('article_name', None)
        authors_name = request.data.get('authors_name')
        journals_name = request.data.get('journals_name')
        publisher_name = request.data.get('publisher_name', None)
        publication_year = request.data.get('publication_year', None)
        url_link = request.data.get('url_link', None)
        has_link = request.data.get('has_link', None)

        # need to do something when link is true

        data = {
            "user": user,
            "article_name": article_name,
            "authors_name": authors_name,
            "journals_name": journals_name,
            "publisher_name": publisher_name,
            "publication_year": publication_year,
            "url_link": url_link,
            "has_link": has_link
        }

        serializer = ResearchArticleSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user research article data inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserResearchArticleGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchArticleSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_article_instances = ResearchArticle.objects.filter(user_id=user_id)
        else:
            research_article_instances = ResearchArticle.objects.filter(user_id=user_id, is_public=True)
        return research_article_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserResearchArticleUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchArticleSerializer
    queryset = ResearchArticle.objects.all()

    def patch(self, request, user_id, article_id, format=None):
        research_article_ins = ResearchArticle.objects.filter(user_id=user_id, id=article_id).first()
        if research_article_ins:
            serializer = ResearchArticleSerializer(research_article_ins, data=request.data,
                                                   partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchArticleDeleteView(ViewSet):
    def destroy(self, request, user_id, article_id):

        research_article_ins = ResearchArticle.objects.filter(id=article_id,
                                                              user_id=user_id).exists()
        if research_article_ins:

            ResearchArticle.objects.filter(id=article_id,
                                           user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchArticleViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchArticle.objects.all()
    serializer_class = ResearchArticleSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_article = ResearchArticle.objects.get(id=self.kwargs.get('id'))

            if current_article.user == self.request.user:
                current_article.is_public = not current_article.is_public
                current_article.save()
                data = {
                    "id": current_article.id,
                    "created_date": current_article.created_date,
                    "modified_date": current_article.modified_date,
                    "enable": current_article.enable,
                    "article_name": current_article.article_name,
                    "authors_name": current_article.authors_name,
                    "journals_name": current_article.journals_name,
                    "publisher_name": current_article.publisher_name,
                    "publication_year": current_article.publication_year,
                    "has_link": current_article.has_link,
                    "url_link": current_article.url_link,
                    "is_public": current_article.is_public,
                    "user": current_article.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserResearchWorkCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        involvement_research_work_info = request.data.get('involvement_research_work_info', None)
        institution = request.data.get('institution')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date', None)

        # need to do something when link is true
        is_present = request.data.get('is_present', None)

        data = {
            "user": user,
            "involvement_research_work_info": involvement_research_work_info,
            "institution": institution,
            "start_date": start_date,
            "end_date": end_date,
            "is_present": is_present,
        }

        serializer = ResearchWorkSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user research work data inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserResearchWorkGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchWorkSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_work_instances = ResearchWork.objects.filter(user_id=user_id)
        else:
            research_work_instances = ResearchWork.objects.filter(user_id=user_id, is_public=True)
        return research_work_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserResearchWorkUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchWorkSerializer
    queryset = ResearchWork.objects.all()

    def patch(self, request, user_id, work_id, format=None):
        research_work_ins = ResearchWork.objects.filter(user_id=user_id, id=work_id).first()
        if research_work_ins:
            serializer = ResearchWorkSerializer(research_work_ins, data=request.data,
                                                partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchWorkDeleteView(ViewSet):
    def destroy(self, request, user_id, work_id):

        research_work_ins = ResearchWork.objects.filter(id=work_id,
                                                        user_id=user_id).exists()
        if research_work_ins:

            ResearchWork.objects.filter(id=work_id,
                                        user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchWorkViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchWork.objects.all()
    serializer_class = ResearchWorkSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_work = ResearchWork.objects.get(id=self.kwargs.get('id'))

            if current_work.user == self.request.user:
                current_work.is_public = not current_work.is_public
                current_work.save()
                data = {
                    "id": current_work.id,
                    "created_date": current_work.created_date,
                    "modified_date": current_work.modified_date,
                    "enable": current_work.enable,
                    "involvement_research_work_info": current_work.involvement_research_work_info,
                    "institution": current_work.institution,
                    "start_date": current_work.start_date,
                    "end_date": current_work.end_date,
                    "is_present": current_work.is_present,
                    "is_public": current_work.is_public,
                    "user": current_work.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserResearchSummaryCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        url_link = request.data.get('url_link', None)
        data = {
            "user": user,
            "url_link": url_link,
        }

        serializer = ResearchSummarySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user research summary link inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserResearchSummaryGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchSummarySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_summary_instances = ResearchSummary.objects.filter(user_id=user_id)
        else:
            research_summary_instances = ResearchSummary.objects.filter(user_id=user_id, is_public=True)
        return research_summary_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserResearchSummaryUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchSummarySerializer
    queryset = ResearchSummary.objects.all()

    def patch(self, request, user_id, summary_id, format=None):
        research_summary_ins = ResearchSummary.objects.filter(user_id=user_id, id=summary_id).first()
        if research_summary_ins:
            serializer = ResearchSummarySerializer(research_summary_ins, data=request.data,
                                                   partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchSummaryDeleteView(ViewSet):
    def destroy(self, request, user_id, summary_id):

        research_summary_ins = ResearchSummary.objects.filter(id=summary_id,
                                                              user_id=user_id).exists()
        if research_summary_ins:

            ResearchSummary.objects.filter(id=summary_id,
                                           user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchSummaryViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchSummary.objects.all()
    serializer_class = ResearchSummarySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_summary = ResearchSummary.objects.get(id=self.kwargs.get('id'))

            if current_summary.user == self.request.user:
                current_summary.is_public = not current_summary.is_public
                current_summary.save()
                data = {
                    "id": current_summary.id,
                    "created_date": current_summary.created_date,
                    "modified_date": current_summary.modified_date,
                    "enable": current_summary.enable,
                    "url_link": current_summary.url_link,
                    "is_public": current_summary.is_public,
                    "user": current_summary.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserResearchThoughtCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        url_link = request.data.get('url_link', None)
        data = {
            "user": user,
            "url_link": url_link,
        }

        serializer = ResearchThoughtsSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user research thoughts link inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserResearchThoughtGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchThoughtsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = ResearchThoughts.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = ResearchThoughts.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserResearchThoughtsUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResearchThoughtsSerializer
    queryset = ResearchThoughts.objects.all()

    def patch(self, request, user_id, thoughts_id, format=None):
        research_thoughts_ins = ResearchThoughts.objects.filter(user_id=user_id, id=thoughts_id).first()
        if research_thoughts_ins:
            serializer = ResearchThoughtsSerializer(research_thoughts_ins, data=request.data,
                                                    partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchThoughtsDeleteView(ViewSet):
    def destroy(self, request, user_id, thoughts_id):

        research_thoughts_ins = ResearchThoughts.objects.filter(id=thoughts_id,
                                                                user_id=user_id).exists()
        if research_thoughts_ins:

            ResearchThoughts.objects.filter(id=thoughts_id,
                                            user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserResearchThoughtsViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ResearchThoughts.objects.all()
    serializer_class = ResearchThoughtsSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_thought = ResearchThoughts.objects.get(id=self.kwargs.get('id'))

            if current_thought.user == self.request.user:
                current_thought.is_public = not current_thought.is_public
                current_thought.save()
                data = {
                    "id": current_thought.id,
                    "created_date": current_thought.created_date,
                    "modified_date": current_thought.modified_date,
                    "enable": current_thought.enable,
                    "url_link": current_thought.url_link,
                    "is_public": current_thought.is_public,
                    "user": current_thought.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User Research Skill create view
class UserOtherInfoCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        key_working_skill = request.data.get('key_working_skill', None)
        career_objective_plan = request.data.get('career_objective_plan', None)
        area_of_working_interest = request.data.get('area_of_working_interest', None)
        data = {
            "user": user,
            "key_working_skill": key_working_skill,
            "career_objective_plan": career_objective_plan,
            "area_of_working_interest": area_of_working_interest,
        }

        serializer = UserOtherInfoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"Data": serializer.data, "success": "user other info inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserOtherInfoGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserOtherInfoSerializer

    def retrieve(self, request, user_id, format=None):

        user_research_skill_ins = UserOtherInfo.objects.filter(user_id=user_id).first()
        if user_research_skill_ins:
            serializer = UserOtherInfoSerializer(user_research_skill_ins)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserOtherInfoUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserOtherInfoSerializer
    queryset = UserOtherInfo.objects.all()

    def patch(self, request, user_id, format=None):
        other_info_ins = UserOtherInfo.objects.filter(user_id=user_id).first()
        if other_info_ins:
            serializer = UserOtherInfoSerializer(other_info_ins, data=request.data,
                                                 partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


# User Research Skill create view
class UserSkillCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        technology_skill = request.data.get('technology_skill', None)
        other_notable_skill = request.data.get('other_notable_skill', None)
        data = {
            "user": user,
            "technology_skill": technology_skill,
            "other_notable_skill": other_notable_skill,
        }

        serializer = UserSkillSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"Data": serializer.data, "success": "user skill inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserSkillGetView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSkillSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            user_research_skill_ins = UserSkill.objects.filter(user_id=user_id)
        else:
            user_research_skill_ins = UserSkill.objects.filter(user_id=user_id, is_public=True)
        return user_research_skill_ins


class UserSkillUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSkillSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = UserSkill.objects.all()

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if UserSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Something Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if UserSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class UserSkillViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_skill = UserSkill.objects.get(id=self.kwargs.get('id'))

            if current_skill.user == self.request.user:
                current_skill.is_public = not current_skill.is_public
                current_skill.save()
                data = {
                    "id": current_skill.id,
                    "created_date": current_skill.created_date,
                    "modified_date": current_skill.modified_date,
                    "enable": current_skill.enable,
                    "technology_skill": current_skill.technology_skill,
                    "other_notable_skill": current_skill.other_notable_skill,
                    "is_public": current_skill.is_public,
                    "user": current_skill.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# This Class May be deleted
class UserSkillUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSkillSerializer
    queryset = UserSkill.objects.all()

    def patch(self, request, user_id, format=None):
        user_skill_info_ins = UserSkill.objects.filter(user_id=user_id).first()
        if user_skill_info_ins:
            serializer = UserSkillSerializer(user_skill_info_ins, data=request.data,
                                             partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


# User General Info create view
class UserWorkingHistoryCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        designation = request.data.get('designation', None)
        department = request.data.get('department', None)
        institute = request.data.get('institute', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        data = {
            "user": user,
            "designation": designation,
            "department": department,
            "institute": institute,
            "start_date": start_date,
            "end_date": end_date,
        }

        serializer = WorkingHistorySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user working history inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserWorkingHistoryGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkingHistorySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = WorkingHistory.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = WorkingHistory.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserWorkingHistoryUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkingHistorySerializer
    queryset = WorkingHistory.objects.all()

    def patch(self, request, user_id, work_history_id, format=None):
        working_history_ins = WorkingHistory.objects.filter(user_id=user_id, id=work_history_id).first()
        if working_history_ins:
            serializer = WorkingHistorySerializer(working_history_ins, data=request.data,
                                                  partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserWorkingHistoryDeleteView(ViewSet):
    def destroy(self, request, user_id, work_history_id):

        working_history_ins = WorkingHistory.objects.filter(id=work_history_id,
                                                            user_id=user_id).exists()
        if working_history_ins:

            WorkingHistory.objects.filter(id=work_history_id,
                                          user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserWorkingHistoryViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WorkingHistory.objects.all()
    serializer_class = WorkingHistorySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_history = WorkingHistory.objects.get(id=self.kwargs.get('id'))

            if current_history.user == self.request.user:
                current_history.is_public = not current_history.is_public
                current_history.save()
                data = {
                    "id": current_history.id,
                    "created_date": current_history.created_date,
                    "modified_date": current_history.modified_date,
                    "enable": current_history.enable,
                    "designation": current_history.designation,
                    "department": current_history.department,
                    "institute": current_history.institute,
                    "start_date": current_history.start_date,
                    "end_date": current_history.end_date,
                    "is_present": current_history.is_present,
                    "is_public": current_history.is_public,
                    "user": current_history.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserAcademicDisciplineCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        academic_discipline = request.data.get('academic_discipline', None)
        data = {
            "user": user,
            "academic_discipline": academic_discipline,
        }

        serializer = UserAcademicDisciplineSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user academic discipline inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserAcademicDisciplineGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAcademicDisciplineSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = UserAcademicDiscipline.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = UserAcademicDiscipline.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserAcademicDisciplineUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAcademicDisciplineSerializer
    queryset = UserAcademicDiscipline.objects.all()

    def patch(self, request, user_id, academic_discipline_id, format=None):
        academic_discipline_ins = UserAcademicDiscipline.objects.filter(user_id=user_id,
                                                                        id=academic_discipline_id).first()
        if academic_discipline_ins:
            serializer = UserAcademicDisciplineSerializer(academic_discipline_ins, data=request.data,
                                                          partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserAcademicDisciplineDeleteView(ViewSet):
    def destroy(self, request, user_id, academic_discipline_id):

        academic_discipline_ins = UserAcademicDiscipline.objects.filter(id=academic_discipline_id,
                                                                        user_id=user_id).exists()
        if academic_discipline_ins:

            UserAcademicDiscipline.objects.filter(id=academic_discipline_id,
                                                  user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserAcademicDisciplineViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserAcademicDiscipline.objects.all()
    serializer_class = UserAcademicDisciplineSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_discipline = UserAcademicDiscipline.objects.get(id=self.kwargs.get('id'))

            if current_discipline.user == self.request.user:
                current_discipline.is_public = not current_discipline.is_public
                current_discipline.save()
                data = {
                    "id": current_discipline.id,
                    "created_date": current_discipline.created_date,
                    "modified_date": current_discipline.modified_date,
                    "enable": current_discipline.enable,
                    "academic_discipline": current_discipline.academic_discipline,
                    "is_public": current_discipline.is_public,
                    "user": current_discipline.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserAcademicDegreeCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        degree = request.data.get('degree', None)
        department = request.data.get('department', None)
        institutions = request.data.get('institutions', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        data = {
            "user": user,
            "degree": degree,
            "department": department,
            "institutions": institutions,
            "start_date": start_date,
            "end_date": end_date,
        }

        serializer = UserAcademicDegreeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user academic degree inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserAcademicDegreeGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAcademicDegreeSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = UserAcademicDegree.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = UserAcademicDegree.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserAcademicDegreeUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAcademicDegreeSerializer
    queryset = UserAcademicDegree.objects.all()

    def patch(self, request, user_id, academic_degree_id, format=None):
        academic_degree_ins = UserAcademicDegree.objects.filter(user_id=user_id,
                                                                id=academic_degree_id).first()
        if academic_degree_ins:
            serializer = UserAcademicDegreeSerializer(academic_degree_ins, data=request.data,
                                                      partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserAcademicDegreeDeleteView(ViewSet):
    def destroy(self, request, user_id, academic_degree_id):

        academic_degree_ins = UserAcademicDegree.objects.filter(id=academic_degree_id,
                                                                user_id=user_id).exists()
        if academic_degree_ins:

            UserAcademicDegree.objects.filter(id=academic_degree_id,
                                              user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserAcademicDegreeViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserAcademicDegree.objects.all()
    serializer_class = UserAcademicDegreeSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_degree = UserAcademicDegree.objects.get(id=self.kwargs.get('id'))

            if current_degree.user == self.request.user:
                current_degree.is_public = not current_degree.is_public
                current_degree.save()
                data = {
                    "id": current_degree.id,
                    "created_date": current_degree.created_date,
                    "modified_date": current_degree.modified_date,
                    "enable": current_degree.enable,
                    "degree": current_degree.degree,
                    "department": current_degree.department,
                    "institutions": current_degree.institutions,
                    "start_date": current_degree.start_date,
                    "end_date": current_degree.end_date,
                    "is_public": current_degree.is_public,
                    "user": current_degree.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserTrainingCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        training_name = request.data.get('training_name', None)
        institutions = request.data.get('institutions', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        # is true need to update later.
        is_present = request.data.get('is_present', None)
        data = {
            "user": user,
            "training_name": training_name,
            "institutions": institutions,
            "start_date": start_date,
            "end_date": end_date,
            "is_present": is_present,
        }

        serializer = UserTrainingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user academic discipline inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserTrainingGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserTrainingSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = UserTraining.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = UserTraining.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserTrainingUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserTrainingSerializer
    queryset = UserTraining.objects.all()

    def patch(self, request, user_id, training_id, format=None):
        training_ins = UserTraining.objects.filter(user_id=user_id,
                                                   id=training_id).first()
        if training_ins:
            serializer = UserTrainingSerializer(training_ins, data=request.data,
                                                partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserTrainingDeleteView(ViewSet):
    def destroy(self, request, user_id, training_id):

        user_training_ins = UserTraining.objects.filter(id=training_id,
                                                        user_id=user_id).exists()
        if user_training_ins:

            UserTraining.objects.filter(id=training_id,
                                        user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserTrainingViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserTraining.objects.all()
    serializer_class = UserTrainingSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_training = UserTraining.objects.get(id=self.kwargs.get('id'))

            if current_training.user == self.request.user:
                current_training.is_public = not current_training.is_public
                current_training.save()
                data = {
                    "id": current_training.id,
                    "created_date": current_training.created_date,
                    "modified_date": current_training.modified_date,
                    "enable": current_training.enable,
                    "training_name": current_training.training_name,
                    "institutions": current_training.institutions,
                    "start_date": current_training.start_date,
                    "end_date": current_training.end_date,
                    "is_present": current_training.is_present,
                    "is_public": current_training.is_public,
                    "user": current_training.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


# User General Info create view
class UserWorkshopSeminarCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        user = request.user.id
        workshop_or_seminar_name = request.data.get('workshop_or_seminar_name', None)
        institutions = request.data.get('institutions', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        data = {
            "user": user,
            "workshop_or_seminar_name": workshop_or_seminar_name,
            "institutions": institutions,
            "start_date": start_date,
            "end_date": end_date,
        }

        serializer = UserWorkShopSeminarSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response({"data": serializer.data, "success": "user academic discipline inserted."},
                            status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class UserWorkshopSeminarGetView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserWorkShopSeminarSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user.id:
            research_thoughts_instances = UserWorkShopSeminar.objects.filter(user_id=user_id)
        else:
            research_thoughts_instances = UserWorkShopSeminar.objects.filter(user_id=user_id, is_public=True)
        return research_thoughts_instances

    def get_serializer_context(self):
        return {'request': self.request}


class UserWorkshopOrSeminarUpdateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserWorkShopSeminarSerializer
    queryset = UserWorkShopSeminar.objects.all()

    def patch(self, request, user_id, workshop_seminar_id, format=None):
        workshop_seminar_ins = UserWorkShopSeminar.objects.filter(user_id=user_id,
                                                                  id=workshop_seminar_id).first()
        if workshop_seminar_ins:
            serializer = UserWorkShopSeminarSerializer(workshop_seminar_ins, data=request.data,
                                                       partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "enter valid id"}, status=status.HTTP_400_BAD_REQUEST)


class UserWorkshopOrSeminarDeleteView(ViewSet):
    def destroy(self, request, user_id, workshop_seminar_id):

        workshop_or_seminar_ins = UserWorkShopSeminar.objects.filter(id=workshop_seminar_id,
                                                                     user_id=user_id).exists()
        if workshop_or_seminar_ins:

            UserWorkShopSeminar.objects.filter(id=workshop_seminar_id,
                                               user_id=user_id).delete()
            return Response({"message: ": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message: ": "This data is not available"}, status=status.HTTP_400_BAD_REQUEST)


class UserWorkshopOrSeminarViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserWorkShopSeminar.objects.all()
    serializer_class = UserWorkShopSeminarSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_seminar = UserWorkShopSeminar.objects.get(id=self.kwargs.get('id'))

            if current_seminar.user == self.request.user:
                current_seminar.is_public = not current_seminar.is_public
                current_seminar.save()
                data = {
                    "id": current_seminar.id,
                    "created_date": current_seminar.created_date,
                    "modified_date": current_seminar.modified_date,
                    "enable": current_seminar.enable,
                    "workshop_or_seminar_name": current_seminar.workshop_or_seminar_name,
                    "institutions": current_seminar.institutions,
                    "start_date": current_seminar.start_date,
                    "end_date": current_seminar.end_date,
                    "is_public": current_seminar.is_public,
                    "user": current_seminar.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserBookPublicationsView(generics.ListCreateAPIView):
    serializer_class = UserBookPublicationsSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if ser.is_valid(raise_exception=True):
            self.perform_create(ser)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if not self.kwargs.get('user_id'):
            current_user = self.request.user
            return UserBookPublications.objects.filter(user=current_user)
        else:
            current_user = self.kwargs.get('user_id')
            return UserBookPublications.objects.filter(user=current_user, is_public=True)


class UserBookPublicationsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserBookPublicationsSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = UserBookPublications.objects.all()

    def get_queryset(self):
        return UserBookPublications.objects.filter(user=self.request.user, id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Something Wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if UserBookPublications.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class UserBookPublicationsViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserBookPublications.objects.all()
    serializer_class = UserBookPublicationsSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_book = UserBookPublications.objects.get(id=self.kwargs.get('id'))

            if current_book.user == self.request.user:
                current_book.is_public = not current_book.is_public
                current_book.save()
                data = {
                    "id": current_book.id,
                    "created_date": current_book.created_date,
                    "modified_date": current_book.modified_date,
                    "enable": current_book.enable,
                    "publish_url": current_book.publish_url,
                    "authors_name": current_book.authors_name,
                    "publisher_name": current_book.publisher_name,
                    "publication_year": current_book.publication_year,
                    "is_public": current_book.is_public,
                    "user": current_book.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserWorkingSkillView(generics.ListCreateAPIView):
    serializer_class = UserWorkingSkillSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if ser.is_valid(raise_exception=True):
            self.perform_create(ser)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if not self.kwargs.get('user_id'):
            current_user = self.request.user
            return UserWorkingSkill.objects.filter(user=current_user)
        else:
            current_user = self.kwargs.get('user_id')
            return UserWorkingSkill.objects.filter(user=current_user, is_public=True)


class UserWorkingSkillUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserWorkingSkillSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = UserWorkingSkill.objects.all()

    def get_queryset(self):
        return UserWorkingSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if UserWorkingSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Something Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if UserWorkingSkill.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class UserWorkingSkillViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserWorkingSkill.objects.all()
    serializer_class = UserWorkingSkillSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_skill = UserWorkingSkill.objects.get(id=self.kwargs.get('id'))

            if current_skill.user == self.request.user:
                current_skill.is_public = not current_skill.is_public
                current_skill.save()
                data = {
                    "id": current_skill.id,
                    "created_date": current_skill.created_date,
                    "modified_date": current_skill.modified_date,
                    "enable": current_skill.enable,
                    "key_working_skill": current_skill.key_working_skill,
                    "career_object_plan": current_skill.career_object_plan,
                    "area_of_interest": current_skill.area_of_interest,
                    "is_public": current_skill.is_public,
                    "user": current_skill.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class AcademicAchievementView(generics.ListCreateAPIView):
    serializer_class = AcademicAchievementSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if ser.is_valid(raise_exception=True):
            self.perform_create(ser)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if not self.kwargs.get('user_id'):
            current_user = self.request.user
            return AcademicAchievement.objects.filter(user=current_user)
        else:
            current_user = self.kwargs.get('user_id')
            return AcademicAchievement.objects.filter(user=current_user, is_public=True)


class AcademicAchievementUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AcademicAchievementSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = AcademicAchievement.objects.all()

    def get_queryset(self):
        return AcademicAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if AcademicAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Something Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if AcademicAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class AcademicAchievementViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AcademicAchievement.objects.all()
    serializer_class = AcademicAchievementSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_achievement = AcademicAchievement.objects.get(id=self.kwargs.get('id'))

            if current_achievement.user == self.request.user:
                current_achievement.is_public = not current_achievement.is_public
                current_achievement.save()
                data = {
                    "id": current_achievement.id,
                    "created_date": current_achievement.created_date,
                    "modified_date": current_achievement.modified_date,
                    "enable": current_achievement.enable,
                    "achievement": current_achievement.achievement,
                    "institution": current_achievement.institution,
                    "year": current_achievement.year,
                    "is_public": current_achievement.is_public,
                    "user": current_achievement.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class NotableAchievementView(generics.ListCreateAPIView):
    serializer_class = NotableAchievementSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if ser.is_valid(raise_exception=True):
            self.perform_create(ser)
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if not self.kwargs.get('user_id'):
            current_user = self.request.user
            return NotableAchievement.objects.filter(user=current_user)
        else:
            current_user = self.kwargs.get('user_id')
            return NotableAchievement.objects.filter(user=current_user, is_public=True)


class NotableAchievementUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotableAchievementSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = NotableAchievement.objects.all()

    def get_queryset(self):
        return NotableAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if NotableAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Something Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if NotableAchievement.objects.filter(user=self.request.user, id=self.kwargs.get('id')).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class NotableAchievementViewHideView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NotableAchievement.objects.all()
    serializer_class = NotableAchievementSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            current_achievement = NotableAchievement.objects.get(id=self.kwargs.get('id'))

            if current_achievement.user == self.request.user:
                current_achievement.is_public = not current_achievement.is_public
                current_achievement.save()
                data = {
                    "id": current_achievement.id,
                    "created_date": current_achievement.created_date,
                    "modified_date": current_achievement.modified_date,
                    "enable": current_achievement.enable,
                    "notable_achievement": current_achievement.notable_achievement,
                    "year": current_achievement.year,
                    "is_public": current_achievement.is_public,
                    "user": current_achievement.user.id
                }
                return Response(data)
            else:
                return Response({'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
