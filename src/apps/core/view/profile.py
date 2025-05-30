from django.shortcuts import redirect, render
from ..forms import ProfileForm, AllergensForm, CustomPasswordChangeForm
import time, hmac, hashlib
from django.conf import settings
import qrcode
from django.http import HttpResponse
from django.urls import path
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
		elif update_section == 'password':
			# Handle password update
			password_form = CustomPasswordChangeForm(user, request.POST)
			if password_form.is_valid():
				user = password_form.save()
				# Aggiorna la sessione per evitare il logout dell'utente
				update_session_auth_hash(request, user)
				print("DEBUG: Password updated successfully")
			else:
				print("DEBUG: Password form errors:", password_form.errors)
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
		'password_form': password_form,
	}

	return render(request, 'profile/profile.html', context)

def profile_qrcode(request):
	user = request.user
	current_minute = int(time.time() // 60)
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
			# Importante: aggiorna la sessione per evitare il logout dell'utente
			update_session_auth_hash(request, user)
			# Redirect alla pagina del profilo con un parametro per mostrare un messaggio di successo
			return redirect('profile' + '?password_changed=true')
		else:
			# Se il form non è valido, mostra gli errori
			print("DEBUG: Form non valido:", form.errors)
	else:
		form = CustomPasswordChangeForm(request.user)
	
	return redirect('profile')	
