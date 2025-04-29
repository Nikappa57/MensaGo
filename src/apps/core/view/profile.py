from django.shortcuts import redirect, render


# TODO: login required
# TODO: update user profile (altra pagina? boh marius)
def profile_home(request):
    context = {
        "current_user": request.user,
    }

    return render(request, "profile/profile.html", context)


# TODO: login required
def preferences(request):
    current_user = request.user
    context = {
        "current_user": current_user,
    }

    return render(request, "profile/preferences.html", context)


#TODO: login required
def accreditation(request):
    current_user = request.user
    context = {
        "current_user": current_user,
    }

    return render(request, "profile/accreditation.html", context)


#TODO: login required
def accreditation_pay(request):
    current_user = request.user
    context = {
        "current_user": current_user,
    }

    # TODO: controlla il saldo e scala i soldi se li ha
    # TODO: mostra un mex di success o error (senza pagina a se)

    return redirect("accreditation")
