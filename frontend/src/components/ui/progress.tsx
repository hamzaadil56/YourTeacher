import * as React from "react"
import { cn } from "@/lib/utils"

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number
  max?: number
  variant?: "default" | "screener" | "teaching" | "quiz"
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, max = 100, variant = "default", ...props }, ref) => {
    const percentage = Math.min(Math.max((value / max) * 100, 0), 100)

    const variantColors = {
      default: "bg-[rgb(var(--primary))]",
      screener: "bg-[rgb(var(--screener))]",
      teaching: "bg-[rgb(var(--teaching))]",
      quiz: "bg-[rgb(var(--quiz))]",
    }

    return (
      <div
        ref={ref}
        className={cn(
          "relative h-3 w-full overflow-hidden rounded-full bg-[rgb(var(--muted))]",
          className
        )}
        {...props}
      >
        <div
          className={cn(
            "h-full transition-all duration-500 ease-out",
            variantColors[variant]
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    )
  }
)
Progress.displayName = "Progress"

export { Progress }

