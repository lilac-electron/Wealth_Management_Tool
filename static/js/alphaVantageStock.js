const apiKey = 'MFGDW78ZDSOSES7U';
const stockFunction = 'TIME_SERIES_MONTHLY';
const symbol = 'AAPL';

const url = `https://www.alphavantage.co/query?function=${stockFunction}&symbol=${symbol}&apikey=${apiKey}`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        // Accessing the relevant property from the response data
        const metaData = data['Meta Data'];
        const symbol = metaData['2. Symbol'];
        
        // Displaying the symbol in an element with id 'test-stock'
        const stockInfoElement = document.getElementById('test-stock');
        stockInfoElement.innerHTML = `<p>Symbol: ${symbol}</p>`;
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });