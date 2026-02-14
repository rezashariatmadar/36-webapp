type PaginationProps = {
  page: number
  pageSize: number
  total: number
  onChange: (nextPage: number) => void
}

export function Pagination({ page, pageSize, total, onChange }: PaginationProps) {
  const totalPages = Math.max(Math.ceil(total / pageSize), 1)
  if (totalPages <= 1) return null

  return (
    <div className="pagination-row">
      <button className="btn-secondary" type="button" onClick={() => onChange(page - 1)} disabled={page <= 1}>
        قبلی
      </button>
      <span>
        صفحه {page} از {totalPages}
      </span>
      <button className="btn-secondary" type="button" onClick={() => onChange(page + 1)} disabled={page >= totalPages}>
        بعدی
      </button>
    </div>
  )
}

