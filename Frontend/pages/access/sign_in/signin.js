// Ruta: Frontend/pages/access/sign_in/signin.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Sign in page loaded');

    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const phoneNumberField = document.getElementById('phoneNumberField');
    const authMethodSMS = document.getElementById('authMethodSMS');
    const authMethodQR = document.getElementById('authMethodQR');

    // Toggle phone field based on auth method
    if (authMethodSMS && authMethodQR) {
        const togglePhoneField = () => {
            if (authMethodSMS.checked) {
                phoneNumberField.style.display = 'block';
                document.getElementById('phone_number').required = true;
            } else {
                phoneNumberField.style.display = 'none';
                document.getElementById('phone_number').required = false;
            }
        };

        authMethodSMS.addEventListener('change', togglePhoneField);
        authMethodQR.addEventListener('change', togglePhoneField);
        togglePhoneField(); // Initial state
    }

    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            togglePassword.querySelector('i').classList.toggle('bi-eye');
            togglePassword.querySelector('i').classList.toggle('bi-eye-slash');
        });
    }

    if (toggleConfirmPassword) {
        toggleConfirmPassword.addEventListener('click', () => {
            const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
            confirmPassword.setAttribute('type', type);
            toggleConfirmPassword.querySelector('i').classList.toggle('bi-eye');
            toggleConfirmPassword.querySelector('i').classList.toggle('bi-eye-slash');
        });
    }
});

document.getElementById("registerBtn").addEventListener("click", async () => {
    console.log('📝 Register button clicked');

    const first_name = document.getElementById("first_name").value.trim();
    const last_name = document.getElementById("last_name").value.trim();
    const email = document.getElementById("your_email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const authMethodElement = document.querySelector('input[name="authMethod"]:checked');
    const phone_number = document.getElementById("phone_number").value.trim();

    // Validaciones
    if (!email || !email.includes("@")) {
        alert("❌ Por favor ingresa un correo válido.");
        return;
    }

    if (!password || password.length < 6) {
        alert("❌ La contraseña debe tener al menos 6 caracteres.");
        return;
    }

    if (password !== confirmPassword) {
        alert("❌ Las contraseñas no coinciden.");
        return;
    }

    if (!authMethodElement) {
        alert("❌ Por favor selecciona un método de autenticación.");
        return;
    }

    const authMethod = authMethodElement.value;

    if (authMethod === 'sms' && !phone_number) {
        alert("❌ Por favor ingresa un número de teléfono.");
        return;
    }

    try {
        console.log('📤 Sending registration request...');

        const response = await fetch("http://localhost:5000/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                email,
                password,
                first_name,
                last_name,
                auth_method: authMethod,
                phone_number: phone_number
            })
        });

        console.log('📨 Response status:', response.status);

        const data = await response.json();
        console.log('📦 Response data:', data);

        if (response.ok) {
            if (authMethod === 'sms') {
                alert("✅ Usuario registrado correctamente. Se envió un código por SMS.");

                // Guardar email para verificación
                localStorage.setItem('pending_verification_email', email);
                localStorage.setItem('user_auth_method', 'sms');

                // Redirigir a verificación SMS
                setTimeout(() => {
                    window.location.href = "../../auth-methods/sms-otp/verification/verification.html";
                }, 1000);
            } else {
                // Para TOTP
                alert("✅ Usuario registrado correctamente. Escanea el QR en la app de autenticación.");
                localStorage.setItem('pending_verification_email', email);
                localStorage.setItem('user_auth_method', 'totp');
                window.location.href = "../../auth-methods/totp/qr_scan/qr.html";
            }
        } else {
            alert("❌ Error: " + (data.error || 'Error en el registro'));
        }
    } catch (error) {
        console.error('❌ Error:', error);
        alert("❌ Error al conectar con el servidor: " + error.message);
    }
});