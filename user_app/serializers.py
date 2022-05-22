from sqlite3.dbapi2 import IntegrityError

from django.contrib.auth import authenticate

from django.db import models, transaction
from django.db.models import fields
from django.utils.crypto import get_random_string
from rest_framework import serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from otp import generate_otp
from user_app.models import User, UserGeneralInfo, UserContactInformation, UserLanguageProficiency, UserWorkShopSeminar, \
    UserTraining, UserAcademicDegree, UserAcademicDiscipline, UserSkill, WorkingHistory, UserOtherInfo, \
    ResearchThoughts, ResearchSummary, ResearchWork, ResearchArticle, ResearchSkill, IeltsToeflScore, \
    UserBookPublications, UserWorkingSkill, AcademicAchievement, NotableAchievement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'birthdate', 'gender', 'academic_discipline',
            'profession', 'verification_code',)

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data.get('email'))
        user = User(email=validated_data.get('email'), username=validated_data.get('email'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    birthdate=validated_data.get('birthdate'),
                    gender=validated_data.get('gender'),
                    academic_discipline=validated_data.get('academic_discipline'),
                    profession=validated_data.get('profession'),
                    verification_code=validated_data.get('verification_code')
                    )
        user.set_password(validated_data.get('password'))

        user.save()

        return user


class UserGeneralInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGeneralInfo
        fields = '__all__'

    def create(self, validated_data):
        return super(UserGeneralInfoSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserGeneralInfoSerializer, self).validate(validated_data)


class UserNameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']


class UserContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContactInformation
        fields = '__all__'

    def create(self, validated_data):
        return super(UserContactInfoSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserContactInfoSerializer, self).validate(validated_data)


class UserLanguageProficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguageProficiency
        fields = '__all__'

    def create(self, validated_data):
        return super(UserLanguageProficiencySerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserLanguageProficiencySerializer, self).validate(validated_data)


class UserIeltsToeflScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = IeltsToeflScore
        fields = '__all__'

    def create(self, validated_data):
        return super(UserIeltsToeflScoreSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserIeltsToeflScoreSerializer, self).validate(validated_data)


class ResearchSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchSkill
        fields = '__all__'

    def create(self, validated_data):
        return super(ResearchSkillSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(ResearchSkillSerializer, self).validate(validated_data)


class ResearchArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchArticle
        fields = '__all__'

    def create(self, validated_data):
        return super(ResearchArticleSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(ResearchArticleSerializer, self).validate(validated_data)


class ResearchWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchWork
        fields = '__all__'

    def create(self, validated_data):
        return super(ResearchWorkSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(ResearchWorkSerializer, self).validate(validated_data)


class ResearchSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchSummary
        fields = '__all__'

    def create(self, validated_data):
        return super(ResearchSummarySerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(ResearchSummarySerializer, self).validate(validated_data)


class ResearchThoughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchThoughts
        fields = '__all__'

    def create(self, validated_data):
        return super(ResearchThoughtsSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(ResearchThoughtsSerializer, self).validate(validated_data)


class UserOtherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtherInfo
        fields = '__all__'

    def create(self, validated_data):
        return super(UserOtherInfoSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserOtherInfoSerializer, self).validate(validated_data)


class WorkingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHistory
        fields = '__all__'

    def create(self, validated_data):
        return super(WorkingHistorySerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(WorkingHistorySerializer, self).validate(validated_data)


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'

    def create(self, validated_data):
        return super(UserSkillSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserSkillSerializer, self).validate(validated_data)


class UserAcademicDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAcademicDiscipline
        fields = '__all__'

    def create(self, validated_data):
        return super(UserAcademicDisciplineSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserAcademicDisciplineSerializer, self).validate(validated_data)


class UserAcademicDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAcademicDegree
        fields = '__all__'

    def create(self, validated_data):
        return super(UserAcademicDegreeSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserAcademicDegreeSerializer, self).validate(validated_data)


class UserTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTraining
        fields = '__all__'

    def create(self, validated_data):
        return super(UserTrainingSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserTrainingSerializer, self).validate(validated_data)


class UserWorkShopSeminarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkShopSeminar
        fields = '__all__'

    def create(self, validated_data):
        return super(UserWorkShopSeminarSerializer, self).create(validated_data)

    def validate(self, validated_data):
        return super(UserWorkShopSeminarSerializer, self).validate(validated_data)


class UserBookPublicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookPublications
        fields = '__all__'


class UserWorkingSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkingSkill
        fields = '__all__'


class AcademicAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicAchievement
        fields = '__all__'


class NotableAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotableAchievement
        fields = '__all__'


class TokenSerializer(AuthTokenSerializer):
    pass


class ForgotPasswordTokenSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email')  # name or username ?

    def get_id(self, obj):
        return obj.id

    def get_email(self, obj):
        return obj.username


class ResetPasswordSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True,
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False, write_only=True
    )

    @transaction.atomic
    def validate(self, attrs):

        verification_code = attrs.get('verification_code')
        password = attrs.get('password')

        if verification_code and password:
            user = User.objects.filter(verification_code=verification_code).first()

            # user = student if student is not None else teacher

            if not user:
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                user.set_password(raw_password=password)
                user.save()

                db_transaction = transaction.savepoint()
                user.verification_code = generate_otp()
                user.save()

                try:
                    transaction.savepoint_commit(db_transaction)
                except IntegrityError:
                    transaction.savepoint_rollback(db_transaction)
        else:
            msg = 'Must include "verification_code" and "password".'
            raise serializers.ValidationError(msg, code='error')

        return attrs


class OTPSerializer(serializers.Serializer):
    token = serializers.IntegerField()
