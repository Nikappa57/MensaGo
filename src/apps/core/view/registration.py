from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..forms import ProfileAuthenticationForm, RegistrationForm


def register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already registered as {user.email}")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            psw = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=psw)
            login(request, user)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            else:
                return redirect('home')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'profile/register.html', context)


def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('home')
	else:
		return HttpResponse("You are not logged in")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    destination = get_redirect_if_exists(request)

    if request.POST:
        form = ProfileAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            psw = form.cleaned_data.get('password')
            user = authenticate(email=email, password=psw)
            if user is not None:
                login(request, user)

                destination = get_redirect_if_exists(request)

                if destination:
                    return redirect(destination)
                else:
                    return redirect('home')
        else:
            context['form'] = form

    return render(request, 'profile/login.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect


