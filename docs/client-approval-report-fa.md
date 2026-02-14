# گزارش جامع وضعیت محصول برای تایید کارفرما

## 1) خلاصه اجرایی
این پروژه به معماری `Django API/Admin + React SPA (Vite)` مهاجرت داده شده و اکنون فرانت‌اند کاربر نهایی به‌طور کامل روی React اجرا می‌شود.  
Django فقط مسئول API، پنل ادمین، احراز هویت سشن/CSRF، قوانین کسب‌وکار و سرویس‌های SEO زیرساختی است.

خروجی فعلی شامل:
- مسیرهای کامل کاربری (خانه، احراز هویت، پروفایل، کافه، کوورک)
- مسیرهای کامل پنل کارکنان (سفارش‌ها، سفارش دستی، مدیریت منو، مشتریان، تحلیل‌ها، کاربران)
- ماژول بلاگ و فریلنسرها (عمومی + بخش مالک)
- SEO پایه در SPA + `sitemap.xml` و `robots.txt`

---

## 2) معماری نهایی سیستم
### بک‌اند
- فریم‌ورک: `Django 5.2`
- API: `Django REST Framework`
- اپ‌ها: `accounts`, `blog`, `cafe`, `cowork`
- پنل مدیریت: `Django Admin`
- احراز هویت: Session-based + CSRF
- تاریخ جلالی: `django-jalali`, `jdatetime`
- Middleware سفارشی:
  - `RequestIDMiddleware` (افزودن `X-Request-ID`)
  - `ContentSecurityPolicyMiddleware` (اعمال CSP)

### فرانت‌اند
- فریم‌ورک: `React 18 + TypeScript`
- باندلر: `Vite 6`
- مسیرها: `react-router-dom`
- انیمیشن/تعاملات: `motion`, `gsap`
- آیکن‌ها: `@mui/icons-material`
- تاریخ جلالی: `react-multi-date-picker`
- کامپوننت‌های بصری (ReactBits/سفارشی):
  - `Silk` (پس‌زمینه سراسری)
  - `PillNav` (ناوبری موبایل)
  - `Stepper` (ثبت‌نام چندمرحله‌ای)
  - `GlareHover` (افکت hover روی کارت‌ها)

### مدل استقرار
- Same-origin reverse proxy
  - `/api/*`, `/admin/*`, `/media/*`, `/static/*`, `/sitemap.xml`, `/robots.txt` -> Django
  - سایر مسیرها -> React `index.html` (SPA fallback)
- مرجع کانفیگ: `deploy/nginx/react-django-cutover.conf`

---

## 3) استک تکنولوژی
### Python
- `django==5.2.9`
- `djangorestframework==3.16.1`
- `django-jalali==7.4.0`
- `pytest`, `pytest-django`, `pytest-cov`
- `factory-boy`, `faker`
- `pillow`

### Frontend
- `react`, `react-dom`, `typescript`, `vite`
- `@mui/material`, `@mui/icons-material`, `@emotion/*`
- `motion`, `gsap`
- `three`, `@react-three/fiber`
- `vitest`, `@testing-library/*`, `jsdom`

---

## 4) مسیرهای فرانت‌اند (Route Parity)
- `/`
- `/login/`
- `/register/`
- `/profile/`
- `/blog/`
- `/blog/:slug/`
- `/freelancers/`
- `/freelancers/:slug/`
- `/cafe/menu/`
- `/cafe/cart/`
- `/cafe/checkout/`
- `/cafe/orders/`
- `/cowork/`
- `/cowork/book/:spaceId`
- `/cowork/my-bookings/`
- `/cafe/dashboard/`
- `/cafe/manual-order/`
- `/cafe/manage-menu/`
- `/cafe/lookup/`
- `/cafe/analytics/`
- `/staff/users/`

---

## 5) APIهای پیاده‌سازی‌شده
### Auth
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `POST /api/auth/register/`
- `GET /api/auth/me/`
- `GET/PATCH /api/auth/profile/`

### Cafe (عمومی/کاربر)
- `GET /api/cafe/menu/`
- `GET /api/cafe/cart/`
- `POST /api/cafe/cart/items/`
- `POST /api/cafe/checkout/`
- `GET /api/cafe/orders/`
- `POST /api/cafe/orders/{id}/reorder/`

### Cafe (Staff)
- `GET /api/cafe/staff/orders/`
- `POST /api/cafe/staff/orders/{id}/status/`
- `POST /api/cafe/staff/orders/{id}/toggle-payment/`
- `GET/POST /api/cafe/staff/menu-items/`
- `GET /api/cafe/staff/menu-categories/`
- `POST /api/cafe/staff/menu-items/{id}/toggle-availability/`
- `POST /api/cafe/staff/manual-orders/`
- `GET /api/cafe/staff/customer-lookup/`

### Cowork
- `GET /api/cowork/spaces/`
- `GET /api/cowork/bookings/preview/`
- `POST /api/cowork/bookings/`
- `GET /api/cowork/my-bookings/`

### Staff مرکزی
- `GET /api/staff/analytics/overview/`
- `GET /api/staff/users/`
- `PATCH /api/staff/users/{id}/status/`
- `PATCH /api/staff/users/{id}/role/`

### Blog
- `GET /api/blog/posts/`
- `GET /api/blog/posts/{slug}/`
- `GET /api/blog/tags/`

### Freelancers
- عمومی:
  - `GET /api/freelancers/`
  - `GET /api/freelancers/{slug}/`
  - `GET /api/freelancers/specialties/`
  - `GET /api/freelancers/flairs/`
- مالک پروفایل:
  - `GET/PATCH /api/auth/freelancer-profile/`
  - `POST /api/auth/freelancer-profile/submit/`
  - `GET /api/auth/freelancer-specialties/`
  - `GET /api/auth/freelancer-flairs/`
  - `POST /api/auth/freelancer-services/`
  - `PATCH/DELETE /api/auth/freelancer-services/{id}/`

### SEO زیرساختی
- `GET /sitemap.xml`
- `GET /robots.txt`

---

## 6) مدل داده و دامنه کسب‌وکار
### Accounts
- `CustomUser` با ورود بر پایه شماره موبایل
- نقش‌ها: `Admin`, `Barista`, `Customer`
- اعتبارسنجی کد ملی ایران

### دامنه فریلنسر
- `FreelancerProfile` (draft, pending_approval, published, rejected)
- `FreelancerSpecialtyTag`
- `FreelancerFlair`
- `FreelancerServiceOffering`
- قوانین:
  - slug عمومی با regex
  - تخصص‌های سفارشی حداکثر 10 مورد
  - dedupe و validation نوع کار
  - سقف سرویس‌ها: 20 مورد

### Cafe
- `MenuCategory`, `MenuItem`
- `CafeOrder`, `OrderItem`
- وضعیت سفارش: `PENDING`, `PREPARING`, `READY`, `DELIVERED`, `CANCELLED`

### Cowork
- `PricingPlan`, `Space`, `Booking`
- zoneها:
  - سیت روزانه
  - میز شخصی (تکی)
  - میز اشتراکی (۴ نفره)
  - اتاق VIP (۲ نفره)
  - اتاق VIP (۳ نفره)
  - اتاق جلسه
- رزروها در ابتدا `PENDING` و نیازمند تایید ادمین

### Blog
- `BlogPost`, `BlogTag`
- محتوا با `content_blocks` نوع‌دار
- فیلدهای SEO/GEO

---

## 7) قابلیت‌های پیاده‌سازی‌شده (Product Features)
### احراز هویت و پروفایل
- ثبت‌نام و ورود کاربر
- مدیریت session در React (`AuthContext`)
- محافظت مسیرهای کاربری و کارکنان (`AuthGuard`, `StaffGuard`)
- ویرایش پروفایل پایه
- مدیریت پروفایل فریلنسر (ویرایش، سرویس‌ها، ارسال برای تایید)

### کافه (سمت کاربر)
- منوی دسته‌بندی‌شده
- نوار چسبان دسته‌بندی‌ها با اسکرول افقی
- سبد خرید + افزودن/کاهش تعداد آیتم
- Checkout
- تاریخچه سفارش‌ها + سفارش مجدد

### کافه (سمت کارکنان)
- داشبورد سفارش‌های فعال
- تغییر وضعیت سفارش و تغییر وضعیت پرداخت
- مدیریت منو (افزودن آیتم، تغییر availability)
- جستجوی مشتری
- ثبت سفارش دستی:
  - جستجو مشتری با نام یا شماره (autocomplete)
  - انتخاب آیتم از منو (به‌جای ID)
  - کنترل تعداد آیتم‌ها
  - انتخاب نوع مشتری از dropdown
  - پیشنهاد آیتم‌ها بر اساس محبوبیت فروش (Sales rate ranking)

### کوورک
- نمایش زون‌ها و فضاها با کارت‌های collapsible
- برای میز اشتراکی: انتخاب صندلی داخلی
- رزرو با پیش‌نمایش قیمت
- تاریخ جلالی و نمایش بازه رزرو
- پیام رزرو «نیازمند تایید نهایی/تماس»
- صفحه رزروهای من

### بلاگ
- لیست پست‌ها + فیلتر و جستجو
- نمایش جزئیات پست با بلاک‌های محتوا
- نمایش مطالب مرتبط

### فریلنسرها
- لیست عمومی فریلنسرها با فیلتر
- صفحه عمومی هر فریلنسر (خدمات، تگ‌ها، flair)

### مدیریت کاربران Staff/Admin
- لیست کاربران با paging/filter
- تغییر نقش کاربر
- تغییر وضعیت فعال/غیرفعال

---

## 8) UI/UX و دیزاین سیستم
- RTL کامل و فارسی
- پس‌زمینه سراسری جدید با `Silk` (تم تیره و eye-friendly)
- سایدبار دسکتاپ + `PillNav` برای موبایل
- کارت‌های شیشه‌ای + Glare hover برای کارت‌های منو/کوورک
- بازطراحی منوی کافه:
  - دسته‌بندی‌های افقی
  - حالت active دسته
  - اسکرول چپ/راست
