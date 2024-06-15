function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.textContent = message;
    popup.classList.add('show');
    setTimeout(() => {
        popup.classList.remove('show');
    }, 5000);
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
            //newAttempt.innerHTML = resultHtml;
            //document.getElementById('attempts-list').appendChild(newAttempt);
            wordInput.value = '';

            for (let letter in data.alphabet) {
                const element = document.getElementById(`letter-${letter}`);
                if (element) {
                    element.className = `letter ${data.alphabet[letter]}`;
                }
            }
            
            if (data.game_over) {
                disableForm();
                console.log(data.attempts.length);
                if (data.game_won) {
                    showPopup('Félicitations ! Vous avez trouvé le mot ! Vous remportez ' + (6 - data.attempts.length) + ' points !');
                } else {
                    showPopup('Nombre maximum de tentatives atteint. Le mot était : ' + data.word + '. Vous avez gagné 1 point.');
                }
            }
            loadAttempts();
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
            const attemptDivs = attemptsList.getElementsByClassName('attempt');

            data.attempts.forEach((attemptData, index) => {
                const letterBoxes = attemptDivs[index].getElementsByClassName('letter-box');
                attemptData.attempt.split('').forEach((letter, i) => {
                    const span = letterBoxes[i].getElementsByTagName('span')[0];
                    span.textContent = letter;
                    
                    if (attemptData.well_placed.includes(i)) {
                        
                        span.className = 'well-placed';
                        // Colore dans l'alpabet la lettre bien placée
                        var element = document.getElementById(`letter-${letter}`);
                        if (element) {
                            
                            element.className = 'letter green';
                        }

                    } else if (attemptData.in_word.includes(letter)) {
                        span.className = 'in-word';
                        var element = document.getElementById(`letter-${letter}`);
                        if (element) {
                            element.className = 'letter orange';
                        }
                        delete attemptData.in_word[attemptData.in_word.indexOf(letter)];
                    } else {
                        span.className = 'out';
                        var element = document.getElementById(`letter-${letter}`);
                        if (element) {
                            element.className = 'letter red';
                        }
                    }
                });
            });

          

            // Supprimer le formulaire si le jeu est gagné ou le nombre maximum de tentatives est atteint
            if (data.game_over) {
                disableForm();
            }
        } else {
            showPopup(data.message);
        }
    });
    var element = document.getElementById('word');
    if (element) {
        element.focus();
    }

}

window.onload = function() {
    loadAttempts();
};
