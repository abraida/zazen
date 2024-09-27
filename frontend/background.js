
let intervalTimeID;
let remainingTime;
let blockingActive = false;
let allowedUrls = [];
let projectId;
let intervalId;
let url_attempt = null;

// Listener para mensajes
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'startBlocking') {
        const duration = request.duration;
        allowedUrls = request.allowedUrls;
        projectId = request.projectId;
        intervalId = request.intervalId;

        startBlocking(allowedUrls);
        startTimer(duration);
        sendResponse({ status: 'blocking started' });
    }

    if (request.action === 'getPopupData') {
        sendResponse({
            timeLeft: remainingTime, // Tiempo restante
            allowedUrls: allowedUrls  // URLs permitidas
        });
    }

    if (request.action === 'pauseTimer') {
        pauseTimer();
        sendResponse({ status: 'timer paused' });
    }

    if (request.action === 'getLogAttempts') {
        sendResponse({ 
            url: url_attempt
         });
    }

    if (request.action === 'resumeTimer') {
        resumeTimer();
        sendResponse({ status: 'timer resumed' });
    }
});

function startBlocking(allowedUrls) {
    if (blockingActive) return;

    blockingActive = true;

    // Escuchar las solicitudes de URL
    chrome.webRequest.onBeforeRequest.addListener(
        blockingListener,
        { urls: ["<all_urls>"] }, // Escuchar todas las URLs
        ["blocking"] // Permitir la cancelación de la solicitud
    );
}

function stopBlocking() {
    if (!blockingActive) return;

    fetch(`http://localhost:5000/interval/${intervalId}/finish/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ interval_id: intervalId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message); // Mensaje exitoso
        } else {
            console.error("Error:", data.error); // Manejar errores
        }
    })
    .catch((error) => {
        console.error('Error al finalizar el intervalo:', error);
    });

    blockingActive = false;
    chrome.webRequest.onBeforeRequest.removeListener(blockingListener);
}

const blockingListener =
    (details) => {
        const url = details.url;
        const isAllowed = allowedUrls.some(allowedUrl => { return url.includes(allowedUrl) });
        if (!isAllowed && !url.includes("http://localhost:5000")) {
            url_attempt = url
            return { cancel: true };
        }

    };

function startTimer(duration) {
    remainingTime = 1;
    intervalTimeID = setInterval(() => {
        if (remainingTime <= 0) {
            clearInterval(intervalTimeID);
            stopBlocking();
            chrome.runtime.sendMessage({ action: 'timerFinished' }, function (response) {
                console.log("Mensaje enviado al content script: Timer finalizado.");
            });
            
        } else {
            remainingTime--;
            console.log(`Tiempo restante: ${remainingTime} segundos`);
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(intervalTimeID);
    console.log("Temporizador pausado.");
}

function resumeTimer() {
    startTimer(remainingTime);
    console.log("Temporizador reanudado.");
}




