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

    // ============================================================
    // MODAL VIP: Filtro de Servicio Exclusivo a Domicilio y WhatsApp
    // ============================================================
    let waFilterModal = document.getElementById('wa-filter-modal');
    if (!waFilterModal) {
        waFilterModal = document.createElement('div');
        waFilterModal.className = 'modal-overlay';
        waFilterModal.id = 'wa-filter-modal';
        waFilterModal.setAttribute('role', 'dialog');
        waFilterModal.setAttribute('aria-modal', 'true');
        waFilterModal.setAttribute('aria-label', 'Modalidad de Servicio Exclusivo macWave');
        waFilterModal.innerHTML = `
    <div class="wa-filter-modal-card" role="document">
      <button class="close-wa-filter-btn" id="close-wa-filter-modal" type="button" aria-label="Cerrar ventana">×</button>
      
      <span class="wa-filter-badge">
        <span>🚚</span> Servicio en Sitio y Laboratorio CDMX
      </span>
      
      <h3>¿Cómo funciona nuestro servicio técnico?</h3>
      
      <p class="wa-filter-intro">
        Para tu comodidad y máxima seguridad, <strong>no necesitas salir al tráfico ni hacer filas en locales comerciales</strong>:
      </p>
      
      <div class="wa-filter-points">
        <div class="wa-filter-item">
          <span class="point-check">✔</span>
          <div><strong>Servicio 100% a Domicilio u Oficina:</strong> Para baterías, diagnósticos y mantenimiento, el especialista acude directo a tu puerta con orden de servicio foliada.</div>
        </div>
        <div class="wa-filter-item">
          <span class="point-check">✔</span>
          <div><strong>Laboratorio Especializado:</strong> Para cortos en tarjeta lógica o Mac mojadas, realizamos recolección segura con traslado asegurado a laboratorio.</div>
        </div>
        <div class="wa-filter-item">
          <span class="point-check">✔</span>
          <div><strong>Cero Locales Públicos:</strong> Tu equipo nunca se expone en plazas de computación ni en manos de intermediarios.</div>
        </div>
      </div>
      
      <div class="wa-filter-prompt">
        📍 <strong>Para coordinar visita o recolección con especialista:</strong><br>
        Indícanos qué modelo de Mac tienes y tu colonia o alcaldía en CDMX / Área Metropolitana.
      </div>

      <div class="wa-filter-inputs">
        <div class="wa-input-group">
          <label for="wa-input-model">Modelo de tu Mac (opcional):</label>
          <input type="text" id="wa-input-model" placeholder="Ej. MacBook Pro 2020, MacBook Air M1, iMac..." autocomplete="off">
        </div>
        <div class="wa-input-group">
          <label for="wa-input-colonia">Colonia o Alcaldía (opcional):</label>
          <input type="text" id="wa-input-colonia" placeholder="Ej. Polanco, Del Valle, Coyoacán, Satélite..." autocomplete="off">
        </div>
      </div>
      
      <div class="wa-filter-actions">
        <a id="btn-wa-modal-confirm" href="https://wa.me/525535757364?text=Hola%20macWave%2C%20solicito%20servicio%20a%20domicilio%20o%20recolecci%C3%B3n%20en%20CDMX.%20Mi%20modelo%20es%3A%20...%20y%20estoy%20en%20la%20colonia%3A%20..." class="btn-wa-modal-confirm" target="_blank" rel="noopener noreferrer">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
            <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/>
          </svg>
          Continuar a WhatsApp Oficial
        </a>
        <button type="button" class="btn-wa-modal-cancel" id="cancel-wa-filter-modal">Regresar al sitio</button>
      </div>
    </div>`;
        document.body.appendChild(waFilterModal);
    }

    const closeWaFilterBtn = document.getElementById('close-wa-filter-modal');
    const cancelWaFilterBtn = document.getElementById('cancel-wa-filter-modal');
    const btnWaModalConfirm = document.getElementById('btn-wa-modal-confirm');
    const inputModel = document.getElementById('wa-input-model');
    const inputColonia = document.getElementById('wa-input-colonia');

    let currentBaseMessage = "Hola macWave, solicito servicio a domicilio o recolección técnica en CDMX.";

    function updateConfirmLink() {
        if (!btnWaModalConfirm) return;
        const model = inputModel ? inputModel.value.trim() : '';
        const colonia = inputColonia ? inputColonia.value.trim() : '';
        
        let text = currentBaseMessage;
        if (model || colonia) {
            text += ` [Modelo: ${model || 'Por confirmar'} | Colonia: ${colonia || 'Por confirmar'}]`;
        } else {
            text += ` [Modelo: ... | Colonia: ...]`;
        }
        btnWaModalConfirm.setAttribute('href', `https://wa.me/525535757364?text=${encodeURIComponent(text)}`);
    }

    if (inputModel) inputModel.addEventListener('input', updateConfirmLink);
    if (inputColonia) inputColonia.addEventListener('input', updateConfirmLink);

    function openWaFilterModal(e) {
        if (e) {
            e.preventDefault();
            const sourceLink = e.currentTarget || e.target.closest('a');
            if (sourceLink) {
                const originalHref = sourceLink.getAttribute('href');
                if (originalHref && originalHref.includes('wa.me')) {
                    if (originalHref.includes('text=')) {
                        currentBaseMessage = decodeURIComponent(originalHref.split('text=')[1]);
                    } else {
                        currentBaseMessage = "Hola macWave, solicito servicio a domicilio o recolección técnica en CDMX.";
                    }
                }
            }
        }
        updateConfirmLink();
        if (!waFilterModal) return;
        waFilterModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeWaFilterModal() {
        if (!waFilterModal) return;
        waFilterModal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Interceptar todos los enlaces a WhatsApp excepto el botón del modal
    document.addEventListener('click', (e) => {
        const waAnchor = e.target.closest('a[href*="wa.me/525535757364"]');
        if (waAnchor && !waAnchor.closest('#wa-filter-modal')) {
            openWaFilterModal(e);
        }
    });

    if (closeWaFilterBtn) closeWaFilterBtn.addEventListener('click', closeWaFilterModal);
    if (cancelWaFilterBtn) cancelWaFilterBtn.addEventListener('click', closeWaFilterModal);
    if (btnWaModalConfirm) {
        btnWaModalConfirm.addEventListener('click', () => {
            setTimeout(closeWaFilterModal, 300);
        });
    }

    if (waFilterModal) {
        waFilterModal.addEventListener('click', (e) => {
            if (e.target === waFilterModal) closeWaFilterModal();
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && waFilterModal && waFilterModal.classList.contains('active')) {
            closeWaFilterModal();
        }
    });

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
