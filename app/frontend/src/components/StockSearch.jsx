// Stock search component
import { useState } from "react";
import { predictStockPrice } from "../api/api";

export default function StockSearch() {
    const [stockSymbol, setStockSymbol] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = () => {
        if (!stockSymbol.trim()) {
            setError("Please enter a stock symbol");
            return;
        }

        setLoading(true);
        setError(null);
        
        predictStockPrice(stockSymbol.toUpperCase())
            .then((data) => {
                setPrediction(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching predicted price:", error);
                setError("Failed to fetch prediction. Please try again.");
                setLoading(false);
            });
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    return (
        <div className="stock-search">
            <div style={{ marginBottom: '1rem' }}>
                <input
                    type="text"
                    value={stockSymbol}
                    onChange={(e) => setStockSymbol(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Enter stock symbol (e.g., AAPL)"
                    style={{ marginRight: '0.5rem', padding: '0.5rem' }}
                />
                <button onClick={handleSearch} disabled={loading}>
                    {loading ? 'Loading...' : 'Predict'}
                </button>
            </div>

            {error && (
                <div style={{ color: 'red', marginTop: '1rem' }}>
                    {error}
                </div>
            )}

            {prediction && (
                <div className="prediction-card" style={{ 
                    marginTop: '1rem', 
                    padding: '1.5rem', 
                    border: '1px solid #ccc', 
                    borderRadius: '8px',
                    background: '#f9f9f9'
                }}>
                    <h3>Prediction Results</h3>
                    {prediction.company_name && prediction.company_name !== prediction.symbol && (
                        <p><strong>Company:</strong> {prediction.company_name}</p>
                    )}
                    <p><strong>Symbol:</strong> {prediction.symbol}</p>
                    <p><strong>Current Price:</strong> {prediction.currency || '$'}{prediction.current_price?.toFixed(2) || 'N/A'}</p>
                    <p><strong>Predicted Price:</strong> {prediction.currency || '$'}{prediction.prediction?.toFixed(2) || 'N/A'}</p>
                    <p><strong>Model Used:</strong> {prediction.model || 'N/A'}</p>
                    {prediction.change && (
                        <p style={{ color: prediction.change > 0 ? 'green' : 'red' }}>
                            <strong>Expected Change:</strong> {prediction.change > 0 ? '+' : ''}{prediction.change.toFixed(2)}%
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}