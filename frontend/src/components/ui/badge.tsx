import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-[rgb(var(--primary))] text-[rgb(var(--primary-foreground))] shadow",
        secondary:
          "border-transparent bg-[rgb(var(--secondary))] text-[rgb(var(--secondary-foreground))]",
        destructive:
          "border-transparent bg-[rgb(var(--destructive))] text-[rgb(var(--destructive-foreground))] shadow",
        outline: "text-[rgb(var(--foreground))]",
        screener: "border-transparent bg-[rgb(var(--screener))] text-white shadow",
        teaching: "border-transparent bg-[rgb(var(--teaching))] text-white shadow",
        quiz: "border-transparent bg-[rgb(var(--quiz))] text-white shadow",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }


