
document.addEventListener('DOMContentLoaded', function() {
	function closeAllEditPanels(exceptId = null) {
		const editPanels = [
			'collapse-avatar-edit',
			'collapse-allergens-edit', 
			'collapse-password-edit'
		];
		
		editPanels.forEach(panelId => {
			if (panelId !== exceptId) {
				const element = document.getElementById(panelId);
				if (element && element.classList.contains('show')) {
					const collapse = bootstrap.Collapse.getInstance(element);
					if (collapse) collapse.hide();
				}
			}
		});
	}
	
	// Handle URL parameters for notifications
	const urlParams = new URLSearchParams(window.location.search);
	const passwordChanged = urlParams.get('password_changed');
	if (passwordChanged === 'true') {
		showNotification('Password modificata con successo', 'success');
		window.history.replaceState({}, document.title, window.location.pathname);
	}
	
	// Refresh QR code every 10 minute with animation
	setInterval(() => {
		const qrcode = document.getElementById('qrcode-img');
		if (!qrcode) return;
		
		const qrcodeWrapper = qrcode.closest('.qrcode-wrapper');
		if (qrcodeWrapper) {
			qrcodeWrapper.classList.add('loading');
		}
		
		// Create new src with timestamp to avoid cache
		const newSrc = qrcode.getAttribute('data-url') || qrcode.src;
		const updatedSrc = newSrc.split('?')[0] + `?t=${Math.floor(Date.now()/60000)}`;
		
		// When new image is loaded, remove loading class and add pulse animation
		qrcode.onload = () => {
			if (qrcodeWrapper) {
				qrcodeWrapper.classList.remove('loading');
			}
			qrcode.classList.add('animate__animated', 'animate__pulse');
			setTimeout(() => {
				qrcode.classList.remove('animate__animated', 'animate__pulse');
			}, 1000);
		};
		
		qrcode.src = updatedSrc;
	}, 60000);
	
	// Add hover and focus effects on form elements
	document.querySelectorAll('.profile-edit-form input, .profile-edit-form select').forEach(el => {
		el.addEventListener('focus', function() {
			const formControl = this.closest('.form-control-custom');
			if (formControl) {
				formControl.classList.add('focused');
			}
		});
		el.addEventListener('blur', function() {
			const formControl = this.closest('.form-control-custom');
			if (formControl) {
				formControl.classList.remove('focused');
			}
		});

		if (el.tagName === 'SELECT') {
			el.addEventListener('mousedown', function() {
				this.classList.add('select-active');
			});

			if (el.multiple) {
				el.addEventListener('change', function() {
					this.classList.toggle('has-selection', this.selectedOptions.length > 0);
				});
			}
		}
	});
	
	// Animation for edit buttons
	document.querySelectorAll('.profile-item-hover').forEach(item => {
		item.addEventListener('mouseenter', function() {
			const btn = this.querySelector('.btn');
			if (btn) {
				btn.classList.add('animate__animated', 'animate__pulse');
			}
		});
		item.addEventListener('mouseleave', function() {
			const btn = this.querySelector('.btn');
			if (btn) {
				btn.classList.remove('animate__animated', 'animate__pulse');
			}
		});
	});
	
	// Animation for forms on collapse/expand
	document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(btn => {
		const targetId = btn.getAttribute('data-bs-target');
		if (!targetId) return;
		
		const target = document.getElementById(targetId.substring(1));
		if (!target) return;
		
		target.addEventListener('show.bs.collapse', function() {
			this.classList.add('show');
		});
		
		target.addEventListener('hide.bs.collapse', function() {
			this.classList.remove('show');
		});

		target.classList.add('profile-edit-form');
	});
	
	// Transform allergen checkboxes for new design
	function setupAllergenCheckboxes() {
		const allergensContainer = document.querySelector('.allergens-checkboxes');
		if (!allergensContainer) return;
		
		if (allergensContainer.dataset.transformed === 'true') return;
		
		const originalInputs = [...allergensContainer.querySelectorAll('input[type="checkbox"]')];
		
		const ul = document.createElement('ul');
		
		originalInputs.forEach(input => {
			const originalLabel = input.parentElement.tagName === 'LABEL' ? 
				input.parentElement : input.nextElementSibling;
			
			const labelText = originalLabel ? 
				originalLabel.textContent.trim() : input.value;
			
			// Create list element
			const li = document.createElement('li');
			const newInput = input.cloneNode(true);
			
			// Create new label
			const newLabel = document.createElement('label');
			newLabel.setAttribute('for', newInput.id || `allergen-${Math.random().toString(36).substring(2, 9)}`);
			newLabel.textContent = labelText;
			
			// Add elements to DOM
			li.appendChild(newInput);
			li.appendChild(newLabel);
			ul.appendChild(li);
		});

		const helperText = allergensContainer.querySelector('.allergen-helper');
		allergensContainer.innerHTML = '';
		allergensContainer.appendChild(ul);
		
		// Re-add helper text
		if (helperText) {
			allergensContainer.appendChild(helperText);
		} else {
			const newHelperText = document.createElement('small');
			newHelperText.className = 'allergen-helper text-muted mt-2 d-block';
			newHelperText.innerHTML = '<i class="bi bi-info-circle me-1"></i>Seleziona una o più allergie dalla lista';
			allergensContainer.appendChild(newHelperText);
		}
		// Mark as transformed
		allergensContainer.dataset.transformed = 'true';
		attachAllergensEventListeners();
	}
	
	function attachAllergensEventListeners() {
		const allergensCheckboxes = document.querySelectorAll('input[name="suffers_from"]');
		if (allergensCheckboxes.length > 0) {
			allergensCheckboxes.forEach(checkbox => {
				// Remove any existing listeners
				checkbox.removeEventListener('change', checkboxChangeHandler);
				// Add new listener
				checkbox.addEventListener('change', checkboxChangeHandler);
			});
		}
	}
	
	function checkboxChangeHandler() {
		const selectedCount = document.querySelectorAll('input[name="suffers_from"]:checked').length;
		
		// Update helper text
		const helperText = document.querySelector('.allergen-helper');
		if (helperText) {
			if (selectedCount > 0) {
				helperText.innerHTML = `<i class="bi bi-check-circle-fill me-1" style="color: #20bf55;"></i>Hai selezionato ${selectedCount} ${selectedCount === 1 ? 'allergia' : 'allergie'}`;
			} else {
				helperText.innerHTML = `<i class="bi bi-info-circle me-1"></i>Seleziona una o più allergie dalla lista`;
			}
		}
		
		// Add animated effect to label
		const label = document.querySelector(`label[for="${this.id}"]`) || this.nextElementSibling;
		if (label) {
			label.classList.add('checkbox-changed');
			setTimeout(() => {
				label.classList.remove('checkbox-changed');
			}, 600);
		}
	}
	
	// Initial setup
	setupAllergenCheckboxes();
	
	// Function to handle edit button clicks
	function setupEditButtonHandler(btnSelector, targetId, callback = null) {
		const editBtn = document.querySelector(btnSelector);
		if (editBtn) {
			editBtn.addEventListener('click', function(e) {
				e.preventDefault();
				const collapseElement = document.getElementById(targetId);
				if (collapseElement) {
					const isExpanded = collapseElement.classList.contains('show');
					const collapse = bootstrap.Collapse.getInstance(collapseElement) 
						|| new bootstrap.Collapse(collapseElement, { toggle: false });
					
					if (isExpanded) {
						collapse.hide();
					} else {
						collapse.show();
						closeAllEditPanels(targetId);
						if (callback) setTimeout(callback, 100);
					}
				}
			});
		}
	}

	// Avatar edit button handler
	setupEditButtonHandler('.edit-avatar-btn', 'collapse-avatar-edit');

	// Avatar cancel button handler
	const cancelAvatarBtn = document.querySelector('.cancel-avatar-btn');
	if (cancelAvatarBtn) {
		cancelAvatarBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const collapseElement = document.getElementById('collapse-avatar-edit');
			if (collapseElement) {
				const collapse = bootstrap.Collapse.getInstance(collapseElement) || new bootstrap.Collapse(collapseElement, { toggle: false });
				collapse.hide();
				
				// Reset avatar preview to original
				setTimeout(() => {
					const propicInput = document.querySelector('input[name="propic"]');
					const avatarEditPreview = document.getElementById('avatar-edit-preview');
					const avatarDisplay = document.getElementById('avatar-display');
					
					if (avatarEditPreview && avatarDisplay) {
						avatarEditPreview.src = avatarDisplay.src;
					}
					if (propicInput) {
						propicInput.value = '';
					}
				}, 300);
			}
		});
	}

	// Avatar save button handler
	const saveAvatarBtn = document.querySelector('.save-avatar-btn');
	if (saveAvatarBtn) {
		saveAvatarBtn.addEventListener('click', function(e) {
			e.preventDefault();
			
			// Add loading state
			const loadingSpinner = document.createElement('div');
			loadingSpinner.className = 'spinner-border spinner-border-sm text-light ms-2';
			loadingSpinner.setAttribute('role', 'status');
			loadingSpinner.innerHTML = '<span class="visually-hidden">Caricamento...</span>';
			this.appendChild(loadingSpinner);
			this.disabled = true;
			
			// Add hidden field to indicate avatar update
			const sectionInput = document.createElement('input');
			sectionInput.type = 'hidden';
			sectionInput.name = 'update_section';
			sectionInput.value = 'avatar';
			const form = document.querySelector('form');
			if (form) {
				form.appendChild(sectionInput);
				form.submit();
			}
		});
	}

	// Avatar file input change handler for preview
	const avatarInput = document.querySelector('input[name="propic"]');
	if (avatarInput) {
		avatarInput.addEventListener('change', function(e) {
			const file = e.target.files[0];
			if (file) {
				const reader = new FileReader();
				reader.onload = function(e) {
					const avatarEditPreview = document.getElementById('avatar-edit-preview');
					const avatarDisplay = document.getElementById('avatar-display');
					if (avatarEditPreview) {
						avatarEditPreview.src = e.target.result;
					}
					if (avatarDisplay) {
						avatarDisplay.src = e.target.result;
					}
				};
				reader.readAsDataURL(file);
			}
		});
	}

	// Allergens edit button handler with setup callback
	setupEditButtonHandler('.edit-allergens-btn', 'collapse-allergens-edit', setupAllergenCheckboxes);

	// Password edit button handler
	setupEditButtonHandler('.edit-password-btn', 'collapse-password-edit');

	// Password cancel button handler
	const cancelPasswordBtn = document.querySelector('.cancel-password-btn');
	if (cancelPasswordBtn) {
		cancelPasswordBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const collapseElement = document.getElementById('collapse-password-edit');
			if (collapseElement) {
				const collapse = bootstrap.Collapse.getInstance(collapseElement) || new bootstrap.Collapse(collapseElement, { toggle: false });
				collapse.hide();
				
				// Reset password form fields
				setTimeout(() => {
					['old_password', 'new_password1', 'new_password2'].forEach(field => {
						const input = document.querySelector(`#id_${field}`);
						if (input) input.value = '';
					});
					
					// Remove any error messages
					document.querySelectorAll('#collapse-password-edit .invalid-feedback.d-block').forEach(el => el.remove());
				}, 300);
			}
		});
	}

	// Allergens cancel button handler
	const cancelAllergensBtn = document.querySelector('.cancel-allergens-btn');
	if (cancelAllergensBtn) {
		cancelAllergensBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const collapseElement = document.getElementById('collapse-allergens-edit');
			if (collapseElement) {
				const collapse = bootstrap.Collapse.getInstance(collapseElement) || new bootstrap.Collapse(collapseElement, { toggle: false });
				collapse.hide();
				
				// Reset allergens selection to original values
				setTimeout(() => {
					const originalAllergensElement = document.getElementById('original_allergens');
					if (originalAllergensElement) {
						const original = JSON.parse(originalAllergensElement.textContent);
						// Reset logic if needed
					}
				}, 300);
			}
		});
	}

	// Allergens save button handler (AJAX)
	const saveAllergensBtn = document.querySelector('.save-allergens-btn');
	if (saveAllergensBtn) {
		saveAllergensBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const btn = this;
			const form = document.querySelector('form');
			
			// Build FormData for AJAX
			const formData = new FormData();
			const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
			if (csrfToken) {
				formData.append('csrfmiddlewaretoken', csrfToken.value);
			}
			formData.append('update_section', 'allergens');
			
			// Get all checked allergens
			const selectedAllergens = document.querySelectorAll('input[name="suffers_from"]:checked');
			selectedAllergens.forEach(checkbox => {
				formData.append('suffers_from', checkbox.value);
			});
			
			// Clear previous error messages if any
			document.querySelectorAll('#collapse-allergens-edit .invalid-feedback.d-block').forEach(el => el.remove());
			
			// Show spinner
			btn.disabled = true;
			const spinner = document.createElement('span');
			spinner.className = 'spinner-border spinner-border-sm text-light ms-2';
			btn.appendChild(spinner);
			
			fetch(window.location.pathname, {
				method: 'POST',
				headers: {'X-Requested-With': 'XMLHttpRequest'},
				body: formData
			})
			.then(response => {
				btn.disabled = false;
				spinner.remove();
				
				if (response.ok) {
					// Success: hide collapse and show notification
					const collapseEl = document.getElementById('collapse-allergens-edit');
					const ex = bootstrap.Collapse.getInstance(collapseEl);
					if (ex) ex.hide();
					// Refresh page
					window.location.reload();
					// Show success notification
					showNotification('Allergie aggiornate con successo', 'success');
				} else {
					return response.json().then(data => {
						// Render field errors
						if (data.errors) {
							Object.entries(data.errors).forEach(([field, msgs]) => {
								const input = document.querySelector(`input[name="${field}"]`);
								if (input) {
									const errorDiv = document.createElement('div');
									errorDiv.className = 'invalid-feedback d-block';
									errorDiv.textContent = msgs[0];
									input.parentElement.appendChild(errorDiv);
								}
							});
						}
					});
				}
			})
			.catch(() => {
				btn.disabled = false;
				spinner.remove();
				showNotification('Errore di rete, riprova', 'error');
			});
		});
	}

	// Password save button handler (AJAX)
	const savePasswordBtn = document.querySelector('.save-password-btn');
	if (savePasswordBtn) {
		savePasswordBtn.addEventListener('click', function(e) {
			e.preventDefault();
			const btn = this;
			const form = document.querySelector('form');
			
			// Build FormData for AJAX
			const formData = new FormData();
			const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
			if (csrfToken) {
				formData.append('csrfmiddlewaretoken', csrfToken.value);
			}
			formData.append('update_section', 'password');
			
			['old_password','new_password1','new_password2'].forEach(field => {
				const input = document.querySelector(`#id_${field}`);
				if (input) formData.append(field, input.value);
			});
			
			// Clear previous error messages
			document.querySelectorAll('#collapse-password-edit .invalid-feedback.d-block').forEach(el => el.remove());
			
			// Show spinner
			btn.disabled = true;
			const spinner = document.createElement('span');
			spinner.className = 'spinner-border spinner-border-sm text-light ms-2';
			btn.appendChild(spinner);
			
			fetch(window.location.pathname, {
				method: 'POST',
				headers: {'X-Requested-With': 'XMLHttpRequest'},
				body: formData
			})
			.then(response => {
				btn.disabled = false;
				spinner.remove();
				if (response.ok) {
					// Success: hide collapse and show notification
					const collapseEl = document.getElementById('collapse-password-edit');
					const ex = bootstrap.Collapse.getInstance(collapseEl);
					if (ex) ex.hide();
					showNotification('Password modificata con successo', 'success');
				} else {
					return response.json().then(data => {
						// Render field errors
						const errors = data.errors;
						Object.entries(errors).forEach(([field, msgs]) => {
							const input = document.querySelector(`#id_${field}`);
							if (input) {
								const errorDiv = document.createElement('div');
								errorDiv.className = 'invalid-feedback d-block';
								errorDiv.textContent = msgs[0];
								input.parentElement.appendChild(errorDiv);
							}
						});
					});
				}
			})
			.catch(() => {
				btn.disabled = false;
				spinner.remove();
				showNotification('Errore di rete, riprova', 'error');
			});
		});
	}
	
	// Ripple effect for buttons
	document.querySelectorAll('.btn').forEach(button => {
		button.addEventListener('click', function(e) {
			const x = e.clientX - e.target.getBoundingClientRect().left;
			const y = e.clientY - e.target.getBoundingClientRect().top;
			
			const ripple = document.createElement('span');
			ripple.className = 'ripple';
			ripple.style.left = `${x}px`;
			ripple.style.top = `${y}px`;
			
			this.appendChild(ripple);
			
			setTimeout(() => {
				ripple.remove();
			}, 600);
		});
	});
	
	// Function to show notifications
	function showNotification(message, type) {
		const toast = document.createElement('div');
		toast.className = `toast align-items-center text-white bg-${type} border-0`;
		toast.setAttribute('role', 'alert');
		toast.setAttribute('aria-live', 'assertive');
		toast.setAttribute('aria-atomic', 'true');
		
		const toastContent = document.createElement('div');
		toastContent.className = 'd-flex';
		
		const toastBody = document.createElement('div');
		toastBody.className = 'toast-body';
		toastBody.textContent = message;
		
		const closeButton = document.createElement('button');
		closeButton.type = 'button';
		closeButton.className = 'btn-close btn-close-white me-2 m-auto';
		closeButton.setAttribute('data-bs-dismiss', 'toast');
		closeButton.setAttribute('aria-label', 'Close');
		
		toastContent.appendChild(toastBody);
		toastContent.appendChild(closeButton);
		toast.appendChild(toastContent);
		
		// Create toast container if it doesn't exist
		let toastContainer = document.querySelector('.toast-container');
		if (!toastContainer) {
			toastContainer = document.createElement('div');
			toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
			document.body.appendChild(toastContainer);
		}
		
		toastContainer.appendChild(toast);
		
		const bsToast = new bootstrap.Toast(toast);
		bsToast.show();
		
		// Remove toast after it's hidden
		toast.addEventListener('hidden.bs.toast', function() {
			toast.remove();
		});
	}
});
