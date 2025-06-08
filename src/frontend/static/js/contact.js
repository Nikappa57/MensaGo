document.addEventListener('DOMContentLoaded', function() {
	const contactForm = document.getElementById('contactForm');
	const formStatus = document.getElementById('formStatus');
	
	if (contactForm) {
		contactForm.addEventListener('submit', function(event) {
			event.preventDefault();

			const formDataObj = new FormData(contactForm);
			
			// Send POST request to the server
			fetch(window.location.href, {
				method: 'POST',
				body: formDataObj,
				headers: {
					'X-Requested-With': 'XMLHttpRequest'
				}
			})
			.then(response => response.json())
			.then(data => {
				// Show status message
				formStatus.style.display = 'block';
				
				if (data.status === 'success') {
					// Show success message
					formStatus.className = 'col-12 mt-2 alert alert-success';
					formStatus.textContent = data.message;
					
					// Reset the form
					contactForm.reset();
					
					// Hide success message after 3 seconds
					setTimeout(() => {
						formStatus.style.display = 'none';
					}, 3000);
				} else {
					// Show error message
					formStatus.className = 'col-12 mt-2 alert alert-danger';
					formStatus.textContent = 'Si è verificato un errore. Riprova.';
				}
			})
			.catch(error => {
				console.error('Error:', error);
				formStatus.style.display = 'block';
				formStatus.className = 'col-12 mt-2 alert alert-danger';
				formStatus.textContent = 'Si è verificato un errore. Riprova.';
			});
		});
	}
});
