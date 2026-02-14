# Alpha Release Readiness

تاریخ آماده‌سازی: **2026-02-14**

## 1) وضعیت کلی
- وضعیت: **Ready for Alpha (مشروط به Freeze و Tag)**
- دامنه: Django API/Admin + React SPA
- محیط هدف آلفا: Same-origin proxy (`/api|/admin|/media|/static` -> Django, سایر مسیرها -> React)

## 2) Gateهای انتشار (اجرا شده)
## Backend
- دستور: `uv run pytest`
- نتیجه: **PASS**
- جزئیات: `79 passed`
- نکته: هشدارهای `factory_boy` (غیر بلاک‌کننده برای آلفا)

## Frontend tests
- دستور: `cd frontend && npm run test`
- نتیجه: **PASS**
- جزئیات: `4 files, 14 tests passed`
- نکته: هشدار future flags مربوط به React Router v7 (غیر بلاک‌کننده)

## Frontend build
- دستور: `cd frontend && npm run build`
- نتیجه: **PASS**
- جزئیات: build موفق، خروجی `frontend/build`
- ریسک باز: main chunk بزرگ (`~1.36MB`) و هشدار chunk size

---

## 3) Go/No-Go Checklist
- [x] API backend پایدار و تست‌شده
- [x] مسیرهای کلیدی کاربر و Staff روی SPA فعال
- [x] احراز هویت session/CSRF فعال
- [x] SEO endpoints (`/sitemap.xml`, `/robots.txt`) فعال
- [x] اسناد انتشار و گزارش فارسی برای کارفرما آماده
- [x] اسکرین‌شات‌های محصول آماده
- [ ] Freeze نهایی تغییرات (stop feature churn)
- [ ] نسخه‌گذاری (`alpha` tag)
- [ ] استقرار staging/prod با کانفیگ Nginx نهایی
- [ ] Smoke دستی پس از deploy روی URL نهایی

---

## 4) موارد بلوکه‌کننده آلفا
در وضعیت فعلی، **Blocker فنی بحرانی مشاهده نشد**.  
موارد زیر برای Beta/GA پیشنهاد می‌شوند ولی آلفا را متوقف نمی‌کنند:

1. بهینه‌سازی bundle (split routes/components).
2. کاهش هشدارهای تست (factory_boy / React Router future flags).
3. اجرای smoke تصویری پس از هر deploy به‌صورت خودکار.

---

## 5) ریسک‌ها و کاهش ریسک
## ریسک 1: حجم بالای باندل فرانت
- اثر: زمان لود اولیه بالاتر در شبکه ضعیف
- کاهش ریسک:
  - route-level code splitting
  - `manualChunks` در Vite/Rollup
  - lazy load کامپوننت‌های سنگین

## ریسک 2: Worktree بسیار پر تغییر
- اثر: احتمال ورود تغییرات ناخواسته به ریلیز
- کاهش ریسک:
  - شاخه release جدا (`release/alpha-YYYYMMDD`)
  - commit کردن فقط فایل‌های scope ریلیز
  - review نهایی diff قبل از tag

## ریسک 3: وابستگی به پیکربندی صحیح proxy
- اثر: مشکلات session/csrf در prod
- کاهش ریسک:
  - استفاده دقیق از `deploy/nginx/react-django-cutover.conf`
  - sanity check endpointهای auth و csrf پس از deploy

---

## 6) Runbook انتشار آلفا
1. آخرین مهاجرت‌ها:
   - `uv run python manage.py migrate`
2. Seed پایه (در صورت نیاز محیط جدید):
   - `uv run python manage.py init_roles`
   - `uv run python manage.py import_menu --file "36 menu.csv"`
   - `uv run python manage.py seed_spaces`
   - `uv run python manage.py seed_freelancer_taxonomy`
3. Build فرانت:
   - `cd frontend && npm ci && npm run build`
4. تست:
   - `uv run pytest`
   - `cd frontend && npm run test`
5. استقرار با proxy هم‌مبدأ
6. Smoke نهایی:
   - `/`
   - `/login/`
   - `/register/`
   - `/cafe/menu/`
   - `/cowork/`
   - `/profile/`
   - Staff pages

---

## 7) معیار پذیرش Alpha
- کاربر عادی:
  - ثبت‌نام/ورود/پروفایل بدون خطا
  - جریان کامل کافه (منو -> سبد -> checkout -> orders)
  - جریان کامل کوورک (spaces -> preview -> booking -> my bookings)
- Staff:
  - مدیریت سفارش‌ها
  - ثبت سفارش دستی
  - مدیریت منو
  - تحلیل‌ها
  - مدیریت کاربران
- SEO:
  - دسترسی صحیح به `sitemap.xml` و `robots.txt`

---

## 8) اسناد مرتبط
- گزارش جامع برای کارفرما: `docs/client-approval-report-fa.md`
- نسخه PDF گزارش: `docs/client-approval-report-fa.pdf`
- چک‌لیست کات‌اور: `docs/cutover-checklist.md`
- کانفیگ پراکسی: `deploy/nginx/react-django-cutover.conf`
