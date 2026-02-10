import { Link } from 'react-router-dom'
import { ClickSpark } from '../components/ClickSpark'
import { FadeContent } from '../components/FadeContent'
import { GradientText } from '../components/GradientText'

const landingShots = [
  {
    src: '/img/36cowork/hero-space.webp',
    alt: 'نمای داخلی 36',
  },
  {
    src: '/img/36cowork/space-3.jpg',
    alt: 'سالن مشترک برای کار تیمی',
  },
  {
    src: '/img/azno/space-44147.webp',
    alt: 'فضای کار منتخب از azno',
  },
]

export function HomePage() {
  return (
    <ClickSpark sparkColor="#8bc2ff" sparkRadius={24} sparkCount={6}>
      <section className="page-stack">
        <FadeContent blur duration={650}>
          <div className="hero">
            <div className="hero-content">
              <p className="eyebrow">فضای کاری اشتراکی 36</p>
              <GradientText animationSpeed={2.5}>محیط کار برای تیم‌های خلاق و حرفه‌ای</GradientText>
              <p>همین تجربه فعلی حالا به صورت کامل روی فرانت React اجرا می‌شود.</p>
              <div className="row">
                <Link to="/cowork/" className="btn-primary">
                  <span>رزرو فضا</span>
                </Link>
                <Link to="/cafe/menu/" className="btn-secondary">
                  <span>منوی کافه</span>
                </Link>
              </div>
            </div>
            <img src="/img/36cowork/hero-space.webp" alt="cowork hero" />
          </div>
        </FadeContent>

        <section className="panel">
          <p className="eyebrow">گالری فضا</p>
          <div className="landing-gallery">
            {landingShots.map((shot) => (
              <article className="card card-tall" key={shot.src}>
                <img src={shot.src} alt={shot.alt} className="gallery-image" loading="lazy" />
                <p>{shot.alt}</p>
              </article>
            ))}
          </div>
        </section>

        <div className="grid cols-3">
          <article className="card card-tall card-hover-rise">
            <h3>فضای کار</h3>
            <p>اتاق‌ها و میزهای اشتراکی را براساس نیاز روزانه یا ساعتی انتخاب کنید.</p>
            <Link to="/cowork/">مشاهده فضاها</Link>
          </article>
          <article className="card card-tall card-hover-rise">
            <h3>کافه</h3>
            <p>منوی نوشیدنی و میان‌وعده را سریع ثبت کنید و سفارش خود را پیگیری کنید.</p>
            <Link to="/cafe/menu/">رفتن به منو</Link>
          </article>
          <article className="card card-tall card-hover-rise">
            <h3>حساب کاربری</h3>
            <p>پروفایل، سفارش‌ها و رزروهای خود را یکجا و با دسترسی سریع مدیریت کنید.</p>
            <Link to="/profile/">مشاهده پروفایل</Link>
          </article>
        </div>
      </section>
    </ClickSpark>
  )
}
