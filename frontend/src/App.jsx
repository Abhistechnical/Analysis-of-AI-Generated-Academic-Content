import { useState, useRef } from 'react';
import Header from './components/Header';
import TextInput from './components/TextInput';
import ResultCard from './components/ResultCard';
import StatsCard from './components/StatsCard';
import IndicatorsCard from './components/IndicatorsCard';
import Charts from './components/Charts';
import ModelInfo from './components/ModelInfo';
import AdminDashboard from './components/AdminDashboard';
import './App.css';

const API = 'http://localhost:8000/api';

/**
 * App — Main application shell with tab navigation and analysis workflow.
 */
export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const resultRef = useRef(null);

  const handleAnalyze = async (text) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const res = await fetch(`${API}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Analysis failed');
      }

      const data = await res.json();
      setResult(data);

      // Scroll to results
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeFile = async (file) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${API}/analyze/file`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'File analysis failed');
      }

      const data = await res.json();
      setResult(data);

      // Scroll to results
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyResult = () => {
    if (!result) return;
    const text = `AI Academic Content Detector - Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Prediction: ${result.prediction}
AI Generated Probability: ${Math.round(result.ai_probability * 100)}%
Human Written Probability: ${Math.round(result.human_probability * 100)}%

Content Statistics:
  Words: ${result.statistics.total_words}
  Sentences: ${result.statistics.total_sentences}
  Avg Sentence Length: ${result.statistics.avg_sentence_length}
  Vocabulary Richness: ${result.statistics.vocabulary_richness}%

AI Indicators:
${result.indicators.map(i => `  ${i.name}: ${i.value}`).join('\n')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;
    navigator.clipboard.writeText(text);
  };

  const handleExportPDF = () => {
    window.print();
  };

  return (
    <>
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="main-content">
        <div className="container">

          {/* ─── Home Tab ─── */}
          {activeTab === 'home' && (
            <div className="home-page">
              <TextInput
                onAnalyze={handleAnalyze}
                onAnalyzeFile={handleAnalyzeFile}
                loading={loading}
              />

              {/* Error */}
              {error && (
                <div className="alert alert-error mt-lg">
                  ⚠️ {error}
                </div>
              )}

              {/* Results */}
              {result && (
                <div className="results-section" ref={resultRef}>
                  <div className="results-header">
                    <h2 className="section-title" style={{ marginBottom: 0 }}>
                      📊 Analysis Results
                    </h2>
                    <div className="results-actions">
                      <button
                        className="btn btn-ghost btn-sm"
                        onClick={handleCopyResult}
                        title="Copy result to clipboard"
                        id="copy-result-btn"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                        </svg>
                        Copy
                      </button>
                      <button
                        className="btn btn-ghost btn-sm"
                        onClick={handleExportPDF}
                        title="Export as PDF"
                        id="export-pdf-btn"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                          <line x1="12" y1="18" x2="12" y2="12"/>
                          <line x1="9" y1="15" x2="15" y2="15"/>
                        </svg>
                        Export PDF
                      </button>
                    </div>
                  </div>

                  <div className="results-grid">
                    <ResultCard result={result} />
                    <StatsCard statistics={result.statistics} />
                    <IndicatorsCard indicators={result.indicators} />
                    <Charts result={result} />
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ─── Model Info Tab ─── */}
          {activeTab === 'model' && <ModelInfo />}

          {/* ─── Admin Tab ─── */}
          {activeTab === 'admin' && <AdminDashboard />}

        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>AI Academic Content Detector • Built with React, FastAPI & Scikit-Learn</p>
        </div>
      </footer>
    </>
  );
}
