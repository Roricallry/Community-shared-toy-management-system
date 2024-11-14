from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcement
from .forms import AnnouncementForm

def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'announce/announcement_list.html', {'announcements': announcements})

def announcement_create(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement')
    else:
        form = AnnouncementForm()
    return render(request, 'announce/announcement_form.html', {'form': form})

def announcement_update(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announce/announcement_form.html', {'form': form})

def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        announcement.delete()
        return redirect('announcement')
    return render(request, 'announce/announcement_confirm_delete.html', {'announcement': announcement})


def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announce/announcement_detail.html', {'announcement': announcement})

def announcement_user(request):
    announcements = Announcement.objects.all()
    return render(request, 'announce/announcement_user.html', {'announcements': announcements})
