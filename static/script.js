function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.textContent = message;
    popup.classList.add('show');
    setTimeout(() => {
        popup.classList.remove('show');
    }, 3000);
}

function disableForm() {
    const form = document.getElementById('wordle-form');
    if (form) {
        form.remove();
    }
}

document.getElementById('wordle-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const wordInput = document.getElementById('word');
    const word = wordInput.value;
    fetch('/play_wordle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ word: word })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let resultHtml = '';
            for (let i = 0; i < word.length; i++) {
                const letter = word[i];
                let className = 'out';
                if (i in data.well_placed) {
                    className = 'well-placed';
                    resultHtml += `<span class="${className}">${data.well_placed[i]}</span>`;
                } else if (letter in data.in_word) {
                    className = 'in-word';
                    resultHtml += `<span class="${className}">${letter}</span>`;
                } else {
                    resultHtml += `<span class="${className}">${letter}</span>`;
                }
            }
            const newAttempt = document.createElement('div');
            newAttempt.className = 'attempt';
            newAttempt.innerHTML = resultHtml;
            document.getElementById('attempts-list').appendChild(newAttempt);
            wordInput.value = '';

            for (let letter in data.alphabet) {
                const element = document.getElementById(`letter-${letter}`);
                element.className = `letter ${data.alphabet[letter]}`;
            }

            if (data.game_over) {
                disableForm();
                if (data.game_won) {
                    showPopup('Félicitations ! Vous avez trouvé le mot !');
                } else {
                    showPopup('Nombre maximum de tentatives atteint.');
                }
            }
        } else {
            showPopup(data.message);
        }
    });
});

document.getElementById('enter').addEventListener('click', function() {
    document.getElementById('wordle-form').requestSubmit();
});

document.getElementById('backspace').addEventListener('click', function() {
    const wordInput = document.getElementById('word');
    wordInput.value = wordInput.value.slice(0, -1);
});

document.querySelectorAll('.letter').forEach(letterElement => {
    letterElement.addEventListener('click', function() {
        const wordInput = document.getElementById('word');
        wordInput.value += letterElement.textContent;
    });
});

function loadAttempts() {
    fetch('/get_attempts_colors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const attemptsList = document.getElementById('attempts-list');
            attemptsList.innerHTML = ''; // Clear previous attempts

            data.attempts.forEach(attemptData => {
                const attemptDiv = document.createElement('div');
                attemptDiv.className = 'attempt';

                attemptData.attempt.split('').forEach((letter, i) => {
                    const span = document.createElement('span');
                    span.textContent = letter;
                    if (i in attemptData.well_placed) {
                        span.className = 'well-placed';
                    } else if (attemptData.in_word.includes(letter)) {
                        span.className = 'in-word';
                    } else {
                        span.className = 'out';
                    }
                    attemptDiv.appendChild(span);
                });

                attemptsList.appendChild(attemptDiv);
            });

            // Mise à jour des couleurs du clavier
            for (let letter in data.alphabet) {
                const element = document.getElementById(`letter-${letter}`);
                element.className = `letter ${data.alphabet[letter]}`;
            }

            // Supprimer le formulaire si le jeu est gagné ou le nombre maximum de tentatives est atteint
            if (data.game_over) {
                disableForm();
            }
        } else {
            showPopup(data.message);
        }
    });
}

window.onload = function() {
    loadAttempts();
};
