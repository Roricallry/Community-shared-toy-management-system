from django.shortcuts import render, redirect, get_object_or_404
from .models import Toy_type
from .forms import ToyTypeForm

def Toy_Inquire(request):
    toy_types = Toy_type.objects.all()
    return render(request, 'toy_type/inquire.html', {'toy_types': toy_types})

def Toy_Create(request):
    if request.method == 'POST':
        form = ToyTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Toy_Inquire')
    else:
        form = ToyTypeForm()
    return render(request, 'toy_type/create.html', {'form': form})

def Toy_Update(request, id):
    toy_type = get_object_or_404(Toy_type, id=id)
    if request.method == 'POST':
        form = ToyTypeForm(request.POST, instance=toy_type)
        if form.is_valid():
            form.save()
            return redirect('Toy_Inquire')
    else:
        form = ToyTypeForm(instance=toy_type)
    return render(request, 'toy_type/update.html', {'form': form, 'toy_type': toy_type})

def Toy_Delete(request, id):
    toy_type = get_object_or_404(Toy_type, id=id)
    if request.method == 'POST':
        toy_type.delete()
        return redirect('Toy_Inquire')
    return render(request, 'toy_type/delete.html', {'toy_type': toy_type})

def Toy_Search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        toy_types = Toy_type.objects.filter(name__icontains=query)
        return render(request, 'toy_type/inquire.html', {'toy_types': toy_types})
    return redirect('Toy_Inquire')