from django.shortcuts import render, redirect
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Photo, Like
from django.contrib.auth import login
from .forms import RegisterForm


@login_required
def index(request):
    photos = Photo.objects.all()
    liked_photo_ids = Like.objects.filter(user=request.user).values_list('photo_id', flat=True)
    return render(request, 'index.html', {
        'photos': photos,
        'liked_photo_ids': list(liked_photo_ids),
    })



@login_required
@require_POST
def like_photo(request):
    photo_id = request.POST.get('photo_id')
    if not photo_id:
        return JsonResponse({'error': 'No photo_id'}, status=400)

    photo = get_object_or_404(Photo, id=photo_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, photo=photo)

    if not created:
        like.delete()
        Photo.objects.filter(id=photo.id).update(total_likes=F('total_likes') - 1)
        liked = False
    else:
        Photo.objects.filter(id=photo.id).update(total_likes=F('total_likes') + 1)
        liked = True

    photo.refresh_from_db()

    return JsonResponse({
        'liked': liked,
        'total_likes': photo.total_likes
    })


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:index')  # после загрузки редирект на главную
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
