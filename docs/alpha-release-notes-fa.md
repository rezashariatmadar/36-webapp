# Alpha Release Notes (FA)

تاریخ: **2026-02-14**

## خلاصه نسخه
نسخه Alpha شامل مهاجرت کامل فرانت‌اند به React + Vite، حفظ بک‌اند Django برای API/Admin، و ارائه کامل قابلیت‌های کافه، کوورک، بلاگ، فریلنسرها و پنل کارکنان است.

---

## مهم‌ترین تغییرات محصول
## 1) مهاجرت معماری فرانت‌اند
- جایگزینی رندر template-based قدیمی با SPA کامل React.
- حفظ URLهای اصلی محصول.
- نگه‌داشتن Django به‌عنوان backend-only.

## 2) کافه
- منوی دسته‌بندی‌شده با نوار چسبان و پیمایش سریع دسته‌ها.
- سبد خرید، checkout، history سفارش‌ها.
- پنل Staff:
  - داشبورد سفارش‌های فعال
  - تغییر وضعیت سفارش
  - تغییر وضعیت پرداخت
  - مدیریت منو/availability
  - ثبت سفارش دستی با UX جدید:
    - جستجوی مشتری با نام/شماره
    - انتخاب آیتم از لیست به‌جای ID
    - انتخاب نوع مشتری با dropdown
    - رتبه‌بندی پیشنهاد آیتم‌ها بر اساس محبوبیت فروش

## 3) کوورک
- نمایش زون‌ها و فضاها با کارت‌های جمع‌شونده.
- انتخاب صندلی برای میزهای اشتراکی.
- پیش‌نمایش رزرو و قیمت.
- تاریخ جلالی در مسیر رزرو.
- رزروها با وضعیت اولیه pending و نیازمند تایید.

## 4) بلاگ
- لیست و جزئیات پست‌ها.
- پشتیبانی از بلوک‌های ساختاری محتوا.
- تگ‌ها، فیلترها، related posts.

## 5) فریلنسرها
- دایرکتوری عمومی فریلنسرها.
- صفحه عمومی هر فریلنسر.
- پروفایل مالک با workflow ارسال برای تایید.
- مدیریت خدمات، تخصص‌ها و flair.

## 6) SEO/GEO
- مدیریت title/meta/canonical/OG/JSON-LD در SPA.
- `sitemap.xml` و `robots.txt` در Django.

---

## تغییرات فنی کلیدی
- Frontend: React 18, TypeScript, Vite, React Router.
- Backend: Django 5.2 + DRF.
- Auth model: Session + CSRF.
- Deployment model: same-origin proxy.

---

## QA summary
- Backend tests: PASS (`79 passed`)
- Frontend tests: PASS (`14 passed`)
- Frontend build: PASS

---

## Known Non-Blocking Issues
1. هشدار chunk size در build فرانت (نیاز به code splitting).
2. هشدارهای future flags در React Router v7.
3. هشدار deprecation در factory_boy.

---

## راهنمای سریع اجرای محلی
- Backend:
  - `uv sync`
  - `uv run python manage.py migrate`
  - `uv run python manage.py runserver`
- Frontend:
  - `cd frontend && npm install`
  - `cd frontend && npm run dev`

---

## Assets و مستندات همراه نسخه
- گزارش کامل مشتری: `docs/client-approval-report-fa.md`
- PDF گزارش: `docs/client-approval-report-fa.pdf`
- اسکرین‌شات‌ها: `output/playwright/`
- چک‌لیست کات‌اور: `docs/cutover-checklist.md`
