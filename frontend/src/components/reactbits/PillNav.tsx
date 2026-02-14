import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import './PillNav.css'

type PillNavItem = {
  label: string
  href: string
}

type PillNavProps = {
  logo: string
  logoAlt?: string
  items: PillNavItem[]
  activeHref: string
  className?: string
}

const isExternalLink = (href: string) =>
  href.startsWith('http://') ||
  href.startsWith('https://') ||
  href.startsWith('//') ||
  href.startsWith('mailto:') ||
  href.startsWith('tel:') ||
  href.startsWith('#')

export default function PillNav({ logo, logoAlt = '36 Cowork', items, activeHref, className = '' }: PillNavProps) {
  const [mobileOpen, setMobileOpen] = useState(false)

  const navItems = useMemo(() => items.filter((item) => item.href !== '/'), [items])

  const isActive = (href: string) => activeHref === href || activeHref.startsWith(`${href}/`)

  return (
    <div className={`rb-pill-nav-wrap ${className}`}>
      <nav className="rb-pill-nav" aria-label="Primary">
        <Link className="rb-pill-logo" to="/" aria-label="Home">
          <img src={logo} alt={logoAlt} />
        </Link>

        <ul className="rb-pill-list rb-pill-desktop" role="menubar">
          {navItems.map((item) => (
            <li key={item.href} role="none">
              {isExternalLink(item.href) ? (
                <a
                  className={`rb-pill-link ${isActive(item.href) ? 'is-active' : ''}`}
                  href={item.href}
                  role="menuitem"
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </a>
              ) : (
                <Link
                  className={`rb-pill-link ${isActive(item.href) ? 'is-active' : ''}`}
                  to={item.href}
                  role="menuitem"
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </Link>
              )}
            </li>
          ))}
        </ul>

        <button
          className={`rb-pill-toggle rb-pill-mobile ${mobileOpen ? 'is-open' : ''}`}
          type="button"
          aria-expanded={mobileOpen}
          aria-label="Toggle navigation menu"
          onClick={() => setMobileOpen((prev) => !prev)}
        >
          <span />
          <span />
        </button>
      </nav>

      <div className={`rb-pill-popover rb-pill-mobile ${mobileOpen ? 'is-open' : ''}`}>
        <ul className="rb-pill-mobile-list">
          {items.map((item) => (
            <li key={item.href}>
              {isExternalLink(item.href) ? (
                <a
                  className={`rb-pill-mobile-link ${isActive(item.href) ? 'is-active' : ''}`}
                  href={item.href}
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </a>
              ) : (
                <Link
                  className={`rb-pill-mobile-link ${isActive(item.href) ? 'is-active' : ''}`}
                  to={item.href}
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </Link>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
