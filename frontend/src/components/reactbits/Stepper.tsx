import { Children, ReactNode, isValidElement, useEffect, useLayoutEffect, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import './Stepper.css'

type StepperProps = {
  children: ReactNode
  initialStep?: number
  onStepChange?: (step: number) => void
  onFinalStepCompleted?: () => void
  backButtonText?: string
  nextButtonText?: string
  completeButtonText?: string
  disableStepIndicators?: boolean
  className?: string
  canProceed?: (step: number) => boolean
}

type StepProps = {
  children: ReactNode
}

export function Step({ children }: StepProps) {
  return <div className="rb-stepper-step">{children}</div>
}

export default function Stepper({
  children,
  initialStep = 1,
  onStepChange,
  onFinalStepCompleted,
  backButtonText = 'Back',
  nextButtonText = 'Continue',
  completeButtonText = 'Complete',
  disableStepIndicators = false,
  className = '',
  canProceed,
}: StepperProps) {
  const steps = Children.toArray(children).filter((child) => isValidElement(child))
  const totalSteps = steps.length
  const [currentStep, setCurrentStep] = useState(Math.min(Math.max(initialStep, 1), Math.max(totalSteps, 1)))
  const [direction, setDirection] = useState(0)
  const [contentHeight, setContentHeight] = useState(0)
  const isLastStep = currentStep === totalSteps

  const updateStep = (nextStep: number) => {
    setCurrentStep(nextStep)
    onStepChange?.(nextStep)
  }

  const moveToStep = (nextStep: number) => {
    if (nextStep < 1 || nextStep > totalSteps || nextStep === currentStep) return
    if (canProceed && nextStep > currentStep && !canProceed(currentStep)) return
    setDirection(nextStep > currentStep ? 1 : -1)
    updateStep(nextStep)
  }

  const handleBack = () => {
    moveToStep(currentStep - 1)
  }

  const handleNext = () => {
    if (isLastStep) {
      if (canProceed && !canProceed(currentStep)) return
      onFinalStepCompleted?.()
      return
    }
    moveToStep(currentStep + 1)
  }

  return (
    <section className={`rb-stepper ${className}`}>
      <ol
        className="rb-stepper-indicators"
        aria-label="Registration steps"
        style={{ ['--steps' as string]: totalSteps }}
      >
        {steps.map((_, idx) => {
          const stepNumber = idx + 1
          const status = currentStep === stepNumber ? 'active' : currentStep > stepNumber ? 'complete' : 'inactive'
          const clickable = !disableStepIndicators
          return (
            <li className="rb-stepper-indicator-item" key={stepNumber}>
              <button
                type="button"
                className={`rb-stepper-indicator is-${status}`}
                onClick={() => clickable && moveToStep(stepNumber)}
                disabled={!clickable}
                aria-current={currentStep === stepNumber ? 'step' : undefined}
                aria-label={`Step ${stepNumber}`}
              >
                {status === 'complete' ? '✓' : stepNumber}
              </button>
              {stepNumber < totalSteps ? <span className={`rb-stepper-connector ${currentStep > stepNumber ? 'is-complete' : ''}`} /> : null}
            </li>
          )
        })}
      </ol>

      <motion.div className="rb-stepper-content" animate={{ height: contentHeight }} transition={{ duration: 0.28 }}>
        <AnimatePresence mode="wait" initial={false} custom={direction}>
          <StepSlide key={currentStep} direction={direction} onHeight={setContentHeight}>
            {steps[currentStep - 1]}
          </StepSlide>
        </AnimatePresence>
      </motion.div>

      <div className={`rb-stepper-footer ${currentStep > 1 ? 'spread' : 'end'}`}>
        {currentStep > 1 ? (
          <button type="button" className="rb-stepper-back" onClick={handleBack}>
            {backButtonText}
          </button>
        ) : null}
        <button type="button" className="rb-stepper-next" onClick={handleNext}>
          {isLastStep ? completeButtonText : nextButtonText}
        </button>
      </div>
    </section>
  )
}

function StepSlide({
  children,
  direction,
  onHeight,
}: {
  children: ReactNode
  direction: number
  onHeight: (height: number) => void
}) {
  const ref = useRef<HTMLDivElement | null>(null)

  useLayoutEffect(() => {
    if (ref.current) {
      onHeight(ref.current.offsetHeight)
    }
  }, [children, onHeight])

  useEffect(() => {
    if (!ref.current) return
    const element = ref.current
    const syncHeight = () => onHeight(element.offsetHeight)
    syncHeight()

    window.addEventListener('resize', syncHeight)
    const supportsResizeObserver = typeof ResizeObserver !== 'undefined'
    const observer = supportsResizeObserver ? new ResizeObserver(syncHeight) : null
    if (observer) observer.observe(element)

    return () => {
      if (observer) observer.disconnect()
      window.removeEventListener('resize', syncHeight)
    }
  }, [onHeight])

  return (
    <motion.div
      ref={ref}
      custom={direction}
      variants={{
        enter: (dir: number) => ({ x: dir >= 0 ? '-12%' : '12%', opacity: 0 }),
        center: { x: '0%', opacity: 1 },
        exit: (dir: number) => ({ x: dir >= 0 ? '10%' : '-10%', opacity: 0 }),
      }}
      initial="enter"
      animate="center"
      exit="exit"
      transition={{ duration: 0.25 }}
      className="rb-stepper-slide"
    >
      {children}
    </motion.div>
  )
}




