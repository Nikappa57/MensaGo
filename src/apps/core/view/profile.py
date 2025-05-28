from django.shortcuts import redirect, render
from ..forms import ProfileForm, AllergensForm
import time, hmac, hashlib
from django.conf import settings
import qrcode
from django.http import HttpResponse
from django.urls import path


def profile_home(request):
	user = request.user
	if not user.is_authenticated:
		return redirect('login')

	# Initialize forms
	form = ProfileForm(instance=user)
	allergens_form = AllergensForm(initial={'suffers_from': user.suffers_from.all()})

	if request.method == 'POST':
		update_section = request.POST.get('update_section')
		print(f"DEBUG: update_section = {update_section}")
		print(f"DEBUG: POST data = {request.POST}")
		
		if update_section == 'avatar':
			# Handle only avatar update
			if 'propic' in request.FILES:
				user.propic = request.FILES['propic']
				user.save()
				print("DEBUG: Avatar updated successfully")
			return redirect('profile')
		elif update_section == 'allergens':
			# Handle only allergens update using AllergensForm
			allergens_form = AllergensForm(request.POST)
			print(f"DEBUG: AllergensForm is_valid = {allergens_form.is_valid()}")
			if allergens_form.is_valid():
				# Save only allergens field
				allergens_data = allergens_form.cleaned_data['suffers_from']
				print(f"DEBUG: Allergens data = {allergens_data}")
				user.suffers_from.set(allergens_data)
				user.save()
				print("DEBUG: Allergens updated successfully")
			else:
				# Debug: stampa errori del form
				print("DEBUG: AllergensForm errors:", allergens_form.errors)
			return redirect('profile')
		else:
			# Handle full form update (fallback)
			form = ProfileForm(request.POST, request.FILES, instance=user)
			if form.is_valid():
				form.save()
				return redirect('profile')

	context = {
		'current_user': user,
		'form': form,
		'allergens_form': allergens_form,
	}

	return render(request, 'profile/profile.html', context)


def profile_qrcode(request):
	user = request.user
	current_minute = int(time.time() // 60)
	msg = f"{user.id}:{current_minute}"
	sig = hmac.new(settings.SECRET_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()
	qr_img = qrcode.make(sig)
	response = HttpResponse(content_type="image/png")
	qr_img.save(response, "PNG")
	return response


urlpatterns = [
	path('profile/qrcode/', profile_qrcode, name='profile_qrcode'),
]

def accreditation(request):
	# Placeholder for accreditation logic
	return render(request, 'profile/accreditation.html')
def accreditation_pay(request):
	# Placeholder for accreditation payment logic
	return render(request, 'profile/accreditation_pay.html')
def preferences(request):
	# Placeholder for user preferences logic
	return render(request, 'profile/preferences.html')	
