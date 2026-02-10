import { type CSSProperties, type ReactNode } from 'react'

type GradientTextProps = {
  children: ReactNode
  className?: string
  colors?: string[]
  animationSpeed?: number
}

export function GradientText({
  children,
  className,
  colors = ['#8bc2ff', '#6d79ff', '#54d2ff'],
  animationSpeed = 2.5,
}: GradientTextProps) {
  const gradient = `linear-gradient(120deg, ${colors.join(', ')})`
  const style = {
    '--rb-gradient': gradient,
    '--rb-speed': `${animationSpeed}s`,
  } as CSSProperties

  return (
    <span className={`gradient-text ${className ?? ''}`.trim()} style={style}>
      {children}
    </span>
  )
}
