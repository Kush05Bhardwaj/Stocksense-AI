// Stock search component
import { useState } from "react";
import { predictStockPrice } from "../api/api";
import { 
    ComposedChart, 
    Line, 
    Bar, 
    XAxis, 
    YAxis, 
    CartesianGrid, 
    Tooltip, 
    Legend, 
    ResponsiveContainer,
    Area,
    AreaChart
} from 'recharts';

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

                    {/* Model Predictions in 2x2 Grid */}
                    <h4 style={{ color: '#000', marginBottom: '1rem' }}>Model Predictions:</h4>
                    <div style={{ 
                        display: 'grid', 
                        gridTemplateColumns: 'repeat(2, 1fr)',
                        gap: '1.5rem',
                        maxWidth: '1200px'
                    }}>
                        {prediction.predictions && prediction.predictions.map((pred, index) => {
                            // Prepare chart data
                            const chartData = [
                                { 
                                    name: 'Current', 
                                    price: prediction.current_price,
                                    type: 'Current'
                                },
                                { 
                                    name: 'Predicted', 
                                    price: pred.prediction,
                                    change: pred.change,
                                    type: 'Predicted'
                                }
                            ];

                            return (
                                <div key={index} style={{
                                    padding: '1.5rem',
                                    background: '#fff',
                                    border: '2px solid #ddd',
                                    borderRadius: '8px',
                                    color: '#000',
                                    minHeight: '350px'
                                }}>
                                    <h4 style={{ 
                                        color: '#000', 
                                        marginTop: 0,
                                        marginBottom: '1rem',
                                        borderBottom: '2px solid #eee',
                                        paddingBottom: '0.5rem',
                                        fontSize: '1.1rem'
                                    }}>
                                        {pred.model}
                                    </h4>
                                    
                                    <div style={{ marginBottom: '1rem' }}>
                                        <p style={{ color: '#666', margin: '0.2rem 0', fontSize: '0.85rem' }}>
                                            Predicted Price
                                        </p>
                                        <p style={{ 
                                            color: '#000', 
                                            fontSize: '1.4rem', 
                                            fontWeight: 'bold',
                                            margin: '0.2rem 0'
                                        }}>
                                            {prediction.currency}{pred.prediction?.toFixed(2)}
                                        </p>
                                    </div>

                                    <div style={{ marginBottom: '1rem' }}>
                                        <p style={{ color: '#666', margin: '0.2rem 0', fontSize: '0.85rem' }}>
                                            Expected Change
                                        </p>
                                        <p style={{ 
                                            color: pred.change > 0 ? '#28a745' : '#dc3545',
                                            fontSize: '1.2rem',
                                            fontWeight: 'bold',
                                            margin: '0.2rem 0'
                                        }}>
                                            {pred.change > 0 ? '↑' : '↓'} {pred.change > 0 ? '+' : ''}{pred.change?.toFixed(2)}%
                                        </p>
                                    </div>

                                    {/* Chart based on index */}
                                    <div style={{ 
                                        marginTop: '1rem', 
                                        paddingTop: '1rem', 
                                        borderTop: '1px solid #eee' 
                                    }}>
                                        <ResponsiveContainer width="100%" height={150}>
                                            {index === 0 ? (
                                                // Bar Chart for Linear Regression
                                                <ComposedChart data={chartData}>
                                                    <CartesianGrid strokeDasharray="3 3" />
                                                    <XAxis dataKey="name" />
                                                    <YAxis />
                                                    <Tooltip />
                                                    <Bar dataKey="price" fill={pred.change > 0 ? '#28a745' : '#dc3545'} />
                                                </ComposedChart>
                                            ) : index === 1 ? (
                                                // Line Chart for Random Forest
                                                <ComposedChart data={chartData}>
                                                    <CartesianGrid strokeDasharray="3 3" />
                                                    <XAxis dataKey="name" />
                                                    <YAxis />
                                                    <Tooltip />
                                                    <Line 
                                                        type="monotone" 
                                                        dataKey="price" 
                                                        stroke={pred.change > 0 ? '#28a745' : '#dc3545'}
                                                        strokeWidth={3}
                                                    />
                                                </ComposedChart>
                                            ) : index === 2 ? (
                                                // Area Chart for XGBoost
                                                <AreaChart data={chartData}>
                                                    <CartesianGrid strokeDasharray="3 3" />
                                                    <XAxis dataKey="name" />
                                                    <YAxis />
                                                    <Tooltip />
                                                    <Area 
                                                        type="monotone" 
                                                        dataKey="price" 
                                                        fill={pred.change > 0 ? '#28a745' : '#dc3545'}
                                                        fillOpacity={0.6}
                                                        stroke={pred.change > 0 ? '#28a745' : '#dc3545'}
                                                    />
                                                </AreaChart>
                                            ) : (
                                                // Candlestick-style for LSTM
                                                <ComposedChart data={chartData}>
                                                    <CartesianGrid strokeDasharray="3 3" />
                                                    <XAxis dataKey="name" />
                                                    <YAxis />
                                                    <Tooltip />
                                                    <Bar 
                                                        dataKey="price" 
                                                        fill={pred.change > 0 ? '#28a745' : '#dc3545'}
                                                        barSize={40}
                                                    />
                                                    <Line 
                                                        type="monotone" 
                                                        dataKey="price" 
                                                        stroke="#2196F3"
                                                        strokeWidth={2}
                                                    />
                                                </ComposedChart>
                                            )}
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}