- placeholder تصویر برای آیتم‌های منو
- فرم ثبت‌نام چندمرحله‌ای با `Stepper`
- پولیش dropdown و scrollbar فرم سفارش دستی

---

## 9) SEO/GEO
- `SeoHead` برای مدیریت:
  - title
  - description
  - canonical
  - Open Graph
  - JSON-LD
- JSON-LD مقاله در صفحه بلاگ (`Article`)
- JSON-LD فرد در صفحه فریلنسر (`Person`)
- `sitemap.xml` پویا (خانه، بلاگ، فریلنسرهای منتشرشده)
- `robots.txt`

---

## 10) امنیت و تنظیمات کلیدی
- Session + CSRF محفوظ
- `credentials: include` در فراخوانی‌های API
- `CSRF_TRUSTED_ORIGINS` برای dev:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`
- CSP قابل تنظیم با `DJANGO_CSP`
- هدر ردیابی درخواست: `X-Request-ID`

---

## 11) Seed و دستورات عملیاتی
### Python
- `uv sync`
- `uv run python manage.py migrate`
- `uv run python manage.py runserver`

### Frontend
- `cd frontend && npm install`
- `cd frontend && npm run dev`
- `cd frontend && npm run build`

### Seed/Init
- `uv run python manage.py init_roles`
- `uv run python manage.py import_menu --file "36 menu.csv"`
- `uv run python manage.py seed_spaces`
- `uv run python manage.py seed_freelancer_taxonomy`

---

## 12) تست و کنترل کیفیت
### Backend
- `uv run pytest`
- پوشش تست در:
  - accounts (API/RBAC/Normalization/Freelancer/Staff)
  - cafe (SPA API)
  - cowork (Logic/Forms/SPA API)
  - blog

### Frontend
- `cd frontend && npm run test`
- تست‌های مسیر و رفتار فرم/API

### Build gate
- `cd frontend && npm run build`

---

## 13) خروجی‌ها و اسناد مرجع
- `README.md`
- `docs/cutover-checklist.md`
- `deploy/nginx/react-django-cutover.conf`
- `config/settings.py`
- `config/urls.py`
- `config/seo_views.py`
- `frontend/src/App.tsx`
- `frontend/src/layouts/AppShell.tsx`

---

## 14) ضمیمه تصویری (Screenshots)
> منبع تصاویر: محیط اجرای فعلی روی `http://localhost:5173/`  
> مسیر ذخیره: `output/playwright/`

### نمای دسکتاپ
#### خانه
![Home Desktop](../output/playwright/home-desktop.png)
[نمایش با اندازه کامل](../output/playwright/home-desktop.png)

#### منوی کافه
![Cafe Menu Desktop](../output/playwright/cafe-menu-desktop.png)
[نمایش با اندازه کامل](../output/playwright/cafe-menu-desktop.png)

#### فضای کاری
![Cowork Desktop](../output/playwright/cowork-desktop.png)
[نمایش با اندازه کامل](../output/playwright/cowork-desktop.png)

#### سفارش دستی (پنل کافه)
![Manual Order Desktop](../output/playwright/manual-order-desktop.png)
[نمایش با اندازه کامل](../output/playwright/manual-order-desktop.png)

#### داشبورد سفارش‌ها (Staff)
![Staff Dashboard Desktop](../output/playwright/staff-dashboard-desktop.png)
[نمایش با اندازه کامل](../output/playwright/staff-dashboard-desktop.png)

#### ثبت‌نام
![Register Desktop](../output/playwright/register-desktop.png)
[نمایش با اندازه کامل](../output/playwright/register-desktop.png)

### نمای موبایل (Viewport شبیه‌سازی‌شده: `390x844`)
#### خانه
![Home Mobile](../output/playwright/home-mobile.png)
[نمایش با اندازه کامل](../output/playwright/home-mobile.png)

#### منوی کافه
![Cafe Menu Mobile](../output/playwright/cafe-menu-mobile.png)
[نمایش با اندازه کامل](../output/playwright/cafe-menu-mobile.png)

#### فضای کاری
![Cowork Mobile](../output/playwright/cowork-mobile.png)
[نمایش با اندازه کامل](../output/playwright/cowork-mobile.png)

#### سفارش دستی (پنل کافه)
![Manual Order Mobile](../output/playwright/manual-order-mobile.png)
[نمایش با اندازه کامل](../output/playwright/manual-order-mobile.png)

#### ثبت‌نام
![Register Mobile](../output/playwright/register-mobile.png)
[نمایش با اندازه کامل](../output/playwright/register-mobile.png)

---

## 15) فرض‌ها و پیش‌فرض‌های فعلی
- نسخه فعلی محصول فارسی‌محور است.
- SEO فعلی از نوع SPA Meta/JSON-LD + Sitemap/Robots است (بدون SSR).
- فرآیند تایید نهایی رزرو کوورک توسط ادمین انجام می‌شود.
- انتشار بلاگ در نسخه فعلی از طریق Django Admin انجام می‌شود.
- پروکسی هم‌مبدأ برای Production الزامی در نظر گرفته شده است.
