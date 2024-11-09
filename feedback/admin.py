from django.contrib import admin
from .models import UserProfile, FeedbackProcess, Review

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'department', 'manager')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'  

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email' 

    def department(self, obj):
        return dict(UserProfile.DEPARTMENT_CHOICES).get(obj.department)
    department.short_description = 'Department' 
    def manager(self, obj):
        return obj.manager.user.username if obj.manager else None
    manager.short_description = 'Manager'
admin.site.register(UserProfile, UserProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ( 'department','reviewee','feedback_process_id', 'reviewer', 'review_id', 'review_text')
     
     
    def department(self, obj):
        return dict(UserProfile.DEPARTMENT_CHOICES).get(obj.feedback_process.reviewee.department)
    department.short_description = 'Department'

    def reviewee(self, obj):
        return obj.feedback_process.reviewee.user.username
    reviewee.short_description = 'Reviewee'

    
    def feedback_process_id(self, obj):
        return obj.feedback_process.id
    feedback_process_id.short_description = 'Feedback Process ID'


    def review_id(self, obj):
        return obj.id
    review_id.short_description = 'Review ID'

    def reviewer(self, obj):
        return obj.reviewer.user.username if obj.reviewer else 'No reviewer'
    reviewer.short_description = 'Reviewer'

    
    def review_text(self, obj):
        return obj.review_text
    review_text.short_description = 'Review Text'
admin.site.register(Review, ReviewAdmin)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
class FeedbackProcessAdmin(admin.ModelAdmin):
    list_display = ('reviewee', 'manager', 'creation_date')
    search_fields = ('reviewee__user__username', 'manager__user__username')
    inlines = [ReviewInline]
admin.site.register(FeedbackProcess, FeedbackProcessAdmin)