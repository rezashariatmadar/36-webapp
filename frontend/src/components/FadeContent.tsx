import { useEffect, useState, type CSSProperties } from 'react'

type FadeContentProps = {
  children: React.ReactNode
  blur?: boolean
  duration?: number
  delay?: number
  className?: string
}

export function FadeContent({ children, blur = false, duration = 450, delay = 0, className }: FadeContentProps) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const id = window.setTimeout(() => setVisible(true), delay)
    return () => window.clearTimeout(id)
  }, [delay])

  return (
    <div
      className={['fade-content', visible ? 'is-visible' : '', className ?? ''].join(' ').trim()}
      style={
        {
          '--fade-duration': `${duration}ms`,
          '--fade-blur': blur ? '8px' : '0px',
        } as CSSProperties
      }
    >
      {children}
    </div>
  )
}
