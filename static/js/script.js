/* =========================================================
   SOC-AI - LÓGICA PRINCIPAL
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    console.log("SOC-AI iniciado correctamente");
    inicializarNavegacion();
    cargarEstado();
    cargarMetricas();
    cargarAlertas();

    // Actualización en segundo plano cada 15 segundos
    setInterval(() => {
        cargarEstado();
        cargarMetricas();
        cargarAlertas();
    }, 15000);
});

/* =========================================================
   SISTEMA DE NOTIFICACIONES (TOAST)
   ========================================================= */
function mostrarToast(mensaje, tipo = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    
    const icono = tipo === 'success' ? '✓' : (tipo === 'error' ? '✕' : 'ℹ');
    toast.innerHTML = `<span style="font-size: 18px;">${icono}</span> <span>${mensaje}</span>`;
    
    container.appendChild(toast);
    
    // Auto-eliminar después de 4 segundos
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/* =========================================================
   NAVEGACIÓN
   ========================================================= */
function inicializarNavegacion() {
    const links = document.querySelectorAll(".nav-link");
    const sections = document.querySelectorAll(".content-section");
    const headerTitle = document.getElementById("header-title");
    const headerSubtitle = document.getElementById("header-subtitle");

    const titulos = {
        'trafico': ['Monitoreo de Tráfico', 'Analiza solicitudes HTTP en tiempo real con IA.'],
        'alertas': ['Registro de Alertas', 'Eventos detectados como comportamiento anómalo.'],
        'analista': ['Analista SOC Virtual', 'Consulta información sobre el estado actual del sistema.'],
        'ia': ['Asistente de Ciberseguridad', 'Consulta sobre seguridad web, ataques y vulnerabilidades.'],
        'sistema': ['Información del Sistema', 'Detalles técnicos y configuración de SOC-AI.']
    };

    window.mostrarSeccion = function(targetId) {
        // Actualizar clases activas
        links.forEach(link => {
            link.classList.toggle("active", link.dataset.section === targetId);
        });
        sections.forEach(section => {
            section.classList.toggle("active", section.id === targetId);
        });

        // Actualizar header
        if (titulos[targetId]) {
            headerTitle.textContent = titulos[targetId][0];
            headerSubtitle.textContent = titulos[targetId][1];
        }
    };
}

/* =========================================================
   ESTADO Y MÉTRICAS
   ========================================================= */
async function cargarEstado() {
    try {
        const response = await fetch("/api/health");
        const data = await response.json();
        const dot = document.querySelector(".status-dot");
        const text = document.querySelector(".status-text");
        
        if (response.ok) {
            dot.style.background = "#22c55e";
            dot.style.boxShadow = "0 0 0 3px rgba(34, 197, 94, 0.2)";
            text.textContent = "Sistema Operativo";
        } else {
            throw new Error("Error en health check");
        }
    } catch (error) {
        const dot = document.querySelector(".status-dot");
        const text = document.querySelector(".status-text");
        dot.style.background = "#ef4444";
        dot.style.boxShadow = "0 0 0 3px rgba(239, 68, 68, 0.2)";
        text.textContent = "Sistema Desconectado";
    }
}

async function cargarMetricas() {
    try {
        const response = await fetch("/api/metrics");
        if (!response.ok) return;
        const data = await response.json();

        document.getElementById("totalEventos").textContent = data.total ?? 0;
        document.getElementById("totalAlertas").textContent = data.alertas ?? 0;
        
        // Calcular tráfico normal
        const total = Number(data.total ?? 0);
        const alertas = Number(data.alertas ?? 0);
        document.getElementById("totalNormales").textContent = Math.max(0, total - alertas);

        // Calcular riesgo
        let porcentaje = total > 0 ? (alertas / total) * 100 : 0;
        document.getElementById("nivelRiesgo").textContent = porcentaje.toFixed(1) + "%";
        
    } catch (error) {
        console.error("Error cargando métricas:", error);
    }
}

/* =========================================================
   ALERTAS
   ========================================================= */
async function cargarAlertas() {
    try {
        const response = await fetch("/api/alerts");
        if (!response.ok) return;
        const data = await response.json();
        mostrarAlertas(data.alertas || data);
    } catch (error) {
        console.error("Error cargando alertas:", error);
    }
}

function mostrarAlertas(alertas) {
    const container = document.getElementById("alertasContainer");
    if (!Array.isArray(alertas) || alertas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="empty-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <p>No hay alertas registradas en este momento.</p>
            </div>`;
        return;
    }

    let html = '<table><thead><tr><th>Nivel</th><th>Descripción</th><th>IP</th><th>Fecha</th></tr></thead><tbody>';
    alertas.forEach(alerta => {
        const nivel = obtenerNivelAlerta(alerta);
        const badgeClass = nivel === 'danger' ? 'badge-danger' : (nivel === 'warning' ? 'badge-warning' : 'badge-info');
        const nivelTexto = nivel === 'danger' ? 'Crítico' : (nivel === 'warning' ? 'Medio' : 'Informativo');
        
        html += `
            <tr>
                <td><span class="badge ${badgeClass}">${nivelTexto}</span></td>
                <td>${escapeHTML(alerta.tipo || alerta.mensaje || "Actividad sospechosa")}</td>
                <td><code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-size:12px;">${escapeHTML(alerta.ip || 'N/A')}</code></td>
                <td style="color: var(--text-muted); font-size: 13px;">${escapeHTML(alerta.timestamp || new Date().toLocaleString())}</td>
            </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function obtenerNivelAlerta(alerta) {
    const nivel = String(alerta.nivel || alerta.severidad || "").toLowerCase();
    if (nivel.includes("critical") || nivel.includes("alto")) return "danger";
    if (nivel.includes("medium") || nivel.includes("medio")) return "warning";
    return "info";
}

/* =========================================================
   ANÁLISIS DE TRÁFICO
   ========================================================= */
document.getElementById("trafficForm")?.addEventListener("submit", async function(event) {
    event.preventDefault();
    const btn = document.getElementById("btnAnalizar");
    const originalText = btn.innerHTML;
    btn.innerHTML = `<svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> Analizando...`;
    btn.disabled = true;

    const formData = new FormData(this);
    const datos = Object.fromEntries(formData);

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });
        const resultado = await response.json();

        if (!response.ok) throw new Error(resultado.error || "Error durante el análisis");

        mostrarResultadoAnalisis(resultado);
        mostrarToast("Tráfico analizado correctamente", "success");
        cargarMetricas(); // Actualizar contadores
    } catch (error) {
        mostrarToast("Error al analizar: " + error.message, "error");
        document.getElementById("resultadoAnalisis").innerHTML = `<div class="alert alert-danger">❌ ${escapeHTML(error.message)}</div>`;
        document.getElementById("resultadoAnalisis").classList.remove("hidden");
        document.getElementById("resultadoInicial").classList.add("hidden");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
});

function mostrarResultadoAnalisis(resultado) {
    const inicial = document.getElementById("resultadoInicial");
    const contenedor = document.getElementById("resultadoAnalisis");
    inicial.classList.add("hidden");
    contenedor.classList.remove("hidden");

    const esAmenaza = resultado.alerta || resultado.sospechoso || resultado.prediccion === -1;
    
    if (esAmenaza) {
        contenedor.innerHTML = `
            <div style="display:flex; gap:12px; align-items:flex-start;">
                <div style="background:var(--danger-bg); color:var(--danger-text); padding:8px; border-radius:8px;">⚠️</div>
                <div>
                    <h4 style="color:var(--danger-text); margin-bottom:4px;">Actividad Sospechosa Detectada</h4>
                    <p style="color:var(--text-secondary); font-size:14px;">${escapeHTML(resultado.mensaje || "El modelo ha identificado un comportamiento potencialmente malicioso.")}</p>
                    <div style="margin-top:12px; display:flex; gap:8px;">
                        <span class="badge badge-danger">IP: ${escapeHTML(resultado.ip || 'N/A')}</span>
                        <span class="badge badge-warning">Score: ${resultado.score || 'N/A'}</span>
                    </div>
                </div>
            </div>`;
    } else {
        contenedor.innerHTML = `
            <div style="display:flex; gap:12px; align-items:flex-start;">
                <div style="background:var(--success-bg); color:var(--success-text); padding:8px; border-radius:8px;">✓</div>
                <div>
                    <h4 style="color:var(--success-text); margin-bottom:4px;">Actividad Normal</h4>
                    <p style="color:var(--text-secondary); font-size:14px;">${escapeHTML(resultado.mensaje || "La solicitud no presenta características sospechosas.")}</p>
                </div>
            </div>`;
    }
}

/* =========================================================
   CONSULTAS IA (Analista y Asistente)
   ========================================================= */
document.getElementById("analistaForm")?.addEventListener("submit", async function(e) {
    e.preventDefault();
    const input = document.getElementById("preguntaAnalista");
    const respuestaDiv = document.getElementById("respuestaAnalista");
    await consultarIAEndpoint(input.value, respuestaDiv, "/api/ai-analysis");
});

document.getElementById("iaForm")?.addEventListener("submit", async function(e) {
    e.preventDefault();
    const input = document.getElementById("preguntaIA");
    const respuestaDiv = document.getElementById("respuestaIA");
    await consultarIAEndpoint(input.value, respuestaDiv, "/api/ai-analysis"); // Ajusta la URL si es diferente
});

async function consultarIAEndpoint(pregunta, contenedor, url) {
    if (!pregunta.trim()) return;
    
    contenedor.classList.remove("hidden");
    contenedor.innerHTML = `<div style="display:flex; align-items:center; gap:10px; color:var(--text-muted);"><div class="spinner" style="width:18px; height:18px; border:2px solid var(--border-color); border-top-color:var(--accent-primary); border-radius:50%; animation: spin 0.8s linear infinite;"></div> La IA está procesando tu consulta...</div>`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta: pregunta })
        });
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.error || "No se pudo consultar el analista IA");

        contenedor.innerHTML = `<div style="line-height:1.7;">${formatearRespuestaIA(data.respuesta || data.response || "Sin respuesta.")}</div>`;
        mostrarToast("Consulta respondida por la IA", "success");
    } catch (error) {
        contenedor.innerHTML = `<div style="color:var(--danger-text);">❌ ${escapeHTML(error.message)}</div>`;
        mostrarToast("Error en la consulta IA", "error");
    }
}

/* =========================================================
   UTILIDADES
   ========================================================= */
function formatearRespuestaIA(texto) {
    return escapeHTML(String(texto))
        .replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

function escapeHTML(valor) {
    return String(valor)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Animación CSS para el spinner
const style = document.createElement('style');
style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
document.head.appendChild(style);