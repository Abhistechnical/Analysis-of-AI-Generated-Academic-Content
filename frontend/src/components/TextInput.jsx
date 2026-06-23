import { useState } from 'react';

/**
 * TextInput — Large text area with word counter, tabbed file upload zone, and validation.
 */
export default function TextInput({ onAnalyze, onAnalyzeFile, loading }) {
  const [activeTab, setActiveTab] = useState('text'); // 'text' or 'file'
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [fileError, setFileError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;

  const handleAnalyze = () => {
    if (activeTab === 'text') {
      if (text.trim().length < 20) return;
      onAnalyze(text.trim());
    } else {
      if (!file || fileError) return;
      onAnalyzeFile(file);
    }
  };

  const handleClear = () => {
    if (activeTab === 'text') {
      setText('');
    } else {
      setFile(null);
      setFileError(null);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && e.ctrlKey && activeTab === 'text') {
      handleAnalyze();
    }
  };

  // Drag and drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (selectedFile) => {
    const ext = selectedFile.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt'].includes(ext)) {
      setFileError('Unsupported file format. Only PDF, DOCX, and TXT are supported.');
      setFile(null);
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setFileError('File exceeds 5MB size limit. Please upload a smaller document.');
      setFile(null);
      return;
    }
    setFileError(null);
    setFile(selectedFile);
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="text-input-section">
      <div className="text-input-header">
        <h2>Analyze Academic Content</h2>
        <p>Paste text or upload a document to detect AI-generated and human-written styles.</p>
      </div>

      {/* Tabs */}
      <div className="input-tabs">
        <button
          className={`input-tab-btn ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
          disabled={loading}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          Paste Text
        </button>
        <button
          className={`input-tab-btn ${activeTab === 'file' ? 'active' : ''}`}
          onClick={() => setActiveTab('file')}
          disabled={loading}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          Upload Document
        </button>
      </div>

      {activeTab === 'text' ? (
        /* Textarea Wrapper */
        <div className="textarea-wrapper">
          <textarea
            className="textarea"
            id="text-input"
            rows={10}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Paste academic content here for analysis...

Example: Research papers, essays, dissertations, thesis sections, literature reviews, or any scholarly text."
            disabled={loading}
          />
          <div className="textarea-footer">
            <div className="text-counters">
              <span className="counter">{wordCount} words</span>
              <span className="counter-divider">·</span>
              <span className="counter">{charCount} characters</span>
            </div>
            {text.trim().length > 0 && text.trim().length < 20 && (
              <span className="counter-warning">
                Minimum 20 characters required
              </span>
            )}
          </div>
        </div>
      ) : (
        /* File Upload Area */
        <div className="file-upload-wrapper">
          <div
            className={`file-dropzone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => !file && document.getElementById('file-upload-input').click()}
          >
            <input
              type="file"
              id="file-upload-input"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              style={{ display: 'none' }}
              disabled={loading}
            />

            {!file ? (
              <div className="dropzone-content">
                <div className="upload-icon">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="12" y1="18" x2="12" y2="12"/>
                    <polyline points="9 15 12 12 15 15"/>
                  </svg>
                </div>
                <h3>Drag & Drop file here</h3>
                <p>Or click to browse your files</p>
                <span className="file-hint">Supports PDF, DOCX, TXT (Max 5MB)</span>
              </div>
            ) : (
              <div className="selected-file-card" onClick={(e) => e.stopPropagation()}>
                <div className="file-info-header">
                  <div className="file-icon-badge">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                  </div>
                  <div className="file-details">
                    <h4 className="file-name">{file.name}</h4>
                    <p className="file-size">{formatBytes(file.size)}</p>
                  </div>
                </div>
                <button
                  className="btn-remove-file"
                  onClick={handleClear}
                  disabled={loading}
                  title="Remove file"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            )}
          </div>
          {fileError && <div className="file-upload-error">{fileError}</div>}
        </div>
      )}

      <div className="text-input-actions">
        <button
          className="btn btn-primary btn-lg"
          onClick={handleAnalyze}
          disabled={loading || (activeTab === 'text' ? text.trim().length < 20 : !file)}
          id="analyze-btn"
        >
          {loading ? (
            <>
              <span className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }}></span>
              Analyzing...
            </>
          ) : (
            <>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              Analyze Content
            </>
          )}
        </button>

        <button
          className="btn btn-secondary"
          onClick={handleClear}
          disabled={loading || (activeTab === 'text' ? !text : !file)}
          id="clear-btn"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
          {activeTab === 'text' ? 'Clear Text' : 'Remove File'}
        </button>
      </div>

      {activeTab === 'text' && (
        <p className="text-hint">
          💡 Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to analyze
        </p>
      )}
    </div>
  );
}

