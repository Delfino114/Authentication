// Ruta: Frontend/pages/auth-methods/sms-otp/sms.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 SMS OTP page loaded');

    const smsForm = document.getElementById('smsForm');
    const messageDiv = document.getElementById('message');

    if (smsForm) {
        smsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('📱 SMS Form submitted');

            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();

            if (!email || !email.includes('@')) {
                showMessage('Por favor ingresa un correo válido', 'error');
                return;
            }

            if (!phone) {
                showMessage('Por favor ingresa un número de teléfono', 'error');
                return;
            }

            showMessage('Enviando código SMS...', 'info');

            try {
                console.log('📤 Sending SMS request...');

                const response = await fetch('http://localhost:5000/api/auth/send-sms-otp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ 
                        email: email,
                        phone_number: phone
                    })
                });

                console.log('📨 Response status:', response.status);

                const data = await response.json();
                console.log('📦 Response data:', data);

                if (response.ok && data.success) {
                    showMessage('✅ Código SMS enviado correctamente', 'success');
                    
                    // Guardar información para la verificación
                    localStorage.setItem('pending_verification_email', email);
                    localStorage.setItem('user_auth_method', 'sms');

                    // Redirigir a verificación después de 2 segundos
                    setTimeout(() => {
                        window.location.href = './verification/verification.html';
                    }, 2000);
                } else {
                    showMessage(data.error || '❌ Error al enviar el código SMS', 'error');
                }
            } catch (error) {
                console.error('❌ Error:', error);
                showMessage('❌ Error de conexión con el servidor', 'error');
            }
        });
    }

    function showMessage(text, type) {
        if (messageDiv) {
            messageDiv.textContent = text;
            messageDiv.className = `mt-3 text-center text-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'}`;
        }
        console.log(`💬 [${type}] ${text}`);
    }

    // Verificar si ya hay una sesión activa
    const storedEmail = localStorage.getItem('user_email');
    if (storedEmail) {
        document.getElementById('email').value = storedEmail;
    }
});