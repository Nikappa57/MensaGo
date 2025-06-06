from django.shortcuts import redirect, render
from ..forms import ProfileForm, AllergensForm, CustomPasswordChangeForm
import time
import qrcode
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def profile_home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    # Initialize forms
    form = ProfileForm(instance=user)
    allergens_form = AllergensForm(initial={'suffers_from': user.suffers_from.all()})
    password_form = CustomPasswordChangeForm(user)

    if request.method == 'POST':
        update_section = request.POST.get('update_section')

        if update_section == 'avatar':
            if 'propic' in request.FILES:
                user.propic = request.FILES['propic']
                user.save()
            return redirect('profile')
        elif update_section == 'allergens':
            allergens_form = AllergensForm(request.POST)
            if allergens_form.is_valid():
                allergens_data = allergens_form.cleaned_data['suffers_from']
                user.suffers_from.set(allergens_data)
                user.save()
                
            return redirect('profile')
        elif update_section == 'password':
            password_form = CustomPasswordChangeForm(user, request.POST)

            # Detect AJAX request
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                if is_ajax:
                    return JsonResponse({'success': True})
                return redirect('profile')  # Redirect only on non-AJAX success
            else:
                if is_ajax:
                    return JsonResponse({'success': False, 'errors': password_form.errors}, status=400)
                return render(request, 'profile/profile.html', {
                    'current_user': user,
                    'form': form,
                    'allergens_form': allergens_form,
                    'password_form': password_form,
                })
        else:
            form = ProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile')

    context = {
        'current_user': user,
        'form': form,
        'allergens_form': allergens_form,
        'password_form': password_form,
        # Serialize original allergens as list of IDs for JSON in template
        'original_allergens': list(user.suffers_from.values_list('name', flat=True)),
    }

    return render(request, 'profile/profile.html', context)

def profile_qrcode(request):
    user = request.user
    current_minute = int(time.time() // 600) # 10-minute interval
    msg = f"{user.email}:{current_minute}"
    qr_img = qrcode.make(msg)
    response = HttpResponse(content_type="image/png")
    qr_img.save(response, "PNG")
    return response

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile' + '?password_changed=true')
        else:
            messages.error(request, "Errore nel cambio password. Assicurati di aver inserito correttamente la password attuale e la nuova password.")
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return redirect('profile')
