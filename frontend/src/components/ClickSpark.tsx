import { useMemo, useState, type PointerEventHandler, type ReactNode } from 'react'

type Spark = {
  id: number
  x: number
  y: number
  angle: number
}

type ClickSparkProps = {
  children: ReactNode
  sparkColor?: string
  sparkCount?: number
  sparkRadius?: number
}

export function ClickSpark({ children, sparkColor = '#8bc2ff', sparkCount = 8, sparkRadius = 28 }: ClickSparkProps) {
  const [sparks, setSparks] = useState<Spark[]>([])
  const lifespan = 450

  const angles = useMemo(() => Array.from({ length: sparkCount }, (_, i) => (i * 360) / sparkCount), [sparkCount])

  const onPointerDown: PointerEventHandler<HTMLDivElement> = (event) => {
    const bounds = event.currentTarget.getBoundingClientRect()
    const x = event.clientX - bounds.left
    const y = event.clientY - bounds.top
    const idBase = Date.now()
    const next = angles.map((angle, index) => ({ id: idBase + index, x, y, angle }))

    setSparks((prev) => [...prev, ...next])
    window.setTimeout(() => {
      setSparks((prev) => prev.filter((spark) => !next.some((n) => n.id === spark.id)))
    }, lifespan)
  }

  return (
    <div className="click-spark" onPointerDown={onPointerDown}>
      {children}
      {sparks.map((spark) => (
        <span
          key={spark.id}
          className="spark"
          style={{
            left: `${spark.x}px`,
            top: `${spark.y}px`,
            background: sparkColor,
            transform: `rotate(${spark.angle}deg) translateX(${sparkRadius}px)`,
          }}
        />
      ))}
    </div>
  )
}
