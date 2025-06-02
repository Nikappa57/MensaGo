from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse

from ..models import CustomUser

@method_decorator(staff_member_required, name='dispatch')
class QRScannerView(TemplateView):
	"""View for scanning QR codes in admin area."""
	template_name = 'admin/qr_scanner.html'


@staff_member_required
def qr_scan_api(request):
	"""API endpoint to get user information from email in QR code."""
	email = request.GET.get('email', '')
	print(f"Received email: {email}")  # Debugging line to check the received email
	
	# Pulizia dell'email (rimuovi spazi e prendi solo la prima parte se contiene due punti)
	email = email.strip()
	if ':' in email:
		email = email.split(':', 1)[0]
	
	print(f"Processed email: {email}")  # Debugging line to check the processed email
	print(f"Request path: {request.path}")  # Debugging to check the requested path
	print(f"Request headers: {request.headers}")  # Check request headers
	print(f"Current user: {request.user.username}")  # Verify the current user
	
	if not email:
		return JsonResponse({
			'success': False,
			'message': 'Email non specificata'
		})
	
	try:
		user = CustomUser.objects.select_related('economical_level').get(email=email)
		
		return JsonResponse({
			'success': True,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'profile_pic': user.propic.url if user.propic else None,
			'economical_level': user.economical_level.name if user.economical_level else None,
			'cost': str(user.economical_level.cost) if user.economical_level else "7.90",
			'credit': str(user.credit)
		})
	except CustomUser.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': f'Utente con email {email} non trovato'
		})
