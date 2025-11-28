// Ruta: Frontend/public/index.js
async function Acceder() {
    try {
        console.log('🚀 Redirigiendo al sistema de autenticación...');
        window.location.href = '/pages/access/log_in/login.html';
    } catch (e) {
        console.error('❌ Error en navegación:', e);
        alert('Error al acceder al sistema. Por favor recarga la página.');
    }
}

// Verificar si ya hay una sesión activa al cargar la página principal
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🔍 Verificando sesión activa...');
    
    try {
        const response = await fetch('http://localhost:5000/api/auth/session-check', {
            method: 'GET',
            credentials: 'include'
        });

        console.log('📨 Respuesta de verificación de sesión:', response.status);

        if (response.ok) {
            const sessionData = await response.json();
            console.log('📋 Datos de sesión:', sessionData);
            
            if (sessionData.logged_in) {
                console.log('✅ Sesión activa detectada, redirigiendo al dashboard...');
                
                // Guardar información en localStorage para consistencia
                if (sessionData.email) {
                    localStorage.setItem('user_email', sessionData.email);
                }
                if (sessionData.auth_method) {
                    localStorage.setItem('user_auth_method', sessionData.auth_method);
                }
                
                // Redirigir al dashboard
                setTimeout(() => {
                    window.location.href = '/pages/index/index.html';
                }, 1000);
            } else {
                console.log('ℹ️ No hay sesión activa, mostrando página principal');
            }
        } else {
            console.log('ℹ️ No se pudo verificar la sesión, mostrando página principal');
        }
    } catch (error) {
        console.log('⚠️ Error verificando sesión:', error);
        console.log('ℹ️ Mostrando página principal');
    }
});

// Función adicional para mejorar la UX
function mostrarInfoMetodos() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Inicializar tooltips si Bootstrap está disponible
if (typeof bootstrap !== 'undefined') {
    document.addEventListener('DOMContentLoaded', mostrarInfoMetodos);
}

// Manejar el estado de los botones durante la navegación
document.addEventListener('DOMContentLoaded', () => {
    const accederBtn = document.querySelector('button[onclick="Acceder()"]');
    if (accederBtn) {
        accederBtn.addEventListener('click', function() {
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Redirigiendo...';
            this.disabled = true;
        });
    }
});

// Función para mostrar estadísticas del sistema (opcional)
async function cargarEstadisticas() {
    try {
        const response = await fetch('http://localhost:5000/api/auth/health');
        if (response.ok) {
            const healthData = await response.json();
            console.log('📊 Estado del sistema:', healthData);
            
            // Podrías mostrar esta información en la UI si lo deseas
            if (healthData.total_users !== undefined) {
                console.log(`👥 Usuarios registrados: ${healthData.total_users}`);
            }
        }
    } catch (error) {
        console.log('⚠️ No se pudieron cargar las estadísticas del sistema');
    }
}

// Cargar estadísticas cuando la página esté lista
document.addEventListener('DOMContentLoaded', cargarEstadisticas);