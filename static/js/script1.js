
    // Replace 'YOUR_API_KEY' with your actual API key
    const apiKey = 'TMpZtMMIblXfUYNFRADWwJn1COf6rL7a';
    const symbol = 'AAPL';
    // Calculate the day before the current day
    const currentDate = new Date();
    const previousDate = new Date(currentDate);
    previousDate.setDate(currentDate.getDate() - 1);

    // Format the date in 'YYYY-MM-DD' format
    //const date = previousDate.toISOString().split('T')[0];
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
            const volume = data.volume;
    
            // Display the information
            const stockInfoElement = document.getElementById('aapl-stock-info');
            stockInfoElement.innerHTML = `
                <p>Symbol: ${stockSymbol}</p>
                <p>Date: ${stockDate}</p>
                <p>Open Price: ${openPrice}</p>
                <p>Close Price: ${closePrice}</p>
                <p>Number of Stocks: ${volume}</p>
            `;
        })
        .catch(error => {
            // Handle errors
            console.error('Error fetching stock information:', error);
        });

        const symbol2 = 'NFLX'
        const apiUrl2 = `https://api.polygon.io/v1/open-close/${symbol2}/${date}?adjusted=true&apiKey=${apiKey}`;
        fetch(apiUrl2)
        .then(response => response.json())
        .then(data => {
            // Extract relevant information
            const openPrice = data.open;
            const closePrice = data.close;
            const stockSymbol = data.symbol;
            const stockDate = data.from;
            const volume = data.volume;
    
            // Display the information
            const stockInfoElement = document.getElementById('nflx-stock-info');
            stockInfoElement.innerHTML = `
                <p>Symbol: ${stockSymbol}</p>
                <p>Date: ${stockDate}</p>
                <p>Open Price: ${openPrice}</p>
                <p>Close Price: ${closePrice}</p>
                <p>Number of Stocks: ${volume}</p>
            `;
        })
        .catch(error => {
            // Handle errors
            console.error('Error fetching stock information:', error);
        });