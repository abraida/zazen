document.addEventListener('DOMContentLoaded', function () {
    const allowedUrlsList = document.getElementById('allowedUrlsList');
    const timerElement = document.getElementById('timer');
    const pauseButton = document.getElementById('pause');
    const resumeButton = document.getElementById('resume');

    // Función para actualizar el contador en el popup
    function updateTimer(timeLeft) {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    // Función para mostrar las URLs permitidas en el popup
    function updateAllowedUrls(urls) {
        allowedUrlsList.innerHTML = ''; // Limpiar lista actual
        urls.forEach(url => {
            const li = document.createElement('li');
            li.textContent = url;
            li.classList.add('url-item');
            allowedUrlsList.appendChild(li);
        });
    }

    // Solicitar información al background script
    chrome.runtime.sendMessage({ action: 'getPopupData' }, function (response) {
        if (response) {
            updateTimer(response.timeLeft); // Actualizar el temporizador
            updateAllowedUrls(response.allowedUrls); // Actualizar las URLs permitidas
        }
    });

    // Listener para pausar el temporizador
    pauseButton.addEventListener('click', function () {
        chrome.runtime.sendMessage({ action: 'pauseTimer' }, function (response) {
            console.log('Temporizador pausado:', response);
            pauseButton.style.display = 'none';
            resumeButton.style.display = 'inline-block';
        });
    });

    // Listener para reanudar el temporizador
    resumeButton.addEventListener('click', function () {
        chrome.runtime.sendMessage({ action: 'resumeTimer' }, function (response) {
            console.log('Temporizador reanudado:', response);
            pauseButton.style.display = 'inline-block';
            resumeButton.style.display = 'none';
        });
    });
});
