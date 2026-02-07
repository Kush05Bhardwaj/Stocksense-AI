// Stock search component
import { useState } from "react";
import { predictStockPrice } from "../api/api";

export default function StockSearch() {
    const [stockSymbol, setStockSymbol] = useState("");
    const [predictedPrice, setPredictedPrice] = useState(null);

    const handleSearch = () => {
        predictStockPrice(stockSymbol)
            .then((price) => {
                setPredictedPrice(price);
            })
            .catch((error) => {
                console.error("Error fetching predicted price:", error);
            });
    };

    return (
        <div>
            <input
                type="text"
                value={stockSymbol}
                onChange={(e) => setStockSymbol(e.target.value)}
                placeholder="Enter stock symbol"
            />
            <button onClick={handleSearch}>Search</button>
            {predictedPrice && <p>Predicted Price: {predictedPrice}</p>}
        </div>
    );
}