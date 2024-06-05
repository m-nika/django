from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import GameReviewForm
from .models import GameReview, Publisher, Game
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

@csrf_protect
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class PublisherView(generic.ListView):
    model = Publisher
    template_name = 'publishers.html'
    paginate_by = 3

class PublisherDetailView(generic.DetailView):
    model = Publisher
    template_name = 'publisher.html'
    context_object_name = 'publisher'

class GameListView(generic.ListView):
    model = Game
    template_name = 'games.html'
    paginate_by = 3

class GameDetailView(FormMixin, generic.DetailView):
    model = Game
    template_name = 'game.html'
    form_class = GameReviewForm

    def get_success_url(self):
        return reverse('game', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.game = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(GameDetailView, self).form_valid(form)

def index(request):
    max_rating = GameReview.objects.aggregate(Max('rating'))['rating__max']
    
    if max_rating is not None:
        best_reviews = GameReview.objects.filter(rating=max_rating).order_by('-date_created')
        if best_reviews.exists():
            best_review = best_reviews.first()
            best_game = best_review.game
        else:
            best_review = None
            best_game = None
    else:
        best_review = None
        best_game = None
    
    context = {
        'best_game': best_game,
        'best_review': best_review
    }
    
    return render(request, 'index.html', context)


