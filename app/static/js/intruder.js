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
            if (name === data.selected_name) {
                container.classList.add(data.is_intruder ? 'intruder-correct' : 'intruder-incorrect');
            }
            if (name === data.intruder_name) {
                container.classList.add('intruder-correct-answer');
            }
            // Disable further clicking
            container.style.pointerEvents = 'none';
        });

        setTimeout(() => {
            location.reload();
        }, 1000);
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
