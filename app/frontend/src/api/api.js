// API client
import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:3000/api",
});

export const predictStockPrice = (stockSymbol) => {
    API.post("/predict", { stockSymbol })
        .then((response) => {
            console.log("Predicted price:", response.data.predictedPrice);
        })
        .catch((error) => {
            console.error("Error predicting stock price:", error);
        });
};

export const getPortfolioStatus = () => {
    API.get("/portfolio/status")
        .then((response) => {
            console.log("Portfolio status:", response.data);
        })
        .catch((error) => {
            console.error("Error fetching portfolio status:", error);
        });
};

export const buyStock = (stockSymbol, quantity) => {
    API.post("/portfolio/buy", { stockSymbol, quantity })
        .then((response) => {
            console.log("Stock bought successfully:", response.data);
        })
        .catch((error) => {
            console.error("Error buying stock:", error);
        });
};
