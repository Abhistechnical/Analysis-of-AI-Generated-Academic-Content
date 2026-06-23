import { useState, useEffect } from 'react';

const API = 'http://localhost:8000/api';

/**
 * ModelInfo — About Model page showing algorithms, dataset, and metrics.
 */
export default function ModelInfo() {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API}/model-info`);
      if (!res.ok) throw new Error('Failed to fetch model info');
      const data = await res.json();
      setInfo(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="spinner"></div>
        <span className="loading-text">Loading model information...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        ⚠️ {error}
      </div>
    );
  }

  if (!info) return null;

  const metricItems = [
    { label: 'Accuracy', value: info.metrics.accuracy, color: 'var(--primary)' },
    { label: 'Precision', value: info.metrics.precision, color: 'var(--accent)' },
    { label: 'Recall', value: info.metrics.recall, color: 'var(--success)' },
    { label: 'F1 Score', value: info.metrics.f1_score, color: 'var(--warning)' },
  ];

  return (
    <div className="model-info-page">
      <div className="page-header">
        <h2>About the Model</h2>
        <p>Technical details about the machine learning models used for AI content detection.</p>
      </div>

      {/* Algorithms */}
      <div className="card mt-lg">
        <div className="card-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
          <h3>Algorithms Used</h3>
        </div>
        <div className="card-body">
          <div className="algorithm-grid">
            {info.algorithms.map((algo, i) => (
              <div className={`algorithm-card ${algo.is_active ? 'active' : ''}`} key={i}>
                <div className="algo-header">
                  <h4>{algo.name}</h4>
                  {algo.is_active && (
                    <span className="badge badge-success">Active</span>
                  )}
                </div>
                <p className="algo-desc">{algo.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Dataset Info */}
      <div className="card mt-lg">
        <div className="card-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3"/>
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
          </svg>
          <h3>Dataset Information</h3>
        </div>
        <div className="card-body">
          <div className="stat-grid">
            <div className="stat-item">
              <div className="stat-value">{info.dataset.total_samples}</div>
              <div className="stat-label">Total Samples</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{info.dataset.ai_samples}</div>
              <div className="stat-label">AI Samples</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{info.dataset.human_samples}</div>
              <div className="stat-label">Human Samples</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{info.dataset.train_size}</div>
              <div className="stat-label">Training Set</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">{info.dataset.test_size}</div>
              <div className="stat-label">Test Set</div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Metrics */}
      <div className="card mt-lg">
        <div className="card-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
          </svg>
          <h3>Model Evaluation Metrics</h3>
          {info.active_algorithm && (
            <span className="badge badge-primary" style={{ marginLeft: 'auto' }}>
              {info.active_algorithm}
            </span>
          )}
        </div>
        <div className="card-body">
          <div className="metrics-grid">
            {metricItems.map((metric, i) => (
              <div className="metric-card" key={i}>
                <div className="metric-circle" style={{ '--metric-color': metric.color }}>
                  <svg viewBox="0 0 36 36" className="circular-chart">
                    <path className="circle-bg"
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path className="circle-fill"
                      strokeDasharray={`${metric.value * 100}, 100`}
                      style={{ stroke: metric.color }}
                      d="M18 2.0845
                        a 15.9155 15.9155 0 0 1 0 31.831
                        a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <span className="metric-percent">{(metric.value * 100).toFixed(1)}%</span>
                </div>
                <span className="metric-label">{metric.label}</span>
              </div>
            ))}
          </div>

          <div className="divider"></div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Training Accuracy</td>
                  <td><strong>{(info.metrics.train_accuracy * 100).toFixed(2)}%</strong></td>
                </tr>
                <tr>
                  <td>Testing Accuracy</td>
                  <td><strong>{(info.metrics.test_accuracy * 100).toFixed(2)}%</strong></td>
                </tr>
                <tr>
                  <td>Precision</td>
                  <td><strong>{(info.metrics.precision * 100).toFixed(2)}%</strong></td>
                </tr>
                <tr>
                  <td>Recall</td>
                  <td><strong>{(info.metrics.recall * 100).toFixed(2)}%</strong></td>
                </tr>
                <tr>
                  <td>F1 Score</td>
                  <td><strong>{(info.metrics.f1_score * 100).toFixed(2)}%</strong></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
