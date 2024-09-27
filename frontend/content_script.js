let lastUrlAttempt;

// Escuchar mensajes de la ventana de la aplicación Flask
window.addEventListener("message", function (event) {
    if (event.source !== window) return;

    if (event.data && event.data.type === "FROM_FLASK") {
        console.log("Mensaje recibido de Flask:", event.data);

        if (event.data.action === 'startInterval') {
            const duration = event.data.payload.duration;
            const allowedUrls = event.data.payload.allowedUrls;
            const projectId = event.data.payload.projectId;
            const intervalId = event.data.payload.intervalId;

            console.log("Duración y URLs permitidas:", { duration, allowedUrls });
            startBlocking(duration, allowedUrls, intervalId);
        }
        if (event.data.action === 'pauseTimer') {
            pauseTimer();
        }
        if (event.data.action === 'resumeTimer') {
            resumeTimer();
        }

        if (event.data.action === 'getLogAttempts') {
            getLogAttempts();

        }
    }
});

// Funciones para pausar y reanudar el temporizador
function pauseTimer() {
    chrome.runtime.sendMessage({ action: "pauseTimer" }, function (response) {
        console.log("Respuesta del background script al pausar:", response);
    });
}

function resumeTimer() {
    chrome.runtime.sendMessage({ action: "resumeTimer" }, function (response) {
        console.log("Respuesta del background script al reanudar:", response);
    });
}

function getLogAttempts() {
    let url_attempt = null

    chrome.runtime.sendMessage({ action: "getLogAttempts" }, function (response) {
        console.log("Respuesta del background script al pedir urls:", response);
        url_attempt = response.url

    });

    if (url_attempt !== null && url_attempt != lastUrlAttempt) {
        
    }


}

function startBlocking(duration, allowedUrls, intervalId) {
    chrome.runtime.sendMessage({
        action: "startBlocking",
        duration: duration,
        allowedUrls: allowedUrls,
        intervalId: intervalId
    }, function (response) {
        console.log("Respuesta del background script:", response);

        if (response && response.status === 'blocking started') {
            console.log("Bloqueo iniciado correctamente.");
        } else {
            console.error("Error al iniciar el bloqueo.");
        }
    });

}