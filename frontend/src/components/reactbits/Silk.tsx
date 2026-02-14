import { useMemo } from 'react'

type SilkProps = {
  speed?: number
  scale?: number
  color?: string
  noiseIntensity?: number
  rotation?: number
}

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value))

const hexToRgb = (hex: string) => {
  const normalized = hex.replace('#', '').padEnd(6, '0').slice(0, 6)
  const r = parseInt(normalized.slice(0, 2), 16)
  const g = parseInt(normalized.slice(2, 4), 16)
  const b = parseInt(normalized.slice(4, 6), 16)
  return { r, g, b }
}

export default function Silk({
  speed = 4.6,
  scale = 0.95,
  color = '#39006c',
  noiseIntensity = 0,
  rotation = 0.15,
}: SilkProps) {
  const style = useMemo(() => {
    const { r, g, b } = hexToRgb(color)
    const alphaA = clamp(0.4 + noiseIntensity * 0.03, 0.2, 0.65)
    const alphaB = clamp(0.24 + noiseIntensity * 0.02, 0.12, 0.44)
    const alphaC = clamp(0.2 + noiseIntensity * 0.015, 0.1, 0.34)
    const duration = `${clamp(26 - speed * 2, 12, 34)}s`
    const zoom = clamp(scale, 0.65, 1.5)
    const rotateDeg = `${rotation * 30}deg`

    return {
      ['--silk-rgb' as string]: `${r}, ${g}, ${b}`,
      ['--silk-alpha-a' as string]: String(alphaA),
      ['--silk-alpha-b' as string]: String(alphaB),
      ['--silk-alpha-c' as string]: String(alphaC),
      ['--silk-duration' as string]: duration,
      ['--silk-zoom' as string]: String(zoom),
      ['--silk-rotation' as string]: rotateDeg,
    } as React.CSSProperties
  }, [color, noiseIntensity, rotation, scale, speed])

  return (
    <div className="rb-silk" style={style} aria-hidden>
      <div className="rb-silk-layer rb-silk-layer-a" />
      <div className="rb-silk-layer rb-silk-layer-b" />
      <div className="rb-silk-layer rb-silk-layer-c" />
    </div>
  )
}
