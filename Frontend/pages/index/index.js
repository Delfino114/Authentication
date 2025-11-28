async function cerrarSesion() {
    try {
        const response = await fetch('http://localhost:5000/api/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });

        if (response.ok) {
            console.log('✅ Sesión cerrada exitosamente');
        }
    } catch (e) {
        console.error('Error en logout:', e);
    }
    
    // Limpiar localStorage
    localStorage.removeItem('pending_verification_email');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_auth_method');
    
    // Redirigir al login
    window.location.replace('../access/log_in/login.html');
}

async function cargarUsuario() {
    try {
        console.log('🔍 Verificando sesión en dashboard...');
        
        const response = await fetch('http://localhost:5000/api/auth/user-info', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            const userData = await response.json();
            console.log('✅ Información de usuario:', userData);
            
            // Actualizar UI
            document.getElementById('welcome-text').textContent = 
                `¡Bienvenido ${userData.first_name || 'Usuario'}!`;
            document.getElementById('session-info').textContent = 
                `Sesión activa para: ${userData.email}`;
            document.getElementById('auth-method').textContent = 
                `Método: ${userData.auth_method === 'sms' ? 'SMS OTP' : 'QR/TOTP'}`;
            
            // Guardar en localStorage para consistencia
            localStorage.setItem('user_email', userData.email);
            localStorage.setItem('user_auth_method', userData.auth_method);
            
        } else {
            console.log('❌ No hay sesión activa, redirigiendo...');
            window.location.replace('../access/log_in/login.html');
        }
        
    } catch (error) {
        console.error('❌ Error cargando usuario:', error);
        window.location.replace('../access/log_in/login.html');
    }
}

// Cargar usuario cuando la página se carga
document.addEventListener('DOMContentLoaded', cargarUsuario);