let value = "";
const btn_submt = document.querySelector('.submit_btn');
const messageDiv = document.getElementById('message');
btn_submt.disabled = true;

const inputs = Array.from(document.querySelectorAll('input[class^="form-control"]'));

inputs.forEach((input, idx) => {
    input.setAttribute('maxlength', 1);

    input.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
        updateValue();
        if (e.target.value.length === 1 && idx < inputs.length - 1) {
            inputs[idx + 1].focus();
        }
        subIsActive();
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && e.target.value === '' && idx > 0) {
            inputs[idx - 1].focus();
        }
        setTimeout(() => {
            updateValue();
            subIsActive();
        }, 0);
    });
});

function subIsActive() {
    const filled = inputs.filter(input => input.value.length === 1).length;
    btn_submt.disabled = filled !== 6;
}

function updateValue() {
    value = inputs.map(input => input.value).join('');
}

function showMessage(text, type) {
    if (messageDiv) {
        messageDiv.textContent = text;
        messageDiv.className = type;
    }
    console.log(`💬 [${type}] ${text}`);
}

btn_submt.addEventListener('click', async () => {
    const otpCode = inputs.map(input => input.value).join('');

    if (otpCode.length !== 6) {
        showMessage('Por favor ingresa un código de 6 dígitos', 'error');
        return;
    }

    btn_submt.disabled = true;
    btn_submt.textContent = 'Verificando...';

    try {
        const response = await fetch('http://localhost:5000/api/auth/validate-totp', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: otpCode })
        });

        const data = await response.json();

        if (response.ok && data.valid) {
            showMessage('✅ Código OTP válido. Redirigiendo...', 'success');
            
            // Guardar información de sesión
            const email = localStorage.getItem('pending_verification_email');
            if (email) {
                localStorage.setItem('user_email', email);
                localStorage.setItem('user_auth_method', 'totp');
                localStorage.removeItem('pending_verification_email');
            }

            setTimeout(() => {
                window.location.href = "../../../index/index.html";
            }, 2000);
        } else {
            showMessage('❌ Código OTP inválido', 'error');
            // Limpiar inputs
            inputs.forEach(input => input.value = '');
            inputs[0].focus();
        }
    } catch (error) {
        console.error('Error al validar OTP:', error);
        showMessage('❌ Error de conexión', 'error');
    } finally {
        btn_submt.disabled = false;
        btn_submt.textContent = 'Verificar';
    }
});

// Auto-focus en el primer input
if (inputs.length > 0) {
    inputs[0].focus();
}