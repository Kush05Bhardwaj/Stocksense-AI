// Portfolio page
import { useState, useEffect } from "react";
import axios from "axios";

export default function Portfolio() {
    const [portfolio, setPortfolio] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch portfolio data from backend
        axios.get('/api/portfolio')
            .then((response) => {
                setPortfolio(response.data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching portfolio:", error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading portfolio...</div>;
    }

    return (
        <div>
            <h1>My Portfolio</h1>
            {portfolio.length === 0 ? (
                <p>No stocks in portfolio</p>
            ) : (
                <div>
                    {portfolio.map((stock, index) => (
                        <div key={index} style={{ padding: '1rem', border: '1px solid #ccc', margin: '1rem 0', borderRadius: '8px' }}>
                            <h3>{stock.symbol}</h3>
                            <p>Shares: {stock.shares}</p>
                            <p>Value: ${stock.value}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
