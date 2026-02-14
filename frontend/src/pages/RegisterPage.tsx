import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Stepper, { Step } from '../components/reactbits/Stepper'
import { apiFetch } from '../lib/api/client'
import { useAuth } from '../lib/auth/AuthContext'

export function RegisterPage() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [nationalId, setNationalId] = useState('')
  const [activeStep, setActiveStep] = useState(1)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const { refresh } = useAuth()
  const navigate = useNavigate()

  const submitRegistration = async (event?: FormEvent) => {
    if (event) event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await apiFetch('/api/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone_number: phoneNumber,
          password,
          confirm_password: confirmPassword,
          full_name: fullName,
          national_id: nationalId,
        }),
      })
      await refresh()
      navigate('/')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setSubmitting(false)
    }
  }

  const canProceed = (step: number) => {
    setError('')
    if (step === 1 && !phoneNumber.trim()) {
      setError('شماره موبایل الزامی است.')
      return false
    }
    if (step === 3) {
      if (!password || !confirmPassword) {
        setError('رمز عبور و تکرار آن الزامی است.')
        return false
      }
      if (password !== confirmPassword) {
        setError('رمز عبور و تکرار آن یکسان نیستند.')
        return false
      }
    }
    return true
  }

  return (
    <section className="page-stack layout-flow-compact auth-layout">
      <div className="surface-open auth-head">
        <p className="eyebrow">شروع حساب</p>
        <h2>ثبت نام</h2>
        <p>اطلاعات را مرحله‌به‌مرحله وارد کنید تا حساب مشتری ساخته شود.</p>
      </div>
      <div className="surface-inline auth-form auth-surface">
        <Stepper
          initialStep={1}
          onStepChange={(step) => setActiveStep(step)}
          onFinalStepCompleted={() => {
            void submitRegistration()
          }}
          canProceed={canProceed}
          backButtonText="مرحله قبل"
          nextButtonText="مرحله بعد"
          completeButtonText={submitting ? 'در حال ثبت...' : 'ایجاد حساب'}
        >
          <Step>
            <h3>مشخصات اولیه</h3>
            <p>شماره موبایل را وارد کنید تا حساب شما ساخته شود.</p>
            <input
              autoComplete="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="شماره موبایل"
            />
          </Step>
          <Step>
            <h3>اطلاعات هویتی</h3>
            <p>نام کامل و کد ملی برای نمایش پروفایل و صدور فاکتور استفاده می‌شود.</p>
            <input
              autoComplete="name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="نام کامل"
            />
            <input value={nationalId} onChange={(e) => setNationalId(e.target.value)} placeholder="کد ملی" />
          </Step>
          <Step>
            <h3>امنیت حساب</h3>
            <p>رمز عبور امن وارد کنید.</p>
            <input
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="رمز عبور"
            />
            <input
              type="password"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="تکرار رمز عبور"
            />
          </Step>
          <Step>
            <h3>مرور اطلاعات</h3>
            <p>در صورت صحت اطلاعات، ایجاد حساب را بزنید.</p>
            <div className="grid">
              <p>شماره موبایل: {phoneNumber || '-'}</p>
              <p>نام کامل: {fullName || '-'}</p>
              <p>کد ملی: {nationalId || '-'}</p>
            </div>
          </Step>
        </Stepper>
        {activeStep === 4 && submitting ? <p className="ok">در حال ارسال اطلاعات...</p> : null}
        {error ? <p className="error">{error}</p> : null}
      </div>
      <div className="surface-strip auth-foot">
        <p>
          قبلا ثبت نام کرده‌اید؟ <a href="/login/">ورود</a>
        </p>
      </div>
    </section>
  )
}
