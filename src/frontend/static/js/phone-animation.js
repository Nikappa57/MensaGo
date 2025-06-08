document.addEventListener('DOMContentLoaded', function() {
	const phoneFrames = document.querySelectorAll('.phone-frame');
	const tutorialSection = document.querySelector('.step-box').closest('.container');
	const isHoverSupported = window.matchMedia('(hover: hover)').matches;
	if (isHoverSupported && window.innerWidth >= 992 && tutorialSection) {
		let containerRect = null;
		let isMouseOverContainer = false;
		tutorialSection.addEventListener('mousemove', function(e) {
			if (!containerRect) {
			containerRect = tutorialSection.getBoundingClientRect();
			}
			const centerX = containerRect.left + containerRect.width / 2;
			const centerY = containerRect.top + containerRect.height / 2;
			const distanceX = (e.clientX - centerX) / (containerRect.width / 2);
			const distanceY = (e.clientY - centerY) / (containerRect.height / 2);
			
			phoneFrames.forEach(phone => {
			const tiltX = -distanceY * 10; 
			const tiltY = distanceX * 15;
			
			let transform = 'translateY(-15px)';
			
			if (phone.classList.contains('phone-left')) {
				transform += ` rotate3d(1, 0, 0, ${5 + tiltX}deg) rotate3d(0, 1, 0, ${15 + tiltY}deg)`;
			} else if (phone.classList.contains('phone-center')) {
				transform += ` rotate3d(1, 0, 0, ${5 + tiltX}deg) rotate3d(0, 1, 0, ${tiltY}deg)`;
			} else if (phone.classList.contains('phone-right')) {
				transform += ` rotate3d(1, 0, 0, ${5 + tiltX}deg) rotate3d(0, 1, 0, ${-15 + tiltY}deg)`;
			}
			
			phone.style.transform = transform;
			
			const shadowX = tiltY * -2;
			const shadowY = tiltX * 2;
			phone.style.boxShadow = `${shadowX}px ${15 + shadowY}px 30px rgba(0,0,0,0.2)`;
			});
	});
	
	tutorialSection.addEventListener('mouseenter', function() {
		isMouseOverContainer = true;
		phoneFrames.forEach(phone => {
		let baseTransform = 'translateY(-15px)';
		if (phone.classList.contains('phone-left')) {
			baseTransform += ' rotate3d(0, 1, 0, 15deg) rotate3d(1, 0, 0, 5deg)';
		} else if (phone.classList.contains('phone-center')) {
			baseTransform += ' rotate3d(1, 0, 0, 5deg)';
		} else if (phone.classList.contains('phone-right')) {
			baseTransform += ' rotate3d(0, 1, 0, -15deg) rotate3d(1, 0, 0, 5deg)';
		}
		phone.style.transform = baseTransform;
		phone.style.boxShadow = '0 15px 30px rgba(0,0,0,0.2)';
		});
	});
	
	tutorialSection.addEventListener('mouseleave', function() {
		isMouseOverContainer = false;
		containerRect = null; 
		
		phoneFrames.forEach(phone => {
		if (phone.classList.contains('phone-left')) {
			phone.style.transform = 'rotate3d(0, 1, 0, 15deg) rotate3d(1, 0, 0, 5deg)';
		} else if (phone.classList.contains('phone-center')) {
			phone.style.transform = 'rotate3d(1, 0, 0, 5deg)';
		} else if (phone.classList.contains('phone-right')) {
			phone.style.transform = 'rotate3d(0, 1, 0, -15deg) rotate3d(1, 0, 0, 5deg)';
		}
		phone.style.boxShadow = '';
		});
	});
	
	window.addEventListener('resize', function() {
		containerRect = null;
		
		if (window.innerWidth < 992) {
		phoneFrames.forEach(phone => {
			phone.style.transform = '';
			phone.style.boxShadow = '';
		});
		}
	});
	}
});
