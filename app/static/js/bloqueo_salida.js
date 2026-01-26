// Ruta: minimarket_api/app/static/js/bloqueo_salida.js

console.log("✅ Script bloqueo_salida.js cargado");

window.addEventListener("beforeunload", function () {
  const token = localStorage.getItem("token");

  if (token) {
    console.warn("⚠️ Cierre inesperado detectado. Se eliminará el token.");

    // Enviar auditoría al backend
    navigator.sendBeacon("/auditoria/cierre", JSON.stringify({
      evento: "cierre_sin_salida",
      token: token,
      fecha: new Date().toISOString()
    }));

    // Eliminar token y datos locales
    localStorage.removeItem("token");
    localStorage.removeItem("intentos");
    localStorage.removeItem("bloqueado");

    // ❌ No activamos e.preventDefault ni e.returnValue
  }
});
