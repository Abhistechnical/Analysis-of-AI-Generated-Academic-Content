import { useState, useEffect, useRef } from 'react';
import PredictionHistory from './PredictionHistory';

const API = import.meta.env.DEV ? 'http://localhost:8000/api' : '/_/backend/api';

/**
 * AdminDashboard — Admin panel for dataset management, retraining, and history.
 */
export default function AdminDashboard() {
  const [history, setHistory] = useState([]);
  const [totalHistory, setTotalHistory] = useState(0);
  const [page, setPage] = useState(1);
  const [perPage] = useState(10);
  const [uploading, setUploading] = useState(false);
  const [retraining, setRetraining] = useState(false);
  const [message, setMessage] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, [page]);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API}/admin/history?page=${page}&per_page=${perPage}`);
      if (!res.ok) throw new Error('Failed to fetch history');
      const data = await res.json();
      setHistory(data.predictions);
      setTotalHistory(data.total);
    } catch (err) {
      console.error('History fetch error:', err);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      setMessage(null);
      const res = await fetch(`${API}/admin/upload-dataset`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Upload failed');
      setMessage({ type: 'success', text: `✓ ${data.message}` });
    } catch (err) {
      setMessage({ type: 'error', text: `✗ ${err.message}` });
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleRetrain = async () => {
    try {
      setRetraining(true);
      setMessage(null);
      const res = await fetch(`${API}/admin/retrain`, { method: 'POST' });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Retraining failed');
      setMessage({
        type: 'success',
        text: `✓ ${data.message} — Accuracy: ${(data.metrics.accuracy * 100).toFixed(1)}%`,
      });
    } catch (err) {
      setMessage({ type: 'error', text: `✗ ${err.message}` });
    } finally {
      setRetraining(false);
    }
  };

  const handleExport = async () => {
    try {
      const res = await fetch(`${API}/admin/export`);
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'prediction_history.csv';
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setMessage({ type: 'error', text: `✗ ${err.message}` });
    }
  };

  const totalPages = Math.ceil(totalHistory / perPage);

  return (
    <div className="admin-page">
      <div className="page-header">
        <h2>Admin Dashboard</h2>
        <p>Manage datasets, retrain the model, and view prediction history.</p>
      </div>

      {/* Status Message */}
      {message && (
        <div className={`alert ${message.type === 'success' ? 'alert-success' : 'alert-error'} mt-md`}>
          {message.text}
        </div>
      )}

      {/* Actions Grid */}
      <div className="admin-actions mt-lg">
        {/* Upload Dataset */}
        <div className="card admin-action-card">
          <div className="card-body">
            <div className="action-icon">📁</div>
            <h4>Upload Dataset</h4>
            <p className="text-muted text-small">Upload a CSV file with 'text' and 'label' columns</p>
            <input
              type="file"
              ref={fileInputRef}
              accept=".csv"
              onChange={handleUpload}
              style={{ display: 'none' }}
              id="csv-upload"
            />
            <button
              className="btn btn-primary btn-sm mt-md"
              onClick={() => fileInputRef.current?.click()}
              disabled={uploading}
              id="upload-btn"
            >
              {uploading ? (
                <>
                  <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }}></span>
                  Uploading...
                </>
              ) : (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                  </svg>
                  Choose CSV File
                </>
              )}
            </button>
          </div>
        </div>

        {/* Retrain Model */}
        <div className="card admin-action-card">
          <div className="card-body">
            <div className="action-icon">🔄</div>
            <h4>Retrain Model</h4>
            <p className="text-muted text-small">Retrain all ML models with current dataset</p>
            <button
              className="btn btn-primary btn-sm mt-md"
              onClick={handleRetrain}
              disabled={retraining}
              id="retrain-btn"
            >
              {retraining ? (
                <>
                  <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }}></span>
                  Training...
                </>
              ) : (
                <>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="23 4 23 10 17 10"/>
                    <polyline points="1 20 1 14 7 14"/>
                    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                  </svg>
                  Retrain Model
                </>
              )}
            </button>
          </div>
        </div>

        {/* Export Reports */}
        <div className="card admin-action-card">
          <div className="card-body">
            <div className="action-icon">📊</div>
            <h4>Download Reports</h4>
            <p className="text-muted text-small">Export prediction history as CSV report</p>
            <button
              className="btn btn-primary btn-sm mt-md"
              onClick={handleExport}
              disabled={totalHistory === 0}
              id="export-btn"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Export CSV
            </button>
          </div>
        </div>
      </div>

      {/* Prediction History */}
      <div className="card mt-lg">
        <div className="card-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          <h3>Prediction History</h3>
          <span className="badge badge-info" style={{ marginLeft: 'auto' }}>{totalHistory} records</span>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          <PredictionHistory
            predictions={history}
            page={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </div>
      </div>
    </div>
  );
}
