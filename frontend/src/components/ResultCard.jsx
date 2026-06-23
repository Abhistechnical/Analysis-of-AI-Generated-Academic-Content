/**
 * ResultCard — Displays the AI vs Human detection result with probability bars.
 */
export default function ResultCard({ result }) {
  const isAI = result.prediction === 'AI Generated';
  const aiPercent = Math.round(result.ai_probability * 100);
  const humanPercent = Math.round(result.human_probability * 100);

  return (
    <div className="card result-card">
      <div className="card-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M9 11l3 3L22 4"/>
          <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
        </svg>
        <h3>Detection Result</h3>
      </div>
      <div className="card-body">
        {/* Prediction Badge */}
        <div className="result-prediction">
          <span className={`prediction-badge ${isAI ? 'ai' : 'human'}`}>
            <span className="prediction-icon">{isAI ? '🔴' : '🟢'}</span>
            <span className="prediction-text">{result.prediction}</span>
          </span>
          <span className="prediction-confidence">
            {Math.max(aiPercent, humanPercent)}% confidence
          </span>
        </div>

        {/* Probability Bars */}
        <div className="probability-section">
          <div className="probability-row">
            <div className="probability-label">
              <span className="prob-icon">🤖</span>
              <span>AI Generated</span>
            </div>
            <span className="probability-value ai-text">{aiPercent}%</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-bar-fill ai"
              style={{ width: `${aiPercent}%` }}
            />
          </div>

          <div className="probability-row" style={{ marginTop: 16 }}>
            <div className="probability-label">
              <span className="prob-icon">✍️</span>
              <span>Human Written</span>
            </div>
            <span className="probability-value human-text">{humanPercent}%</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-bar-fill human"
              style={{ width: `${humanPercent}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
