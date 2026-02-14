type TagChipProps = {
  label: string
}

export function TagChip({ label }: TagChipProps) {
  return <span className="tag-chip">{label}</span>
}

