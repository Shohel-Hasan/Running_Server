from django.contrib import admin
from .models import (
    User,
    UserGeneralInfo,
    UserContactInformation,
    UserLanguageProficiency,
    IeltsToeflScore,
    ResearchSkill,
    ResearchArticle,
    ResearchWork,
    ResearchSummary,
    ResearchThoughts,
    UserOtherInfo,
    WorkingHistory,
    UserSkill,
    UserAcademicDiscipline,
    UserTraining,
    UserWorkShopSeminar, UserAcademicDegree, UserWorkingSkill, UserBookPublications, AcademicAchievement,
    NotableAchievement
)


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'gender', 'academic_discipline', 'profession', 'admin',
                    'is_superuser', 'is_staff']


# @admin.register(UserGeneralInfo) class UserGeneralInfoAdmin(admin.ModelAdmin): list_display = ['user',
# 'height_feet', 'height_inch','weight_kg', 'weight_gm', 'blood_group', 'nationality','marital_status', 'nid_number',
# 'fathers_name', 'mothers_name', 'religion', 'native_language']

admin.site.register(UserContactInformation)
admin.site.register(UserGeneralInfo)
admin.site.register(UserLanguageProficiency)
admin.site.register(IeltsToeflScore)
admin.site.register(ResearchSkill)
admin.site.register(ResearchArticle)
admin.site.register(ResearchWork)
admin.site.register(ResearchSummary)
admin.site.register(ResearchThoughts)
admin.site.register(UserOtherInfo)
admin.site.register(WorkingHistory)
admin.site.register(UserSkill)
admin.site.register(UserAcademicDiscipline)
admin.site.register(UserAcademicDegree)
admin.site.register(UserTraining)
admin.site.register(UserWorkShopSeminar)
admin.site.register(UserBookPublications)
admin.site.register(UserWorkingSkill)
admin.site.register(AcademicAchievement)
admin.site.register(NotableAchievement)
