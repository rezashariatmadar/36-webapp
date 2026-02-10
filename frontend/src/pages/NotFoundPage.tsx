import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <section>
      <h2>صفحه پیدا نشد</h2>
      <Link to="/">بازگشت به خانه</Link>
    </section>
  )
}

