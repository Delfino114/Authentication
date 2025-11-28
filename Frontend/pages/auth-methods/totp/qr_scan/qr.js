// Ruta: Frontend/pages/auth-methods/totp/qr_scan/qr.js
document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("qrContainer");
    const scannedBtn = document.getElementById("scannedBtn");

    // Evitar cargar múltiples veces
    if (container.querySelector("img")) return;

    try {
        console.log('📡 Obteniendo código QR...');
        
        const response = await fetch("http://localhost:5000/api/auth/qr", {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    No autorizado. Por favor inicia sesión.
                </div>
            `;
            console.error("No autorizado", response.status);
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const img = document.createElement("img");
        img.src = url;
        img.alt = "QR Code";
        img.className = "img-fluid";

        // Limpiar spinner y mostrar QR
        container.innerHTML = '';
        container.appendChild(img);
        
        console.log('✅ QR cargado exitosamente');

    } catch (error) {
        container.innerHTML = `
            <div class="alert alert-danger">
                Error al cargar el QR. Verifica conexión con el servidor.
            </div>
        `;
        console.error('❌ Error cargando QR:', error);
    }

    // Configurar botón de continuación
    if (scannedBtn) {
        scannedBtn.addEventListener("click", () => {
            window.location.href = "../verification/verification.html";
        });
    }
});