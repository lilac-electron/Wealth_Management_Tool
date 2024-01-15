
    // Replace 'YOUR_API_KEY' with your actual API key
    const apiKey = 'TMpZtMMIblXfUYNFRADWwJn1COf6rL7a';
    const symbol = 'AAPL';
    const date = '2023-01-09';
    
    // Construct the API URL
    const apiUrl = `https://api.polygon.io/v1/open-close/${symbol}/${date}?adjusted=true&apiKey=${apiKey}`;
    
    // Make a GET request to the API using fetch
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Extract relevant information
            const openPrice = data.open;
            const closePrice = data.close;
            const stockSymbol = data.symbol;
            const stockDate = data.from;
    
            // Display the information
            const stockInfoElement = document.getElementById('stock-info');
            stockInfoElement.innerHTML = `
                <p>Symbol: ${stockSymbol}</p>
                <p>Date: ${stockDate}</p>
                <p>Open Price: ${openPrice}</p>
                <p>Close Price: ${closePrice}</p>
            `;
        })
        .catch(error => {
            // Handle errors
            console.error('Error fetching stock information:', error);
        });