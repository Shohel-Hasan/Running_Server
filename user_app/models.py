from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser)
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from core_app.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError("The email must be set")

        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        if password is None:
            raise TypeError("Superusers must have a password.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # user = self.model(
        #     email=self.normalize_email(email)
        #
        # )
        # user.set_password(password)
        # user.admin = True
        # # user.username = email
        # # user.is_superuser = True
        # user.staff = True
        # user.active = True
        # user.save(using=self._db)
        # return user
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # a superuser

    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    academic_discipline = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    verification_code = models.CharField(max_length=10, blank=True, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is__staff(self):
    #     """Is the user a member of staff?"""
    #     return self.is_staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    def as_json(self):
        token, created = Token.objects.get_or_create(user=self)
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "token": token.key,
        }


class AppToken(models.Model):
    user = models.ForeignKey(User, related_name="tokens", on_delete=models.CASCADE)
    kind = models.CharField(max_length=200)
    token = models.CharField(max_length=100, blank=True, null=True)


@receiver(post_save, sender=User)
def add_token(sender, instance, **kwargs):
    token = AppToken(user=instance, token=instance.verification_code, kind="OTP")
    token.save()


class UserGeneralInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='general_info_user')
    profile_pic = models.ImageField(upload_to='user_profile_pic', null=True, blank=True)
    cover_pic = models.ImageField(upload_to='user_cover_pic', null=True, blank=True)
    height_feet = models.CharField(max_length=10, null=True, blank=True)
    height_inch = models.CharField(max_length=10, null=True, blank=True)
    weight_kg = models.CharField(max_length=10, null=True, blank=True)
    weight_gm = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    marital_status = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    nid_number = models.JSONField(null=True, blank=True)  # multiple data (array field)
    fathers_name = models.TextField(null=True, blank=True)
    mothers_name = models.TextField(null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    native_language = models.CharField(max_length=50, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserContactInformation(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    present_address = models.CharField(max_length=250, null=True, blank=True)  # details text
    permanent_address = models.CharField(max_length=250, null=True, blank=True)  # details text
    email_address = models.EmailField(null=True, blank=True)  # multiple data (array field)
    phone_number = models.JSONField(null=True, blank=True)  # multiple data (array field)
    is_public = models.BooleanField(default=True)


class UserLanguageProficiency(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_name = models.CharField(max_length=250, null=True, blank=True)
    listening = models.CharField(max_length=100, null=True, blank=True)
    speaking = models.CharField(max_length=100, null=True, blank=True)
    reading = models.CharField(max_length=100, null=True, blank=True)
    writing = models.CharField(max_length=100, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class IeltsToeflScore(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    ielts_toefl_score = models.CharField(max_length=10, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class ResearchSkill(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area_of_research_interest = models.JSONField(null=True, blank=True)  # multiple data (array field)
    key_research_skill = models.JSONField(null=True, blank=True)  # multiple data (array field)
    is_public = models.BooleanField(default=True)


class ResearchArticle(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_link = models.BooleanField(default=False)
    url_link = models.URLField(max_length=250, null=True, blank=True)
    article_name = models.CharField(max_length=100, null=True, blank=True)
    authors_name = models.CharField(max_length=100, null=True, blank=True)
    journals_name = models.CharField(max_length=100, null=True, blank=True)
    publisher_name = models.CharField(max_length=100, null=True, blank=True)
    publication_year = models.CharField(max_length=100, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class ResearchWork(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    involvement_research_work_info = models.URLField(max_length=250, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_present = models.BooleanField(default=False, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class ResearchSummary(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_link = models.URLField(max_length=250, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class ResearchThoughts(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_link = models.URLField(max_length=250, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserOtherInfo(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key_working_skill = models.CharField(max_length=250, null=True, blank=True)  # multiple data (array field)
    career_objective_plan = models.CharField(max_length=250, null=True, blank=True)  # multiple data (array field)
    area_of_working_interest = models.CharField(max_length=250, null=True, blank=True)  # multiple data (array field)
    is_public = models.BooleanField(default=True)


class WorkingHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_present = models.BooleanField(default=False, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserSkill(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    technology_skill = models.CharField(max_length=250, null=True, blank=True)  # multiple data (array field)
    other_notable_skill = models.CharField(max_length=250, null=True, blank=True)  # multiple data (array field)
    is_public = models.BooleanField(default=True)


class UserAcademicDiscipline(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    academic_discipline = models.CharField(max_length=250, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserAcademicDegree(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    institutions = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserTraining(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_name = models.CharField(max_length=100, null=True, blank=True)
    institutions = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_present = models.BooleanField(default=False, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserWorkShopSeminar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop_or_seminar_name = models.CharField(max_length=100, null=True, blank=True)
    institutions = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)


class UserBookPublications(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_publications_user")
    publish_url = models.URLField(null=True, blank=True)
    book_name = models.CharField(max_length=150, null=True, blank=True)
    authors_name = models.CharField(max_length=255, null=True, blank=True)
    publisher_name = models.CharField(max_length=255, null=True, blank=True)
    publication_year = models.DateField()
    is_public = models.BooleanField(default=True)


class UserWorkingSkill(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="working_skill_user")
    key_working_skill = models.CharField(max_length=255, null=True, blank=True)
    career_object_plan = models.TextField()
    area_of_interest = models.CharField(max_length=255, blank=True, null=True)
    is_public = models.BooleanField(default=True)


class AcademicAchievement(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="academic_achievement_user")
    achievement = models.CharField(max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=True)


class NotableAchievement(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notable_achievement_user")
    notable_achievement = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=True)
