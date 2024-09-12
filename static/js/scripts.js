function choosePerson(winner, loser) {
    // Create a POST request using Fetch API
    fetch("/", {
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
        console.log(data.message); // Handle response from server
        location.reload(); // Reload the page to show new people
    })
    .catch(error => {
        console.error('Error:', error);
    });
}