import './GooeyNav.css';

const GooeyNav = ({ items = [], activeIndex = 0, className = '' }) => {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const count = Math.max(items.length, 1);
  const clampedIndex = Math.max(0, Math.min(activeIndex, count - 1));

  return (
    <div className={`gooey-nav ${prefersReduced ? 'is-reduced' : ''} ${className}`.trim()}>
      <svg className="gooey-nav__filter" aria-hidden="true" focusable="false">
        <filter id="gooey-nav-filter">
          <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur" />
          <feColorMatrix
            in="blur"
            mode="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
            result="gooey"
          />
          <feComposite in="SourceGraphic" in2="gooey" operator="atop" />
        </filter>
      </svg>
      <div
        className="gooey-nav__track"
        style={{ '--item-count': count, '--active-index': clampedIndex }}
        role="navigation"
        aria-label="ناوبری اصلی"
      >
        <span className="gooey-nav__indicator" aria-hidden="true"></span>
        {items.map((item, index) => {
          const isActive = index === clampedIndex;
          return (
            <a
              key={`${item.label}-${index}`}
              href={item.href}
              className={`gooey-nav__item ${isActive ? 'is-active' : ''}`.trim()}
              aria-current={isActive ? 'page' : undefined}
            >
              <span className="gooey-nav__icon" aria-hidden="true">
                {item.icon}
              </span>
              <span className="gooey-nav__label">{item.label}</span>
              {item.badgeId ? (
                <span
                  id={item.badgeId}
                  className={`gooey-nav__badge ${item.badgeHidden ? 'hidden' : ''}`.trim()}
                >
                  {item.badgeValue ?? 0}
                </span>
              ) : null}
            </a>
          );
        })}
      </div>
    </div>
  );
};

export default GooeyNav;
