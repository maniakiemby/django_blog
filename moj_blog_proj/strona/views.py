from django.shortcuts import render
from .models import Post
from django.utils import timezone
from .forms import PostForm, UserRegisterForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# data_publikacji_lte znaczy, że filtrujemy po dacie publikacji i sortujemy


def index(request):
    posty = Post.objects.filter(data_publikacji__lte=timezone.now()).order_by('data_publikacji')
    return render(request, 'strona/index.html', {'posts': posty})


@login_required
def nowy(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_publikacji = timezone.now()
            post.save()
            return redirect('strona:wpis', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'strona/wpis.html', {'form': form})


def wpis(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'strona/wpis.html', {'post': post})


@login_required
def edycja(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_publikacji = timezone.now()
            post.save()
            return redirect('strona:edycja', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'strona/edycja.html', {'form': form})


def rejestracja_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    else:
        form = UserRegisterForm()

    return render(request, 'strona/rejestracja.html', {'form': form,})
