// Function to check if the selected member is the intruder
function checkIntruder(selectedName) {
    // Get all members' names and parties
    const members = Array.from(document.querySelectorAll('.intruder-container')).map(container => {
        return container.getAttribute('data-name');
    });

    // Make a POST request to the Flask server to check the intruder
    fetch('/intruder/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ members: members, selected_name: selectedName })
    })
    .then(response => response.json())
    .then(data => {
        const containers = document.querySelectorAll('.intruder-container');

        // Highlight the selected container
        containers.forEach(container => {
            const name = container.getAttribute('data-name');
            const partyName = document.createElement("div")
            if (name === data.selected_name) {
                if (data.is_intruder) {
                    container.classList.add('intruder-correct')
                    partyName.innerHTML = data.intruder_party
                } else {
                    container.classList.add('intruder-incorrect')
                    partyName.innerHTML = data.majority_party
                }
            }
            else if (name === data.intruder_name) {
                partyName.innerHTML = data.intruder_party
                setTimeout(() => {
                    container.classList.add('intruder-correct-answer')
                }, 500)
            } else {
                partyName.innerHTML = data.majority_party
            }
            container.appendChild(partyName)
            // Disable further clicking
            container.style.pointerEvents = 'none';
        });

        setTimeout(() => {
            location.reload();
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listeners to the member containers
document.addEventListener('DOMContentLoaded', () => {
    const containers = document.querySelectorAll('.intruder-container');
    containers.forEach(container => {
        container.addEventListener('click', () => {
            const selectedName = container.getAttribute('data-name');
            checkIntruder(selectedName);
        });
    });
});
