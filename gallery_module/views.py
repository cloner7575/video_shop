from django.shortcuts import render
from .models import Gallery,UserArtwork


# Create your views here.

def index(request):
    gallery = Gallery.objects.all()
    context = {'gallery': gallery}
    return render(request, 'gallery_module/index.html', context)

def gallery_detail(request, pk):
    gallery = Gallery.objects.get(pk=pk)

    context = {'gallery': gallery}
    return render(request, 'gallery_module/gallery_detail.html', context)

def gallery_payment(request, pk):
    gallery = Gallery.objects.get(pk=pk)
    user_artwork = UserArtwork.objects.filter(user=request.user, gallery=gallery)
    if not user_artwork:
        user_artwork = UserArtwork.objects.create(user=request.user, gallery=gallery)
        user_artwork.save()
    context = {'gallery': gallery}
    return render(request, 'gallery_module/gallery_payment.html', context)


