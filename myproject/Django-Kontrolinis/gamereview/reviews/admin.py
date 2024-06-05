from django.contrib import admin


from django.contrib import admin
from reviews.models import GameReview

class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'reviewer', 'review_content', 'date_created')
    list_editable = ('reviewer',)

admin.site.register(GameReview, GameReviewAdmin)
