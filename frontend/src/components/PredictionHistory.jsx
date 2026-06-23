/**
 * PredictionHistory — Table displaying past prediction records.
 */
export default function PredictionHistory({ predictions, page, totalPages, onPageChange }) {
  if (!predictions || predictions.length === 0) {
    return (
      <div className="empty-state">
        <span style={{ fontSize: '2.5rem' }}>📋</span>
        <p>No prediction history yet. Analyze some text to get started!</p>
      </div>
    );
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      // Brief visual feedback would be nice, but keeping it simple
    });
  };

  return (
    <div>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Text Snippet</th>
              <th>Prediction</th>
              <th>AI Prob</th>
              <th>Words</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td className="snippet-cell" title={p.text_snippet}>
                  {p.text_snippet.length > 60
                    ? p.text_snippet.substring(0, 60) + '...'
                    : p.text_snippet}
                </td>
                <td>
                  <span className={`badge ${
                    p.prediction === 'AI Generated' ? 'badge-danger' : 'badge-success'
                  }`}>
                    {p.prediction === 'AI Generated' ? '🤖' : '✍️'} {p.prediction}
                  </span>
                </td>
                <td>
                  <strong>{Math.round(p.ai_probability * 100)}%</strong>
                </td>
                <td>{p.word_count}</td>
                <td className="text-small text-muted">{formatDate(p.created_at)}</td>
                <td>
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => handleCopy(
                      `Prediction: ${p.prediction}\nAI: ${Math.round(p.ai_probability * 100)}%\nHuman: ${Math.round(p.human_probability * 100)}%`
                    )}
                    title="Copy result"
                  >
                    📋
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
          >
            ← Previous
          </button>
          <span className="page-info">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
}
