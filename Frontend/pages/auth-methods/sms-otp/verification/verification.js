// Ruta: Frontend/pages/auth-methods/sms-otp/verification/verification.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Verification page loaded');

    const otpInput = document.getElementById('otp');
    const verifyButton = document.getElementById('verifyOTP');
    const resendButton = document.getElementById('resendOTP');
    const messageDiv = document.getElementById('message');

    // Auto-focus y auto-tab
    if (otpInput) {
        otpInput.focus();
        
        otpInput.addEventListener('input', (e) => {
            // Solo permitir números
            e.target.value = e.target.value.replace(/\D/g, '');
            
            if (e.target.value.length === 6) {
                verifyButton.click();
            }
        });
    }

    // Verificar OTP
    if (verifyButton) {
        verifyButton.addEventListener('click', async () => {
            console.log('🔍 Verify button clicked');

            const otp = otpInput.value.trim();

            if (!otp || otp.length !== 6) {
                showMessage('Por favor ingresa un código válido de 6 dígitos', 'error');
                return;
            }

            verifyButton.disabled = true;
            verifyButton.textContent = 'Verificando...';

            try {
                console.log('📤 Sending verification request...');

                const email = localStorage.getItem('pending_verification_email') || localStorage.getItem('user_email');
                
                const response = await fetch('http://localhost:5000/api/auth/verify-otp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ 
                        otp: otp,
                        email: email
                    })
                });

                console.log('📨 Response status:', response.status);

                const data = await response.json();
                console.log('📦 Response data:', data);

                if (response.ok && data.valid) {
                    showMessage('✅ Verificación exitosa. Redirigiendo...', 'success');

                    // Guardar información en localStorage
                    localStorage.setItem('user_email', email);
                    localStorage.setItem('user_auth_method', 'sms');
                    localStorage.removeItem('pending_verification_email');

                    setTimeout(() => {
                        window.location.href = "../../../index/index.html";
                    }, 2000);
                } else {
                    showMessage(data.error || '❌ Código inválido', 'error');
                    otpInput.value = '';
                    otpInput.focus();
                }
            } catch (error) {
                console.error('❌ Error:', error);
                showMessage('❌ Error de conexión', 'error');
            } finally {
                verifyButton.disabled = false;
                verifyButton.textContent = 'Verificar';
            }
        });
    }

    // Reenviar OTP
    if (resendButton) {
        resendButton.addEventListener('click', async () => {
            console.log('🔄 Resend button clicked');

            resendButton.disabled = true;
            resendButton.textContent = 'Enviando...';

            try {
                const email = localStorage.getItem('pending_verification_email') || localStorage.getItem('user_email');
                
                if (!email) {
                    showMessage('❌ No se encontró información de verificación', 'error');
                    return;
                }

                const response = await fetch('http://localhost:5000/api/auth/resend-otp', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ email: email })
                });

                const data = await response.json();
                console.log('📦 Response:', data);

                if (response.ok) {
                    showMessage('✅ Nuevo código enviado', 'success');
                    otpInput.value = '';
                    otpInput.focus();
                } else {
                    showMessage(data.error || '❌ Error al reenviar el código', 'error');
                }
            } catch (error) {
                console.error('❌ Error:', error);
                showMessage('❌ Error de conexión', 'error');
            } finally {
                resendButton.disabled = false;
                resendButton.textContent = 'Reenviar código';
            }
        });
    }

    // Permitir Enter para verificar
    if (otpInput) {
        otpInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && verifyButton) {
                verifyButton.click();
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

    // Verificar si hay email en localStorage al cargar
    const storedEmail = localStorage.getItem('pending_verification_email');
    if (storedEmail) {
        console.log('📧 Email encontrado en localStorage:', storedEmail);
        showMessage('📱 Ingresa el código enviado por SMS', 'info');
    } else {
        console.log('⚠️ No se encontró email en localStorage');
        showMessage('⚠️ No se encontró información de verificación', 'error');
    }
});