/**
 * StatsCard — Displays content statistics in a grid layout.
 */
export default function StatsCard({ statistics }) {
  const stats = [
    {
      label: 'Total Words',
      value: statistics.total_words,
      icon: '📝',
    },
    {
      label: 'Total Sentences',
      value: statistics.total_sentences,
      icon: '📄',
    },
    {
      label: 'Avg Sentence Length',
      value: statistics.avg_sentence_length,
      icon: '📏',
    },
    {
      label: 'Vocabulary Richness',
      value: `${statistics.vocabulary_richness}%`,
      icon: '📚',
    },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M18 20V10M12 20V4M6 20v-6"/>
        </svg>
        <h3>Content Statistics</h3>
      </div>
      <div className="card-body">
        <div className="stat-grid">
          {stats.map((stat, i) => (
            <div className="stat-item" key={i}>
              <div style={{ fontSize: '1.5rem', marginBottom: 8 }}>{stat.icon}</div>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
