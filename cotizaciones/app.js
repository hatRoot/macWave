// Logos are now loaded from logo_const.js as LOGO_0_BASE64 and LOGO_10_BASE64

// Ticket Generator Logic
const showWorkshopTicket = () => {
    const modal = document.getElementById('ticket-modal');
    const folioDisplay = document.getElementById('ticket-folio-display');

    // Get/Init counter
    let counter = parseInt(localStorage.getItem('workshop_ticket_counter') || '239');

    // Format Date: YYMMDD
    const now = new Date();
    const dateStr = now.getFullYear().toString().slice(2) +
        (now.getMonth() + 1).toString().padStart(2, '0') +
        now.getDate().toString().padStart(2, '0');

    const folio = `G-${dateStr}-${counter}`;
    folioDisplay.textContent = folio;

    modal.style.display = 'flex';
};

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('generate-ticket-btn')?.addEventListener('click', showWorkshopTicket);

    // --- Folio Auto-Increment Logic ---
    const getNextFolio = (increment = false) => {
        let lastNum = parseInt(localStorage.getItem('quote_folio_counter') || '9199');
        if (increment) {
            lastNum++;
            localStorage.setItem('quote_folio_counter', lastNum);
        }
        return `RPC-${lastNum}`;
    };

    // Initialize folio in input if empty
    const quoteNumInput = document.getElementById('quote-number');
    if (quoteNumInput && !quoteNumInput.value) {
        quoteNumInput.value = getNextFolio();
    }
    // --- End Folio Logic ---

    document.getElementById('close-ticket-modal')?.addEventListener('click', () => {
        document.getElementById('ticket-modal').style.display = 'none';
    });

    document.getElementById('send-ticket-whatsapp')?.addEventListener('click', () => {
        const name = document.getElementById('ticket-client-name').value || 'Cliente';
        const folio = document.getElementById('ticket-folio-display').textContent;
        const sourceVal = document.getElementById('ticket-source')?.value || '';
        const ticketDate = document.getElementById('ticket-date')?.value || '';

        const badgeUrl = `../ticket-badge.html?name=${encodeURIComponent(name)}&folio=${encodeURIComponent(folio)}&source=${encodeURIComponent(sourceVal)}&date=${encodeURIComponent(ticketDate)}`;
        window.open(badgeUrl, '_blank');

        // Increment and close
        let counter = parseInt(localStorage.getItem('workshop_ticket_counter') || '239');
        localStorage.setItem('workshop_ticket_counter', counter + 1);
        document.getElementById('ticket-modal').style.display = 'none';
    });

    const form = document.getElementById('quote-form');
    const itemsContainer = document.getElementById('items-container');
    const addItemBtn = document.getElementById('add-item-btn');
    const previewCanvas = document.getElementById('pdf-preview-canvas');

    // Set default date to today
    document.getElementById('quote-date').valueAsDate = new Date();

    // Default Items
    const defaultItems = [
        { desc: 'Display generico iPhone 16 Pro Max', price: 7434.72, qty: 1 },
        { desc: 'Servicio Tecnico de iPhone', price: 1300.00, qty: 1 }
    ];

    function createItemRow(item = { desc: '', price: '', qty: 1 }) {
        const row = document.createElement('div');
        row.className = 'item-row';
        row.innerHTML = `
            <input type="text" class="item-desc" placeholder="Descripción" value="${item.desc}">
            <input type="number" class="item-price" placeholder="Precio" value="${item.price}" step="0.01">
            <input type="number" class="item-qty" placeholder="Cant." value="${item.qty}" min="1" step="0.01">
            <button type="button" class="remove-btn">✕</button>
        `;

        row.querySelector('.remove-btn').addEventListener('click', () => {
            row.remove();
            updatePreview();
        });

        // Add event listeners for live preview update
        row.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', updatePreview);
        });

        itemsContainer.appendChild(row);
        updatePreview();
    }

    // Add default items
    defaultItems.forEach(item => createItemRow(item));

    addItemBtn.addEventListener('click', () => createItemRow());

    // Update preview on any input change
    form.querySelectorAll('input, select').forEach(input => {
        if (!input.closest('.item-row')) {
            input.addEventListener('input', updatePreview);
        }
    });

    function calculateTotals() {
        let total = 0;
        const items = [];
        document.querySelectorAll('.item-row').forEach(row => {
            const desc = row.querySelector('.item-desc').value;
            const price = parseFloat(row.querySelector('.item-price').value) || 0;
            const qty = parseInt(row.querySelector('.item-qty').value) || 0;
            const subtotal = price * qty;
            total += subtotal;
            items.push({ desc, price, qty, subtotal });
        });
        return { items, total };
    }

    function updatePreview() {
        const { items, total } = calculateTotals();
        const client = document.getElementById('client-name').value || 'Erik';
        const project = document.getElementById('project-name').value || 'Reparacion iPhone 16 Pro Max';
        const tech = document.getElementById('tech-name').value;
        const date = document.getElementById('quote-date').value;
        const qNumber = document.getElementById('quote-number').value || getNextFolio();
        const currency = document.getElementById('currency').value;

        const qrUrl = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://macwave.com.mx";

        previewCanvas.innerHTML = `
            <div class="mock-pdf-content">
                <div class="mock-header">
                    <div class="mock-logo-section" style="display: flex; gap: 10px; align-items: center;">
                        <img src="${LOGO_0_BASE64}" alt="Logo 0" style="width: 55px; height: auto;">
                        <img src="${LOGO_10_BASE64}" alt="Logo 10" style="width: 55px; height: auto;">
                    </div>
                    <div class="mock-header-text" style="flex-grow: 1; text-align: center;">
                        <strong style="font-size: 18px;">Laboratorio de reparación de computadoras Apple</strong><br>
                        <span style="color: #888; font-size: 12px;">Apple Certified Device Support 2025</span>
                    </div>
                    <div class="mock-meta">
                        <span style="color: red; font-size: 16px; font-weight: bold; font-style: italic;">Cotización N° ${qNumber}</span><br>
                        <div style="margin-top: 10px; font-size: 11px; color: #555; text-align: right;">
                            Fecha: ............................ <strong>${date}</strong><br>
                            Tecnico: <span style="text-decoration: underline;">${tech}</span><br>
                            Moneda: ............ <strong>${currency}</strong>
                        </div>
                    </div>
                </div>



                <div style="margin-bottom: 25px; font-size: 13px;">
                    <span style="color: blue; font-weight: bold;">Estimado(a) Sr:</span> <span style="color: #666;"> ${client}</span><br>
                    <span style="color: blue; font-weight: bold;">Oportunidad / Proyecto:</span> <span style="color: #666;"> ${project}</span>
                </div>

                <table class="mock-table" style="width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 20px;">
                <thead>
                    <tr>
                        <th style="background: black; color: white; padding: 10px; border-radius: 8px 0 0 8px; text-align: center;">DESCRIPCION DEL SERVICIO O PRODUCTO</th>
                        <th style="background: black; color: white; padding: 10px; width: 110px; text-align: center;">PRECIO UNTARIO</th>
                        <th style="background: black; color: white; padding: 10px; width: 60px; text-align: center;">UNIDAD</th>
                        <th style="background: black; color: white; padding: 10px; width: 110px; border-radius: 0 8px 8px 0; text-align: center;">SUB TOTAL</th>
                    </tr>
                </thead>
                <tbody class="apple-zebra">
                    ${items.map((item, index) => `
                        <tr style="background-color: ${index % 2 === 0 ? '#ffffff' : '#f5f5f7'};">
                            <td style="color: red; font-weight: 500; padding: 8px; border-bottom: 1px solid #eee;">${item.desc}</td>
                            <td style="color: red; text-align: right; font-weight: bold; padding: 8px; border-bottom: 1px solid #eee;">$ ${item.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                            <td style="color: red; text-align: center; padding: 8px; border-bottom: 1px solid #eee;">${item.qty}</td>
                            <td style="color: red; text-align: right; font-weight: bold; padding: 8px; border-bottom: 1px solid #eee;">$ ${item.subtotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>

                <div class="mock-total" style="border-top: 1px solid #ddd; padding-top: 10px; margin-top: 20px;">
                    <span style="color: red; font-weight: bold;">TOTAL</span> 
                    <span style="color: red; font-weight: bold; margin-left: 50px;">$ ${total.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                </div>

                <div class="mock-terms" style="margin-top: 30px; font-size: 8px; color: #006680; font-weight: 600; text-align: left;">
                    <p style="margin-bottom: 4px;">Vigencia de la cotización: 1 día, expira el día ${new Date(new Date(date).getTime() + 86400000).toLocaleDateString()}</p>
                    <p style="margin-bottom: 4px;">Garantía: 31 días en el servicio técnico, pregunta por tu garantía extendida a 100 días POR UN COSTO ADICIONAL. Condiciones: SE REQUIERE</p>
                    <p style="margin-bottom: 4px; font-weight: 800; font-size: 9.5px;">PAGO ANTICIPADO DEL 100% PARA EL SERVICIO.</p>
                    <p style="margin-bottom: 4px;">Tiempo de Entrega: Noviembre de 2025 ENTREGA TENTATIVA POR PARTE DEL FABRICANTE, modelos sugeridos a disponibilidad del fabricante.</p>
                    <p style="margin-bottom: 4px;">ALGUNOS PRODUCTOS IMPORTADOS DE ESTADOS UNIDOS, AMERICAN PARTNER.</p>
                </div>

                <div class="mock-bank" style="margin-top: 25px; font-size: 10px; color: #004d60; border-top: 1px solid #ddd; padding-top: 15px; text-align: left;">
                    <div style="margin-bottom: 8px;">
                        <strong>PAGAR A ESTE BANCO</strong><br>
                        <strong style="color: #004481; font-size: 14px;">BBVA</strong>
                    </div>
                    CUENTA CLABE : <strong>${document.getElementById('clabe').value}</strong><br>
                    NÚMERO DE CUENTA : <strong>${document.getElementById('account-number').value}</strong><br>
                    NÚMERO DE TARJETA BBVA : <strong>${document.getElementById('card-number').value}</strong>
                </div>

                <div class="mock-legal-disclaimer" style="margin-top: 25px; font-size: 7px; line-height: 1.2; border-top: 1px solid #ddd; padding-top: 15px; text-align: left;">
                    <p style="font-weight: bold; margin-bottom: 8px;">***Precios sujetos a cambios sin previo aviso, en variación al dólar americano o disponibilidad en el mercado de Asia.</p>
                    <p style="font-weight: bold; margin-bottom: 12px;">*El servicio incluye mantenimiento y resolución de problemas en el sistema, instalación de hardware y sistema operativo, migración o instalación de software con licencia adquirida.</p>
                    <p style="font-size: 6px;">AVISO: EQUIPOS CON ABANDONO CON MÁS DE 30 DÍAS NATURALES A PARTIR DEL DÍA QUE SE DEJÓ EL EQUIPO SERÁN DESTRUIDOS SIN GENERAR NINGÚN TIPO DE RESPONSABILIDAD A RECOVERY PRO Y SU EQUIPO. USTED ACEPTA YA ESTE ACUERDO. LA REVISIÓN GENERA UN COSTO DE $499 POR DIAGNÓSTICO Y USO DEL LABORATORIO, SERÁN TOMADOS EN CUENTA SI DECIDE REPARAR AQUÍ EL EQUIPO HOY. CONSULTA TÉRMINOS Y CONDICIONES EN EL SITIO WEB. ¡EQUIPOS APAGADOS O MOJADOS NO LLEVAN GARANTÍA! EL SOFTWARE COMO OFFICE SE ENVÍA POR URL Y EL USUARIO DEBE INSTALARLO Y NOTIFICAR PARA ACTIVARLO.</p>
                </div>

                <div class="mock-partner-icons">
                    <div class="icon-box"><img src="img/1.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/2.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/3.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/4.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/5.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/6.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/7.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/8.png" alt="Partner"></div>
                    <div class="icon-box"><img src="img/9.png" alt="Partner"></div>
                </div>



                <div style="margin-top: 10px; font-size: 7.5px; display: flex; justify-content: space-between; align-items: flex-end; color: #444; position: relative;">
                    <div style="width: 33%;"><strong>ESPECIALISTAS EN TECNOLOGIA ROLDU SAS. DE C.V</strong></div>
                    <div style="width: 33%; text-align: center;"></div>
                    <div style="width: 33%; text-align: right;"><strong>sitio web : https://macWave.com.mx</strong><br><strong>mail: contabilidad@macWave.com.mx</strong></div>
                    
                    <div style="position: absolute; right: 0; bottom: 35px; text-align: center;">
                        <img src="${qrUrl}" alt="QR" style="width: 45px; height: 45px;">
                        <p style="font-size: 6px; margin-top: 1px;">macwave.com.mx</p>
                    </div>
                </div>
            </div>
        `;
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        generatePDF();
    });

    async function generatePDF() {
        try {
            if (!window.jspdf || !window.jspdf.jsPDF) {
                alert("Error: jsPDF no está cargado correctamente. Por favor, recarga la página.");
                return;
            }
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            const { items, total } = calculateTotals();
            const client = document.getElementById('client-name').value;
            const project = document.getElementById('project-name').value;
            const tech = document.getElementById('tech-name').value;
            const dateString = document.getElementById('quote-date').value;
            const qNumber = document.getElementById('quote-number').value;
            const currency = document.getElementById('currency').value;

            // --- Single Page Auto-Scaling (Fit to One Page) ---
            const itemsCount = items.length;
            let scale = 1.0;
            if (itemsCount > 12) {
                scale = Math.max(0.6, 1.0 - (itemsCount - 12) * 0.03);
            }
            const fSize = (s) => s * scale;
            const vSpace = (s) => s * scale;
            // --- End Scaling Logic ---

            // Define colors to match CSS exactly
            const RED = [255, 59, 48]; // Apple Red
            const BLUE = [0, 113, 227]; // Apple Blue
            const LIGHT_GREY = [134, 134, 139]; // Dim text
            const BLACK = [0, 0, 0];
            const TEAL = [0, 102, 128]; // Terms color

            // Function to add images preserving aspect ratio and centering within a bounding box
            const addImageProportional = (url, x, y, maxW, maxH) => {
                return new Promise((resolve) => {
                    const img = new Image();
                    img.onload = () => {
                        try {
                            const ratio = img.width / img.height;
                            let w = maxW;
                            let h = maxW / ratio;
                            if (h > maxH) {
                                h = maxH;
                                w = maxH * ratio;
                            }
                            const xOffset = (maxW - w) / 2;
                            const yOffset = (maxH - h) / 2;
                            doc.addImage(img, 'PNG', x + xOffset, y + yOffset, w, h);
                        } catch (e) { console.error("Error adding image:", e); }
                        resolve();
                    };
                    img.onerror = () => {
                        console.warn("Could not load image:", url);
                        resolve();
                    };
                    img.src = url;
                    setTimeout(resolve, 1500);
                });
            };

            let currentY = 15;

            // 1. Header Section
            // Circular Logo on the left
            await addImageProportional(LOGO_0_BASE64, 15, currentY, 40 * scale, 40 * scale);

            // Center Text
            doc.setTextColor(...BLACK);
            doc.setFont("helvetica", "bold");
            doc.setFontSize(fSize(18));
            doc.text("Laboratorio de reparación de", 105, currentY + vSpace(12), { align: 'center' });
            doc.text("computadoras Apple", 105, currentY + vSpace(20), { align: 'center' });

            doc.setFont("helvetica", "normal");
            doc.setFontSize(fSize(10));
            doc.setTextColor(...LIGHT_GREY);
            doc.text("Apple Certified Device Support 2025", 105, currentY + vSpace(28), { align: 'center' });

            // Right Meta Info
            doc.setFontSize(fSize(16));
            doc.setTextColor(...RED);
            doc.setFont("helvetica", "bolditalic");
            doc.text(`Cotización N°`, 200, currentY + vSpace(12), { align: 'right' });
            doc.text(qNumber || "RPC-9199", 200, currentY + vSpace(20), { align: 'right' });

            doc.setTextColor(...BLACK);
            doc.setFontSize(fSize(10));
            doc.setFont("helvetica", "normal");

            // Header Metadata - Cleanly aligned without dots
            const metaXLabel = 155;
            const metaXValue = 200;

            doc.text("Fecha:", metaXLabel, currentY + vSpace(32), { align: 'left' });
            doc.setFont("helvetica", "bold");
            doc.text(dateString, metaXValue, currentY + vSpace(32), { align: 'right' });

            doc.setFont("helvetica", "normal");
            doc.text("Técnico:", metaXLabel, currentY + vSpace(38), { align: 'left' });
            doc.setFont("helvetica", "bold");
            doc.text(tech, metaXValue, currentY + vSpace(38), { align: 'right' });

            doc.setFont("helvetica", "normal");
            doc.text("Moneda:", metaXLabel, currentY + vSpace(44), { align: 'left' });
            doc.setFont("helvetica", "bold");
            doc.text(currency, metaXValue, currentY + vSpace(44), { align: 'right' });

            currentY += vSpace(55);

            // 2. Client Info Section
            doc.setFontSize(fSize(12));
            doc.setTextColor(...BLUE);
            doc.setFont("helvetica", "bold");
            doc.text("Estimado(a) Sr: ", 15, currentY);
            doc.setFont("helvetica", "normal");
            doc.setTextColor(...LIGHT_GREY);
            doc.text(client || "Erik", 15 + vSpace(33), currentY);

            currentY += vSpace(7);

            doc.setTextColor(...BLUE);
            doc.setFont("helvetica", "bold");
            doc.text("Oportunidad / Proyecto: ", 15, currentY);
            doc.setFont("helvetica", "normal");
            doc.setTextColor(...LIGHT_GREY);
            doc.text(project || "Reparación iPhone 16 Pro Max", 15 + vSpace(53), currentY);

            currentY += vSpace(10);

            // 3. Table Section
            const tableData = items.map(item => [
                item.desc,
                `$ ${item.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}`,
                item.qty,
                `$ ${item.subtotal.toLocaleString(undefined, { minimumFractionDigits: 2 })}`
            ]);

            doc.autoTable({
                startY: currentY,
                head: [['DESCRIPCION DEL SERVICIO O PRODUCTO', 'PRECIO UNTARIO', 'UNIDAD', 'SUB TOTAL']],
                body: tableData,
                theme: 'striped',
                headStyles: {
                    fillColor: [0, 0, 0],
                    textColor: [255, 255, 255],
                    fontSize: fSize(9),
                    halign: 'center',
                    fontStyle: 'bold',
                    cellPadding: vSpace(4)
                },
                bodyStyles: {
                    fontSize: fSize(10),
                    cellPadding: vSpace(3),
                    textColor: RED,
                    fontStyle: 'bold'
                },
                alternateRowStyles: {
                    fillColor: [245, 245, 247]
                },
                columnStyles: {
                    0: { cellWidth: 100, halign: 'left' },
                    1: { cellWidth: vSpace(35), halign: 'right' },
                    2: { cellWidth: vSpace(20), halign: 'center' },
                    3: { cellWidth: vSpace(35), halign: 'right' }
                },
                styles: {
                    lineColor: [255, 255, 255],
                    lineWidth: 0.5
                },
                margin: { left: 15, right: 15 }
            });

            currentY = doc.lastAutoTable.finalY + vSpace(15);

            // 4. Total Area
            doc.setFont("helvetica", "bold");
            doc.setTextColor(...RED);
            doc.setFontSize(fSize(16));
            doc.text("TOTAL", 150, currentY);
            doc.text(`$ ${total.toLocaleString(undefined, { minimumFractionDigits: 2 })}`, 200, currentY, { align: 'right' });

            currentY += vSpace(15);

            // 5. Terms Section (Left Aligned & Smaller)
            doc.setFontSize(fSize(7.5));
            doc.setTextColor(...TEAL);
            doc.setFont("helvetica", "bold");

            const terms = [
                `Vigencia de la cotización: 1 día, expira el día ${new Date(new Date(dateString).getTime() + 86400000).toLocaleDateString()}`,
                "Garantía: 31 días en el servicio técnico, pregunta por tu garantía extendida a 100 días POR UN COSTO ADICIONAL. Condiciones: SE REQUIERE",
                "PAGO ANTICIPADO DEL 100% PARA EL SERVICIO.",
                "Tiempo de Entrega: Noviembre de 2025 ENTREGA TENTATIVA POR PARTE DEL FABRICANTE, modelos sugeridos a disponibilidad del fabricante.",
                "ALGUNOS PRODUCTOS IMPORTADOS DE ESTADOS UNIDOS, AMERICAN PARTNER."
            ];

            terms.forEach((term, index) => {
                doc.setFontSize(fSize(index === 2 ? 8.5 : 7.5));
                const splitTerm = doc.splitTextToSize(term, 180);
                doc.text(splitTerm, 15, currentY, { align: 'left' });
                currentY += (splitTerm.length * vSpace(4.5));
            });

            currentY += vSpace(4);
            doc.setDrawColor(220);
            doc.line(15, currentY, 195, currentY);
            currentY += vSpace(8);

            // 6. Bank Area (Left Aligned & Smaller)
            doc.setFontSize(fSize(10));
            doc.setTextColor(...TEAL);
            doc.setFont("helvetica", "bold");
            doc.text("PAGAR A ESTE BANCO", 15, currentY, { align: 'left' });

            currentY += vSpace(6);
            doc.setTextColor(0, 77, 129); // BBVA Blue
            doc.setFontSize(fSize(14));
            doc.text("BBVA", 15, currentY, { align: 'left' });

            currentY += vSpace(8);
            doc.setFontSize(fSize(9));
            doc.setTextColor(...TEAL);
            doc.setFont("helvetica", "normal");
            doc.text(`CUENTA CLABE : ${document.getElementById('clabe').value}`, 15, currentY, { align: 'left' });

            currentY += vSpace(5.5);
            doc.text(`NÚMERO DE CUENTA : ${document.getElementById('account-number').value}`, 15, currentY, { align: 'left' });

            currentY += vSpace(5.5);
            doc.text(`NÚMERO DE TARJETA BBVA : ${document.getElementById('card-number').value}`, 15, currentY, { align: 'left' });

            currentY += vSpace(12);


            // 7. Legal Area (Centered & wrapped)
            // Forced to stay on 1 page - removed addPage

            doc.setFontSize(fSize(6.5));
            doc.setFont("helvetica", "bold");
            doc.setTextColor(0);
            doc.text("***Precios sujetos a cambios sin previo aviso, en variación al dólar americano o disponibilidad en el mercado de Asia.", 15, currentY, { align: 'left' });

            currentY += vSpace(4.5);
            doc.text("*El servicio incluye mantenimiento y resolución de problemas en el sistema, instalación de hardware y sistema operativo, migración o instalación de software con licencia adquirida.", 15, currentY, { align: 'left' });

            currentY += vSpace(5);
            doc.setFontSize(fSize(6));
            doc.setFont("helvetica", "normal");
            const noticeText = "AVISO: EQUIPOS CON ABANDONO CON MÁS DE 30 DÍAS NATURALES A PARTIR DEL DÍA QUE SE DEJÓ EL EQUIPO SERÁN DESTRUIDOS SIN GENERAR NINGÚN TIPO DE RESPONSABILIDAD A RECOVERY PRO Y SU EQUIPO. USTED ACEPTA YA ESTE ACUERDO. LA REVISIÓN GENERA UN COSTO DE $499 POR DIAGNÓSTICO Y USO DEL LABORATORIO, SERÁN TOMADOS EN CUENTA SI DECIDE REPARAR AQUÍ EL EQUIPO HOY. CONSULTA TÉRMINOS Y CONDICIONES EN EL SITIO WEB. ¡EQUIPOS APAGADOS O MOJADOS NO LLEVAN GARANTÍA! EL SOFTWARE COMO OFFICE SE ENVÍA POR URL Y EL USUARIO DEBE INSTALARLO Y NOTIFICAR PARA ACTIVARLO.";
            const splitNotice = doc.splitTextToSize(noticeText, 180);
            doc.text(splitNotice, 15, currentY, { align: 'left' });

            currentY += vSpace(10);
            // 7. Partner Icons Row (1-9)
            const boxW = 12 * scale;
            const boxH = 10 * scale;
            const iconGap = 6 * scale;
            const totalWidth = (9 * boxW) + (8 * iconGap);
            let iconX = (210 - totalWidth) / 2;
            const iconY = currentY;

            const partnerIcons = [
                'img/1.png', 'img/2.png', 'img/3.png', 'img/4.png', 'img/5.png',
                'img/6.png', 'img/7.png', 'img/8.png', 'img/9.png'
            ];

            for (const iconPath of partnerIcons) {
                await addImageProportional(iconPath, iconX, iconY, boxW, boxH);
                iconX += boxW + iconGap;
            }

            // 8. Footer Info (No black strip)
            const footerY = 285;

            doc.setTextColor(...BLACK);
            doc.setFontSize(fSize(7));
            doc.setFont("helvetica", "normal");
            doc.text("ESPECIALISTAS EN TECNOLOGIA ROLDU SAS. DE C.V", 15, footerY);

            doc.setFont("helvetica", "bold");
            doc.text("sitio web : https://macWave.com.mx\nmail: contabilidad@macWave.com.mx", 195, footerY, { align: 'right' });

            // QR Code at the bottom right
            const qrUrl = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://macwave.com.mx";
            await addImageProportional(qrUrl, 182, footerY - vSpace(15), vSpace(12), vSpace(12));
            doc.setFontSize(fSize(5));
            doc.setFont("helvetica", "normal");
            doc.text("macwave.com.mx", 188.5, footerY - vSpace(2), { align: 'center' });

            // Final Action: Open in new tab
            const blobString = doc.output('bloburl');
            window.open(blobString, '_blank');

            // Increment folio for next time
            getNextFolio(true);
            // Update input for next one
            if (quoteNumInput) {
                quoteNumInput.value = getNextFolio();
                updatePreview();
            }

        } catch (error) {
            console.error("Error generating PDF:", error);
            alert("Ocurrió un error crítico al generar el PDF. Verifica los datos.");
        }
    }

    // Initial preview
    updatePreview();
});
