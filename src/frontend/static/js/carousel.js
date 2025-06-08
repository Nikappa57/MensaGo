document.addEventListener('DOMContentLoaded', function() {
	// Add hover effects for event cards
	const eventCards = document.querySelectorAll('.events-card');
	eventCards.forEach(card => {
		card.addEventListener('mouseenter', function() {
			const dateElement = this.querySelector('.event-date');
			
			if (dateElement) {
				dateElement.style.transform = 'translateY(-5px)';
			}
		});
		
		card.addEventListener('mouseleave', function() {
			const dateElement = this.querySelector('.event-date');
			
			if (dateElement) {
				dateElement.style.transform = 'translateY(0)';
			}
		});
	});
	
	// Initialize the events slider
	initEventsSlider();
	
	const carousels = document.querySelectorAll('.carousel');
	carousels.forEach(carousel => {
		if (carousel.id !== 'eventsCarousel') {
			new bootstrap.Carousel(carousel, {
				interval: 6000,
				wrap: true,
				pause: 'hover',
				keyboard: true
			});
		}
	});
});

function initEventsSlider() {
	const slider = document.querySelector('.events-slider');
	if (!slider) return;
	
	const slides = document.querySelectorAll('.event-slide');
	const prevBtn = document.querySelector('.events-prev-btn');
	const nextBtn = document.querySelector('.events-next-btn');
	
	if (slides.length === 0) return;
	
	// Set initial state
	let currentPosition = 0;
	let slidesToShow = getSlidesToShow();
	let autoScrollTimer = null;
	let isHovered = false;
	
	// Resize handler
	function handleResize() {
		slidesToShow = getSlidesToShow();
		// Ensure currentPosition is valid for the new screen size
		if (currentPosition > slides.length - slidesToShow) {
			currentPosition = Math.max(0, slides.length - slidesToShow);
		}
		adjustSlideWidths();
		positionSlides(currentPosition);
		updateButtonVisibility();
	}
	
	// Get number of slides to show based on viewport
	function getSlidesToShow() {
		if (window.innerWidth >= 992) {
			return 3; // desktop - 3 cards per view
		} else if (window.innerWidth >= 768) {
			return 2; // tablet - 2 cards per view
		} else {
			return 1; // mobile - 1 card per view
		}
	}

	// Adjust slide widths based on slidesToShow and gap
	function adjustSlideWidths() {
		const containerWidth = slider.parentElement.offsetWidth;
		const gapSize = 20;
		const totalGapWidth = gapSize * (slidesToShow);
		const slideWidth = (containerWidth - totalGapWidth) / slidesToShow;

		slides.forEach(slide => {
			slide.style.width = `${slideWidth}px`;
			slide.style.flex = `0 0 ${slideWidth}px`;
		});
	}
	
	// Position slides for current view
	function positionSlides(position, noTransition = false) {
		if (slides.length === 0) return;

		const slide = slides[0];
		const slideWidth = slide.offsetWidth;
		const gapSize = 20;

		const offset = position * (slideWidth + gapSize);
		
		if (noTransition) {
			// Temporarily disable transition for instant moves
			slider.style.transition = 'none';
			slider.style.transform = `translateX(-${offset}px)`;
			// Force reflow to ensure the transition is disabled
			slider.offsetHeight;
			// Re-enable transition
			setTimeout(() => {
				slider.style.transition = 'transform 0.5s ease-in-out';
			}, 50);
		} else {
			slider.style.transition = 'transform 0.5s ease-in-out';
			slider.style.transform = `translateX(-${offset}px)`;
		}
		
		// Highlight current slides
		slides.forEach((slide, index) => {
			if (index >= position && index < position + slidesToShow) {
				slide.classList.add('active-slide');
			} else {
				slide.classList.remove('active-slide');
			}
		});
	}

	// Update buttons visibility based on current position
	function updateButtonVisibility() {
		if (currentPosition <= 0) {
			prevBtn.classList.add('disabled');
		} else {
			prevBtn.classList.remove('disabled');
		}
		
		if (currentPosition >= slides.length - slidesToShow) {
			nextBtn.classList.add('disabled');
		} else {
			nextBtn.classList.remove('disabled');
		}
	}

	// Event listeners for buttons
	nextBtn.addEventListener('click', () => {
		if (currentPosition < slides.length - slidesToShow) {
			currentPosition++;
			positionSlides(currentPosition);
			updateButtonVisibility();
		}
	});
	
	prevBtn.addEventListener('click', () => {
		if (currentPosition > 0) {
			currentPosition--;
			positionSlides(currentPosition);
			updateButtonVisibility();
		}
	});

	// Auto scroll function
	function startAutoScroll() {
		if (autoScrollTimer) clearInterval(autoScrollTimer);

		autoScrollTimer = setInterval(() => {
			if (!isHovered && currentPosition < slides.length - slidesToShow) {
				currentPosition++;
				positionSlides(currentPosition);
				updateButtonVisibility();
			} else if (!isHovered && currentPosition >= slides.length - slidesToShow) {
				currentPosition = 0;
				positionSlides(currentPosition, true);
				updateButtonVisibility();
			}
		}, 5000); // Scroll every 5 seconds
	}
	
	// Pause auto scroll on hover
	const sliderContainer = slider.parentElement.parentElement;
	
	sliderContainer.addEventListener('mouseenter', () => {
		isHovered = true;
	});
	
	sliderContainer.addEventListener('mouseleave', () => {
		isHovered = false;
	});
	
	// Stop auto scroll when user interacts with navigation buttons
	prevBtn.addEventListener('click', () => {
		if (autoScrollTimer) clearInterval(autoScrollTimer);
	});
	
	nextBtn.addEventListener('click', () => {
		if (autoScrollTimer) clearInterval(autoScrollTimer);
	});

	// Initialize slider
	window.addEventListener('resize', handleResize);
	handleResize();
	startAutoScroll();