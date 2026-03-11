import axios from 'axios';

const API_BASE_URL = '/api';

// Predict stock price
export const predictStockPrice = async (symbol, model = 'xgb') => {
    try {
        const response = await axios.post(`${API_BASE_URL}/predict`, {
            symbol: symbol,
            model: model
        });
        return response.data;
    } catch (error) {
        console.error('Error predicting stock price:', error);
        throw error;
    }
};

// Get portfolio
export const getPortfolio = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/portfolio`);
        return response.data;
    } catch (error) {
        console.error('Error fetching portfolio:', error);
        throw error;
    }
};

// Add stock to portfolio
export const addToPortfolio = async (symbol, quantity) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/portfolio`, {
            symbol,
            quantity
        });
        return response.data;
    } catch (error) {
        console.error('Error adding to portfolio:', error);
        throw error;
    }
};

// Get stock history
export const getStockHistory = async (symbol) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/history/${symbol}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching stock history:', error);
        throw error;
    }
};

// Investment report
export const getInvestmentReport = (symbol) => axios.get(`/api/report/${symbol}`);

// Download report
export const downloadReportPDF = (symbol) => axios.get(`/api/report/${symbol}/pdf`, { responseType: 'blob' })