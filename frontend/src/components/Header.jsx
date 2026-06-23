import ThemeToggle from './ThemeToggle';

/**
 * Header — Top navigation bar with logo, nav tabs, and theme toggle.
 */
export default function Header({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'model', label: 'About Model', icon: '🧠' },
    { id: 'admin', label: 'Admin', icon: '⚙️' },
  ];

  return (
    <header className="header">
      <div className="container header-inner">
        {/* Logo & Title */}
        <div className="header-brand">
          <div className="header-logo">
            <svg width="32" height="32" viewBox="0 0 40 40" fill="none">
              <rect width="40" height="40" rx="10" fill="var(--primary)"/>
              <path d="M20 8L30 14V26L20 32L10 26V14L20 8Z" fill="none" stroke="white" strokeWidth="2"/>
              <circle cx="20" cy="20" r="4" fill="white"/>
              <path d="M20 12V16M20 24V28M12.5 16L16 18M24 22L27.5 24M12.5 24L16 22M24 18L27.5 16" stroke="white" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
          </div>
          <div className="header-title-group">
            <h1 className="header-title">AI Academic Detector</h1>
            <span className="header-subtitle">Content Authenticity Analysis</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="header-nav">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => onTabChange(tab.id)}
              id={`nav-${tab.id}`}
            >
              <span className="nav-tab-icon">{tab.icon}</span>
              <span className="nav-tab-label">{tab.label}</span>
            </button>
          ))}
        </nav>

        {/* Theme Toggle */}
        <ThemeToggle />
      </div>
    </header>
  );
}
