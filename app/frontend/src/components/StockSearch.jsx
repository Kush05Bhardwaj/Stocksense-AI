// Stock search component
import { useState } from "react";
import { predictStockPrice } from "../api/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

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
                <div style={{ marginTop: '2rem' }}>
                    {/* Company Info Section */}
                    <div style={{ 
                        padding: '1.5rem', 
                        background: '#fff', 
                        border: '2px solid #333',
                        borderRadius: '8px',
                        marginBottom: '1.5rem',
                        color: '#000'
                    }}>
                        <h3 style={{ color: '#000', marginTop: 0 }}>
                            {prediction.company_name || prediction.symbol}
                        </h3>
                        <p style={{ fontSize: '1.3rem', margin: '0.5rem 0', color: '#000' }}>
                            <strong>Current Price:</strong> {prediction.currency}{prediction.current_price?.toFixed(2)}
                        </p>
                    </div>

                    {/* Model Predictions in Cards */}
                    <h4 style={{ color: '#000', marginBottom: '1rem' }}>Model Predictions:</h4>
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                        gap: '1rem'
                    }}>
                        {prediction.predictions && prediction.predictions.map((pred, index) => (
                            <div key={index} style={{
                                padding: '1.5rem',
                                background: '#fff',
                                border: '2px solid #ddd',
                                borderRadius: '8px',
                                color: '#000'
                            }}>
                                <h4 style={{ 
                                    color: '#000', 
                                    marginTop: 0,
                                    marginBottom: '1rem',
                                    borderBottom: '2px solid #eee',
                                    paddingBottom: '0.5rem'
                                }}>
                                    {pred.model}
                                </h4>
                                
                                <div style={{ marginBottom: '1rem' }}>
                                    <p style={{ color: '#666', margin: '0.3rem 0', fontSize: '0.9rem' }}>
                                        Predicted Price
                                    </p>
                                    <p style={{ 
                                        color: '#000', 
                                        fontSize: '1.5rem', 
                                        fontWeight: 'bold',
                                        margin: '0.3rem 0'
                                    }}>
                                        {prediction.currency}{pred.prediction?.toFixed(2)}
                                    </p>
                                </div>

                                <div style={{ marginBottom: '1rem' }}>
                                    <p style={{ color: '#666', margin: '0.3rem 0', fontSize: '0.9rem' }}>
                                        Expected Change
                                    </p>
                                    <p style={{ 
                                        color: pred.change > 0 ? '#28a745' : '#dc3545',
                                        fontSize: '1.3rem',
                                        fontWeight: 'bold',
                                        margin: '0.3rem 0'
                                    }}>
                                        {pred.change > 0 ? '↑' : '↓'} {pred.change > 0 ? '+' : ''}{pred.change?.toFixed(2)}%
                                    </p>
                                </div>

                                {/* Simple Bar Chart */}
                                <div style={{ 
                                    marginTop: '1rem', 
                                    paddingTop: '1rem', 
                                    borderTop: '1px solid #eee' 
                                }}>
                                    <ResponsiveContainer width="100%" height={120}>
                                        <BarChart data={[
                                            { name: 'Current', value: prediction.current_price },
                                            { name: 'Predicted', value: pred.prediction }
                                        ]}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="name" />
                                            <YAxis />
                                            <Tooltip />
                                            <Bar dataKey="value" fill="#4CAF50">
                                                <Cell fill="#2196F3" />
                                                <Cell fill={pred.change > 0 ? '#28a745' : '#dc3545'} />
                                            </Bar>
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}