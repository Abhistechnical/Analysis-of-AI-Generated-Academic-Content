/**
 * IndicatorsCard — Shows AI detection indicators with severity levels.
 */
export default function IndicatorsCard({ indicators }) {
  return (
    <div className="card">
      <div className="card-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        <h3>AI Indicators</h3>
      </div>
      <div className="card-body">
        <div className="indicator-grid">
          {indicators.map((indicator, i) => (
            <div className="indicator-item" key={i}>
              <span className="indicator-name">{indicator.name}</span>
              <span className={`indicator-value ${indicator.value.toLowerCase()}`}>
                {indicator.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
