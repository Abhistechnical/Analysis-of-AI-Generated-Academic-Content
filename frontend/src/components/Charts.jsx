import { Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

/**
 * Charts — Pie chart for probabilities and bar chart for feature importances.
 */
export default function Charts({ result }) {
  const aiPercent = Math.round(result.ai_probability * 100);
  const humanPercent = Math.round(result.human_probability * 100);

  // Read current theme
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textColor = isDark ? '#94a3b8' : '#475569';
  const gridColor = isDark ? '#1e293b' : '#e2e8f0';

  const pieData = {
    labels: ['AI Generated', 'Human Written'],
    datasets: [{
      data: [aiPercent, humanPercent],
      backgroundColor: [
        'rgba(239, 68, 68, 0.8)',
        'rgba(34, 197, 94, 0.8)',
      ],
      borderColor: [
        'rgba(239, 68, 68, 1)',
        'rgba(34, 197, 94, 1)',
      ],
      borderWidth: 2,
      hoverOffset: 6,
    }],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: textColor,
          padding: 16,
          font: { family: 'Inter', size: 13, weight: '500' },
          usePointStyle: true,
          pointStyleWidth: 12,
        },
      },
      tooltip: {
        backgroundColor: isDark ? '#1e293b' : '#0f172a',
        titleFont: { family: 'Inter', size: 13 },
        bodyFont: { family: 'Inter', size: 12 },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: (ctx) => `${ctx.label}: ${ctx.raw}%`,
        },
      },
    },
  };

  // Feature importance bar chart
  const featureLabels = result.feature_importances.map(f => f.name);
  const featureScores = result.feature_importances.map(f => f.score);

  const barData = {
    labels: featureLabels,
    datasets: [{
      label: 'Importance Score',
      data: featureScores,
      backgroundColor: featureScores.map((_, i) => {
        const colors = [
          'rgba(37, 99, 235, 0.7)',
          'rgba(14, 165, 233, 0.7)',
          'rgba(6, 182, 212, 0.7)',
          'rgba(20, 184, 166, 0.7)',
          'rgba(16, 185, 129, 0.7)',
          'rgba(34, 197, 94, 0.7)',
          'rgba(132, 204, 22, 0.7)',
          'rgba(245, 158, 11, 0.7)',
        ];
        return colors[i % colors.length];
      }),
      borderColor: featureScores.map((_, i) => {
        const colors = [
          'rgba(37, 99, 235, 1)',
          'rgba(14, 165, 233, 1)',
          'rgba(6, 182, 212, 1)',
          'rgba(20, 184, 166, 1)',
          'rgba(16, 185, 129, 1)',
          'rgba(34, 197, 94, 1)',
          'rgba(132, 204, 22, 1)',
          'rgba(245, 158, 11, 1)',
        ];
        return colors[i % colors.length];
      }),
      borderWidth: 1,
      borderRadius: 6,
    }],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: isDark ? '#1e293b' : '#0f172a',
        titleFont: { family: 'Inter', size: 13 },
        bodyFont: { family: 'Inter', size: 12 },
        padding: 12,
        cornerRadius: 8,
        callbacks: {
          label: (ctx) => `Score: ${(ctx.raw * 100).toFixed(1)}%`,
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        max: Math.max(...featureScores) * 1.2 || 1,
        grid: { color: gridColor },
        ticks: {
          color: textColor,
          font: { family: 'Inter', size: 11 },
          callback: (v) => `${(v * 100).toFixed(0)}%`,
        },
      },
      y: {
        grid: { display: false },
        ticks: {
          color: textColor,
          font: { family: 'Inter', size: 12, weight: '500' },
        },
      },
    },
  };

  return (
    <div className="card">
      <div className="card-header">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>
          <path d="M22 12A10 10 0 0 0 12 2v10z"/>
        </svg>
        <h3>Visualizations</h3>
      </div>
      <div className="card-body">
        <div className="charts-grid">
          <div className="chart-container">
            <h4 className="section-title">AI vs Human Probability</h4>
            <div className="chart-wrapper pie-wrapper">
              <Pie data={pieData} options={pieOptions} />
            </div>
          </div>
          <div className="chart-container">
            <h4 className="section-title">Feature Importance</h4>
            <div className="chart-wrapper bar-wrapper">
              <Bar data={barData} options={barOptions} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
