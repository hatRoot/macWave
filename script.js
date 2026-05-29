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
                const header = document.querySelector('.main-header');
                const headerHeight = header ? header.offsetHeight : 0;

                window.scrollTo({
                    top: targetElement.offsetTop - headerHeight - 20,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dynamic Header (Fixed positioning & Shrink on scroll)
    const header = document.querySelector('.main-header');
    const ticker = document.querySelector('.emergency-ticker');
    
    if (header) {
        let tickerHeight = ticker ? ticker.offsetHeight : 0;
        let headerHeight = header.offsetHeight;
        
        // Dynamic padding to avoid content jumping
        document.body.style.paddingTop = `${tickerHeight + headerHeight}px`;
        document.documentElement.style.scrollPaddingTop = `${tickerHeight + headerHeight}px`;

        let lastKnownScrollPosition = 0;
        let ticking = false;

        const handleHeaderScroll = (scrollPos) => {
            const threshold = 80;
            tickerHeight = ticker ? ticker.offsetHeight : 0;
            const tickerThreshold = tickerHeight;
            
            // Handle Ticker & Header Position
            if (scrollPos > tickerThreshold) {
                header.style.top = '0px';
                if (ticker) ticker.style.transform = `translateY(-${tickerHeight}px)`;
            } else {
                header.style.top = `${tickerHeight - scrollPos}px`;
                if (ticker) ticker.style.transform = `translateY(-${scrollPos}px)`;
            }

            // Handle Shrink Effect
            if (scrollPos > threshold && !header.classList.contains('header-scrolled')) {
                header.classList.add('header-scrolled');
                // Optional: update padding if shrink is very significant
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
             document.body.style.paddingTop = `${tickerHeight + headerHeight}px`;
             document.documentElement.style.scrollPaddingTop = `${tickerHeight + headerHeight}px`;
             handleHeaderScroll(window.scrollY);
        });
    }

    // Modal Logic
    const modal = document.getElementById('scheduling-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const durationBtns = document.querySelectorAll('.duration-btn');

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
});
