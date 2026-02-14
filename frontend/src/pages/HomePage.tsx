import { Link } from 'react-router-dom'

const highlights = [
  'فضای کاری آرام، حرفه‌ای و مناسب تمرکز',
  'اینترنت پایدار و تجهیزات کامل روزمره',
  'کافه با منوی متنوع نوشیدنی و غذا',
  'موقعیت عالی در قلب شهر و دسترسی آسان',
]

const galleryTiles = [
  { src: '/img/landing/36-1.jpg', alt: 'فضای داخلی ۳۶ کوورک' },
  { src: '/img/landing/36-2.jpg', alt: 'محیط کار تیمی' },
  { src: '/img/landing/36-3.jpg', alt: 'میزهای کار' },
  { src: '/img/landing/36-4.jpg', alt: 'اتاق جلسه' },
  { src: '/img/landing/36-5.jpg', alt: 'فضای باز' },
  { src: '/img/landing/azno-20975-1.webp', alt: 'محیط مشترک' },
  { src: '/img/landing/azno-20975-2.webp', alt: 'نور طبیعی' },
  { src: '/img/landing/azno-20975-3.webp', alt: 'فضای کار حرفه‌ای' },
]

const serviceRibbon = ['Coworking', 'Meeting Rooms', 'Cafe', 'Events', 'Private Desk']

const serviceBlocks = [
  {
    title: 'فضای کار اشتراکی',
    description: 'میزهای کاری متنوع با چیدمان حرفه‌ای و امکانات کامل برای بهره‌وری روزانه افراد و تیم‌ها.',
    image: '/img/landing/36-3.jpg',
  },
  {
    title: 'کافه و منوی اختصاصی',
    description: 'کافه باکیفیت با منوی کامل نوشیدنی و خوراک برای استراحت، جلسات کوتاه و کار عمیق.',
    image: '/img/landing/36-2.jpg',
  },
  {
    title: 'اتاق جلسه و رویداد',
    description: 'از جلسات رسمی تا ورکشاپ‌های تیمی، فضاهای متنوع ما برای همکاری و ارائه آماده هستند.',
    image: '/img/landing/azno-20975-3.webp',
  },
]

export function HomePage() {
  return (
    <section className="page-stack landing-root evo-landing">
      <section className="evo-hero">
        <div className="evo-copy">
          <p className="eyebrow">36 Cowork</p>
          <h2>فضایی برای تجربه کاری حرفه‌ای در کنار یک جامعه پویا</h2>
          <p className="evo-lead">
            همین حالا فضای کاری خودت را رزرو کن و با امکانات استاندارد، تمرکز بیشتر و تجربه‌ای متفاوت کار کن.
          </p>
          <div className="row evo-actions">
            <Link to="/cowork/" className="btn-primary">
              رزرو فضا
            </Link>
            <Link to="/cafe/menu/" className="btn-secondary">
              منوی کافه
            </Link>
          </div>
          <ul className="evo-metrics">
            <li>
              <strong>24/7</strong>
              <span>دسترسی</span>
            </li>
            <li>
              <strong>150+</strong>
              <span>عضو فعال</span>
            </li>
            <li>
              <strong>8</strong>
              <span>فضای متنوع</span>
            </li>
          </ul>
        </div>
        <div className="evo-hero-media">
          <img src="/img/landing/36-1.jpg" alt="فضای داخلی ۳۶ کوورک" className="evo-main-image" loading="eager" />
          <img src="/img/landing/36-4.jpg" alt="اتاق جلسه" className="evo-float-image evo-float-a" loading="lazy" />
          <img src="/img/landing/azno-20975-2.webp" alt="نور طبیعی" className="evo-float-image evo-float-b" loading="lazy" />
        </div>
      </section>

      <section className="evo-ribbon" aria-label="خدمات اصلی">
        {serviceRibbon.map((item) => (
          <p key={item}>{item}</p>
        ))}
      </section>

      <section className="evo-editorial-lead" aria-label="متن معرفی">
        <p>
          ما اینجا فقط یک میز برای کار نمی‌دهیم. تجربه‌ای می‌سازیم که تمرکز، ارتباط و رشد حرفه‌ای شما را همزمان تقویت کند.
        </p>
        <div className="row evo-actions">
          <Link to="/cowork/" className="btn-primary">
            مشاهده فضاها
          </Link>
          <Link to="/register/" className="btn-secondary">
            ثبت‌نام سریع
          </Link>
        </div>
      </section>

      <section className="evo-services" aria-label="ویژگی‌های فضا">
        {serviceBlocks.map((service) => (
          <article key={service.title} className="evo-service-strip">
            <img src={service.image} alt={service.title} className="evo-service-image" loading="lazy" />
            <div className="evo-service-copy">
              <h3>{service.title}</h3>
              <p>{service.description}</p>
            </div>
          </article>
        ))}
      </section>

      <section className="evo-wide-image" aria-label="تصویر شاخص">
        <img src="/img/landing/36-5.jpg" alt="نمای کلی از فضای کاری اشتراکی" loading="lazy" />
        <div className="evo-wide-caption">
          <p className="eyebrow">Open Workspace</p>
          <h3>چیدمان فضا برای همکاری، تمرکز و حرکت طبیعی بین کار عمیق و تعامل تیمی</h3>
        </div>
      </section>

      <section className="evo-two-column" aria-label="درباره ما">
        <div className="evo-text-block">
          <p className="eyebrow">Why 36 Cowork</p>
          <h3>ترکیب طراحی هوشمند فضا، خدمات کامل و تجربه حرفه‌ای</h3>
          <p>
            از اولین ورود تا پایان روز کاری، همه‌چیز برای یک تجربه روان طراحی شده است: اینترنت پایدار، محیط آرام، کافه فعال و
            پشتیبانی دقیق.
          </p>
          <ul className="landing-editorial-list">
            {highlights.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="evo-side-rail">
          <img src="/img/landing/azno-20975-1.webp" alt="فضای مشترک" className="evo-side-image" loading="lazy" />
          <p>برای رزرو میز، اتاق جلسه یا دریافت مشاوره، مسیر رزرو را شروع کنید و گزینه مناسب خودتان را انتخاب کنید.</p>
          <Link to="/cowork/" className="btn-secondary">
            اینجا کلیک کنید
          </Link>
        </div>
      </section>

      <section className="evo-editorial-break" aria-label="جمع‌بندی معرفی">
        <p>
          هر چیزی که برای یک روز کاری حرفه‌ای نیاز دارید در ۳۶ کوورک فراهم شده است. اگر به دنبال محیطی جدی، راحت و الهام‌بخش
          هستید، اینجا انتخاب مطمئن شماست.
        </p>
      </section>

      <section className="evo-gallery-grid" aria-label="گالری تصاویر">
        {galleryTiles.map((tile) => (
          <figure key={tile.src} className="evo-gallery-item">
            <img src={tile.src} alt={tile.alt} className="gallery-image" loading="lazy" />
          </figure>
        ))}
      </section>
    </section>
  )
}
