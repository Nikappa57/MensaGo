from django.shortcuts import redirect, render
from ..forms import ProfileForm
import time, hmac, hashlib
from django.conf import settings
import qrcode
from django.http import HttpResponse
from django.urls import path


def profile_home(request):
	user = request.user
	if not user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		
		
		form = ProfileForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = ProfileForm(instance=user)

	context = {
		'current_user': user,
		'form': form,
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
