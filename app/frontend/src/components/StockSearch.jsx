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
                    border: '2px solid #333', 
                    borderRadius: '12px',
                    background: '#ffffff',
                    color: '#000000'
                }}>
                    <h3 style={{ color: '#000', marginBottom: '1rem' }}>Prediction Results</h3>
                    {prediction.company_name && prediction.company_name !== prediction.symbol && (
                        <p style={{ color: '#000', fontSize: '1.1rem', marginBottom: '0.5rem' }}>
                            <strong>Company:</strong> {prediction.company_name}
                        </p>
                    )}
                    <p style={{ color: '#000', marginBottom: '0.5rem' }}>
                        <strong>Symbol:</strong> {prediction.symbol}
                    </p>
                    <p style={{ color: '#000', fontSize: '1.2rem', marginBottom: '1rem' }}>
                        <strong>Current Price:</strong> {prediction.currency || '$'}{prediction.current_price?.toFixed(2) || 'N/A'}
                    </p>
                    
                    <hr style={{ margin: '1rem 0', border: '1px solid #ccc' }} />
                    
                    <h4 style={{ color: '#000', marginBottom: '1rem' }}>Model Predictions:</h4>
                    {prediction.predictions && prediction.predictions.length > 0 ? (
                        <div style={{ display: 'grid', gap: '1rem' }}>
                            {prediction.predictions.map((pred, index) => (
                                <div key={index} style={{ 
                                    padding: '1rem', 
                                    background: '#f5f5f5', 
                                    borderRadius: '8px',
                                    border: '1px solid #ddd'
                                }}>
                                    <p style={{ color: '#000', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                                        {pred.model}
                                    </p>
                                    <p style={{ color: '#000', fontSize: '1.1rem', marginBottom: '0.3rem' }}>
                                        <strong>Predicted Price:</strong> {prediction.currency}{pred.prediction?.toFixed(2)}
                                    </p>
                                    <p style={{ 
                                        color: pred.change > 0 ? '#28a745' : '#dc3545',
                                        fontWeight: 'bold',
                                        fontSize: '1rem'
                                    }}>
                                        <strong>Expected Change:</strong> {pred.change > 0 ? '+' : ''}{pred.change?.toFixed(2)}%
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p style={{ color: '#000' }}>No predictions available</p>
                    )}
                </div>
            )}
        </div>
    );
}