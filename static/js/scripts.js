function choosePerson(winner, loser, personNumber) {
    fetch("/dilemma", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            winner: winner,
            loser: loser
        })
    })
    .then(response => response.json())
    .then(data => {
        const eloIncrease = data.elo_increase; // Number of places gained
        
        // Select the container of the chosen person
        const winnerContainer = document.querySelector(`.side:nth-child(${personNumber})`);
        
        const dilemmaContainer = document.querySelector(".container")
        const buttons = dilemmaContainer.querySelectorAll("button")
        buttons.forEach(b => b.disabled = true)

        // Get the button inside the chosen container
        const button = winnerContainer.querySelector('button');
        const nameElement = winnerContainer.querySelector('h2');
        // Remove existing ranking-up element if present
        let rankingUpElement = winnerContainer.querySelector('.ranking-up');
        if (rankingUpElement) {
            rankingUpElement.remove();
        }

        // Create a new ranking-up element
        rankingUpElement = document.createElement('div');
        rankingUpElement.classList.add('ranking-up');
        rankingUpElement.textContent = `↑1`; // Starting text

        // Insert it next to the button
        button.parentNode.insertBefore(rankingUpElement, button.nextSibling);

        nameElement.classList.add("selected")

        // Increment the number with animation
        let currentNumber = 0;
        const increment = setInterval(() => {
            currentNumber++;
            rankingUpElement.textContent = `↑${currentNumber}`;
            if (currentNumber === eloIncrease) {
                clearInterval(increment);
            }
        }, 5);

        // Add visual effects (like grow animation) if needed
        winnerContainer.classList.add('selected', 'show-ranking');

        // Delay the page reload so the user can see the ranking-up effect
        setTimeout(() => {
            location.reload();
        }, eloIncrease * 5 + 1000); // Adjust timing based on the number of increments
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function chooseParty(memberName, chosenParty) {
    fetch("/guess-party/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            member: memberName,
            party: chosenParty
        })
    })
    .then(response => response.json())
    .then(data => {
        const buttons = document.querySelectorAll('.party-buttons button');

        // Iterate over buttons to find the correct and selected options
        buttons.forEach(button => {
            const party = button.innerText;

            // Highlight the correct answer
            if (party === data.correct_party) {
                button.classList.add('highlight-correct');
            }

            // Change the color of the chosen button
            if (party === chosenParty) {
                if (data.is_correct) {
                    button.classList.add('correct');
                } else {
                    button.classList.add('incorrect');
                }
            }

            // Disable all buttons to prevent further clicking
            button.disabled = true;
        });

        setTimeout(() => {
            location.reload();
        }, 1000);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
