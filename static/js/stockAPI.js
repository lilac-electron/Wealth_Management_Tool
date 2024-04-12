
    // Replace 'YOUR_API_KEY' with your actual API key
    const apiKey = 'TMpZtMMIblXfUYNFRADWwJn1COf6rL7a';
    const symbol = 'AAPL';
    // Calculate the day before the current day
    // Format the date in 'YYYY-MM-DD' format
    var today = new Date();
    var yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 5);
    var year = yesterday.getFullYear();
    var month = yesterday.getMonth() + 1;
    var day = yesterday.getDate();
    month = (month < 10 ? '0' : '') + month;
    day = (day < 10 ? '0' : '') + day;
    var formattedDate = year + '-' + month + '-' + day;

    const date = '2024-01-08';
    //const date = formattedDate
    
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

        //const date = '2023-01-09';
        const date2 = '2024-02-09'

        const symbol2 = 'NSPI'
        const apiUrl2 = `https://api.polygon.io/v1/open-close/${symbol2}/${date2}?adjusted=true&apiKey=${apiKey}`;
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