document.addEventListener('DOMContentLoaded', () => {
    // Clean Navigation Handler (Prevents URL preview on hover)
    document.querySelectorAll('[data-link]').forEach(el => {
        el.style.cursor = 'pointer';
        el.addEventListener('click', (e) => {
            e.preventDefault();
            const url = el.getAttribute('data-link');
            if (url && url !== '#') {
                window.location.href = url;
            }
        });
    });

    // Mobile Menu Link Handling (Closes menu on click)
    document.querySelectorAll('.nav-link, [data-link]').forEach(link => {
        link.addEventListener('click', () => {
            document.body.classList.remove('menu-active');
            const btn = document.getElementById('mobile-menu-toggle');
            if (btn) btn.classList.remove('active');
        });
    });

    // Smooth scroll for all internal links
    document.querySelectorAll('a[href^="#"], [data-scroll]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href') || this.getAttribute('data-scroll');
            if (!targetId || targetId === '#' || targetId.startsWith('javascript')) return;

            e.preventDefault();
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const header = document.querySelector('.main-header, .cloned-header');
                const headerHeight = header ? header.offsetHeight : 0;

                window.scrollTo({
                    top: targetElement.offsetTop - headerHeight - 20,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dynamic Header (Fixed positioning & Shrink on scroll)
    const header = document.querySelector('.main-header, .cloned-header');
    const ticker = document.querySelector('.emergency-ticker');
    
    if (header) {
        let tickerHeight = ticker ? ticker.offsetHeight : 0;
        let headerHeight = header.offsetHeight;
        
        // Dynamic padding to avoid content jumping
        const isFixedHeader = header.classList.contains('main-header');
        if (isFixedHeader) {
            document.body.style.paddingTop = `${tickerHeight + headerHeight}px`;
            document.documentElement.style.scrollPaddingTop = `${tickerHeight + headerHeight}px`;
        } else {
            document.body.style.paddingTop = '0px';
            document.documentElement.style.scrollPaddingTop = `${headerHeight}px`;
        }

        let lastKnownScrollPosition = 0;
        let ticking = false;

        const handleHeaderScroll = (scrollPos) => {
            const threshold = 80;
            const isClonedHeader = header.classList.contains('cloned-header');
            tickerHeight = ticker ? ticker.offsetHeight : 0;
            const tickerThreshold = tickerHeight;

            // Ticker sync solo aplica al header oscuro fijo (main-header), no al menú clonado
            if (!isClonedHeader && ticker) {
                if (scrollPos > tickerThreshold) {
                    header.style.top = '0px';
                    ticker.style.transform = `translateY(-${tickerHeight}px)`;
                } else {
                    header.style.top = `${tickerHeight - scrollPos}px`;
                    ticker.style.transform = `translateY(-${scrollPos}px)`;
                }
            } else if (isClonedHeader) {
                header.style.top = '';
            }

            // Handle Shrink Effect
            if (scrollPos > threshold && !header.classList.contains('header-scrolled')) {
                header.classList.add('header-scrolled');
            } else if (scrollPos <= threshold && header.classList.contains('header-scrolled')) {
                header.classList.remove('header-scrolled');
            }
        };

        window.addEventListener('scroll', () => {
            lastKnownScrollPosition = window.scrollY;
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    handleHeaderScroll(lastKnownScrollPosition);
                    ticking = false;
                });
                ticking = true;
            }
        });
        
        // Initial check
        handleHeaderScroll(window.scrollY);

        // Re-calculate on resize
        window.addEventListener('resize', () => {
             tickerHeight = ticker ? ticker.offsetHeight : 0;
             headerHeight = header.offsetHeight;
             if (isFixedHeader) {
                 document.body.style.paddingTop = `${tickerHeight + headerHeight}px`;
                 document.documentElement.style.scrollPaddingTop = `${tickerHeight + headerHeight}px`;
             } else {
                 document.body.style.paddingTop = '0px';
                 document.documentElement.style.scrollPaddingTop = `${headerHeight}px`;
             }
             handleHeaderScroll(window.scrollY);
        });
    }

    // Modal Logic
    const modal = document.getElementById('scheduling-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const durationBtns = document.querySelectorAll('.duration-btn');

    // ============================================================
    // MODAL: Lista de Servicios (Imagen)
    // ============================================================
    const servicesListBtn = document.getElementById('services-list-btn');
    const servicesListModal = document.getElementById('services-list-modal');
    const closeServicesListModalBtn = document.getElementById('close-services-list-modal');

    function openServicesListModal(e) {
        if (e) e.preventDefault();
        if (!servicesListModal) return;
        servicesListModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeServicesListModal() {
        if (!servicesListModal) return;
        servicesListModal.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (servicesListBtn) {
        servicesListBtn.addEventListener('click', openServicesListModal);
        servicesListBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') openServicesListModal(e);
        });
    }

    if (closeServicesListModalBtn) {
        closeServicesListModalBtn.addEventListener('click', closeServicesListModal);
    }

    if (servicesListModal) {
        servicesListModal.addEventListener('click', (e) => {
            if (e.target === servicesListModal) closeServicesListModal();
        });
    }

    // Helper to open modal
    function openModal(e) {
        e.preventDefault();
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        }
    }

    // Helper to close modal
    function closeModal() {
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // Attach event listeners to specific buttons
    const contactButtons = document.querySelectorAll('.cta-button.secondary, .large-cta');
    contactButtons.forEach(btn => {
        btn.addEventListener('click', openModal);
    });

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    // Close on click outside
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    // ESC cierra ambos modales si están abiertos
    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        if (servicesListModal && servicesListModal.classList.contains('active')) closeServicesListModal();
        if (modal && modal.classList.contains('active')) closeModal();
    });

    // Duration Selection Logic
    durationBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            durationBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked
            btn.classList.add('active');
        });
    });

    // Calendar Logic
    const calendarGrid = document.querySelector('.calendar-grid');
    const currentMonthSpan = document.querySelector('.current-month');
    const prevMonthBtn = document.querySelector('.calendar-nav-btn:first-child');
    const nextMonthBtn = document.querySelector('.calendar-nav-btn:last-child');
    const nextMonthLink = document.querySelector('.next-month-link');
    const calendarAlert = document.querySelector('.calendar-alert');

    // Let's use the current date to show availability from today
    let displayDate = new Date();

    const monthNames = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];

    function renderCalendar(date) {
        const year = date.getFullYear();
        const month = date.getMonth();

        // Update Header
        currentMonthSpan.textContent = `${monthNames[month]} ${year}`;

        // Clear existing days (keep headers)
        // We need to keep the first 7 divs (headers)
        if (!calendarGrid) return;
        const headers = Array.from(calendarGrid.children).slice(0, 7);
        calendarGrid.innerHTML = '';
        headers.forEach(header => calendarGrid.appendChild(header));

        // Get first day of month and days in month
        const firstDay = new Date(year, month, 1).getDay(); // 0 = Sunday, 1 = Monday...
        // Adjust for Monday start (Monday=0, Sunday=6)
        const adjustedFirstDay = (firstDay === 0 ? 6 : firstDay - 1);

        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Empty cells for days before start
        for (let i = 0; i < adjustedFirstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.classList.add('calendar-day', 'empty');
            calendarGrid.appendChild(emptyCell);
        }

        // Days
        for (let i = 1; i <= daysInMonth; i++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('calendar-day');
            dayCell.textContent = i;

            const dayOfWeek = new Date(year, month, i).getDay();
            if (dayOfWeek === 0) {
                dayCell.classList.add('disabled');
            } else {
                dayCell.addEventListener('click', () => {
                    document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
                    dayCell.classList.add('selected');

                    const selectedDateText = document.getElementById('selected-date-text');
                    const confirmContainer = document.getElementById('booking-confirmation-container');
                    const noSelectionMsg = document.getElementById('no-selection-message');
                    const whatsappBtn = document.getElementById('confirm-whatsapp-btn');

                    if (selectedDateText && confirmContainer && noSelectionMsg && whatsappBtn) {
                        const dateString = `${i} de ${monthNames[month]} ${year}`;
                        selectedDateText.textContent = dateString;
                        confirmContainer.style.display = 'block';
                        noSelectionMsg.style.display = 'none';

                        const message = `Hola me ayudas a reparar mi Mac?`;
                        whatsappBtn.href = `https://wa.me/525535757364?text=${encodeURIComponent(message)}`;
                    }

                    if (calendarAlert) calendarAlert.style.display = 'none';
                });
            }

            calendarGrid.appendChild(dayCell);
        }

        const today = new Date();
        if (date < new Date(today.getFullYear(), today.getMonth(), 1)) {
            if (calendarAlert) {
                calendarAlert.style.display = 'block';
                calendarAlert.querySelector('p').innerHTML = `<strong>No hay fechas disponibles en ${monthNames[month]}</strong>`;
            }
        } else {
            if (calendarAlert) calendarAlert.style.display = 'none';
        }
    }

    // Initial Render
    if (calendarGrid) renderCalendar(displayDate);

    // Event Listeners
    if (prevMonthBtn) prevMonthBtn.addEventListener('click', () => {
        displayDate.setMonth(displayDate.getMonth() - 1);
        renderCalendar(displayDate);
    });

    if (nextMonthBtn) nextMonthBtn.addEventListener('click', () => {
        displayDate.setMonth(displayDate.getMonth() + 1);
        renderCalendar(displayDate);
    });

    if (nextMonthLink) {
        nextMonthLink.addEventListener('click', (e) => {
            e.preventDefault();
            displayDate.setMonth(displayDate.getMonth() + 1);
            renderCalendar(displayDate);
        });
    }

    // ==========================================================
    // CLONED HOME PAGE IMAGE SLIDER LOGIC (ACSP HIGH FIDELITY)
    // ==========================================================
    const slides = document.querySelectorAll('.cloned-slide');
    const dots = document.querySelectorAll('.cloned-slider-dot');
    const prevBtn = document.getElementById('slider-prev-btn');
    const nextBtn = document.getElementById('slider-next-btn');

    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval = null;

        function showSlide(index) {
            // Remove active class from current slide and dot
            slides[currentSlide].classList.remove('active');
            if (dots[currentSlide]) {
                dots[currentSlide].classList.remove('active');
            }

            // Set new current slide
            currentSlide = index;

            // Handle wrap-around bounds
            if (currentSlide >= slides.length) {
                currentSlide = 0;
            }
            if (currentSlide < 0) {
                currentSlide = slides.length - 1;
            }

            // Add active class to new slide and dot
            slides[currentSlide].classList.add('active');
            if (dots[currentSlide]) {
                dots[currentSlide].classList.add('active');
            }
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function prevSlide() {
            showSlide(currentSlide - 1);
        }

        function startAutoplay() {
            stopAutoplay();
            slideInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoplay() {
            if (slideInterval) {
                clearInterval(slideInterval);
                slideInterval = null;
            }
        }

        // Attach Event Listeners to Arrows
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                prevSlide();
                startAutoplay(); // Reset autoplay timer on interaction
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                nextSlide();
                startAutoplay(); // Reset autoplay timer on interaction
            });
        }

        // Attach Event Listeners to Indicator Dots
        dots.forEach((dot, idx) => {
            dot.addEventListener('click', (e) => {
                e.preventDefault();
                showSlide(idx);
                startAutoplay(); // Reset autoplay timer on interaction
            });
        });

        // Start slide rotation
        startAutoplay();

        // ============================================================
        // LIGHTBOX — abre imagen al hacer clic en el slider
        // ============================================================
        const lightbox        = document.getElementById('sliderLightbox');
        const lightboxImg     = document.getElementById('lightboxImg');
        const lightboxClose   = document.getElementById('lightboxClose');
        const lightboxPrev    = document.getElementById('lightboxPrev');
        const lightboxNext    = document.getElementById('lightboxNext');
        const lightboxCounter = document.getElementById('lightboxCounter');

        // Collect image sources from slides
        const slideImages = Array.from(slides).map(s => {
            const img = s.querySelector('img');
            return { src: img ? img.src : '', alt: img ? img.alt : '' };
        });

        function openLightbox(index) {
            if (!lightbox) return;
            const total = slideImages.length;
            const safeIdx = ((index % total) + total) % total;
            lightboxImg.src = slideImages[safeIdx].src;
            lightboxImg.alt = slideImages[safeIdx].alt;
            if (lightboxCounter) lightboxCounter.textContent = `${safeIdx + 1} / ${total}`;
            lightbox._currentIdx = safeIdx;
            lightbox.classList.add('open');
            document.body.style.overflow = 'hidden';
            stopAutoplay();
        }

        function closeLightbox() {
            if (!lightbox) return;
            lightbox.classList.remove('open');
            document.body.style.overflow = '';
            startAutoplay();
        }

        function lightboxGoTo(delta) {
            openLightbox((lightbox._currentIdx || 0) + delta);
        }

        // Click on slider to open lightbox
        const sliderRight = document.querySelector('.cloned-slider-right');
        if (sliderRight) {
            sliderRight.addEventListener('click', () => openLightbox(currentSlide));
        }

        if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);

        if (lightboxPrev) lightboxPrev.addEventListener('click', (e) => {
            e.stopPropagation();
            lightboxGoTo(-1);
        });

        if (lightboxNext) lightboxNext.addEventListener('click', (e) => {
            e.stopPropagation();
            lightboxGoTo(1);
        });

        // Close on backdrop click
        if (lightbox) {
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) closeLightbox();
            });
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!lightbox || !lightbox.classList.contains('open')) return;
            if (e.key === 'Escape')      closeLightbox();
            if (e.key === 'ArrowLeft')   lightboxGoTo(-1);
            if (e.key === 'ArrowRight')  lightboxGoTo(1);
        });
    }
});
