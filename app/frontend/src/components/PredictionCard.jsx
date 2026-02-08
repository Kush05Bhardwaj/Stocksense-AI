// Prediction card component
export default function PredictionCard({ prediction }) {
    if (!prediction) return null;

    return (
        <div className="prediction-card">
            <h3>Prediction Results</h3>
            <p><strong>Symbol:</strong> {prediction.symbol}</p>
            <p><strong>Predicted Price:</strong> ${prediction.price?.toFixed(2)}</p>
            <p><strong>Confidence:</strong> {prediction.confidence || 'N/A'}</p>
        </div>
    );
}
