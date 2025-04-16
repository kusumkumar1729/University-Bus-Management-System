document.addEventListener('DOMContentLoaded', function() {
    // Scroll animation logic
    const sections = document.querySelectorAll('.scroll-animation');
    const options = {
        threshold: 0.1
        
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, options);

    sections.forEach(section => {
        observer.observe(section);
    });

    // Carousel logic
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel-item');
    const totalSlides = slides.length;
    const slideInterval = 3000; // Interval time in milliseconds (3 seconds)

    function showSlide(index) {
        if (index >= totalSlides) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = totalSlides - 1;
        } else {
            currentSlide = index;
        }

        // Calculate the offset for the slide
        const offset = -currentSlide * 100;
        document.querySelector('.carousel-inner').style.transform = `translateX(${offset}%)`;
    }

    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    // Set interval for automatic slide change
    setInterval(nextSlide, slideInterval);

    // Initial display
    showSlide(currentSlide);

    // Add event listeners for manual controls
    document.querySelector('.carousel-control.next').addEventListener('click', nextSlide);
    document.querySelector('.carousel-control.prev').addEventListener('click', prevSlide);
});


  
  
  