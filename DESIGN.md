---
name: Acme Corp
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
  error: "#D32F2F"
typography:
  headline-lg:
    fontFamily: Public Sans
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.2
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
    fontWeight: 600
    letterSpacing: 0.08em
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.neutral}"
    typography: "{typography.label-caps}"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "#9A3521"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
---
## Overview
Acme Corp's design language is industrial and confident. Deep ink tones with a "Boston Clay" accent that draws the eye without shouting. Typography is clean and functional, never decorative. White space does the heavy lifting.
## Colors
The primary palette is deliberately restrained. Deep charcoal (`primary`) for text, warm stone gray (`secondary`) for supporting elements, and a single warm accent (`tertiary`, Boston Clay) reserved for CTAs and emphasis. The neutral cream (`neutral`) warms the background without clinical white.
Never use tertiary for large surfaces. It's an accent, not a background.
## Typography
Two families. Public Sans for everything structural (headlines, body, captions). Space Grotesk for labels and interactive elements where a slightly geometric character helps with scannability.
The type scale has nine levels. For most pages, you'll use headline-lg, body-md, and label-caps. Reach for the others when you need hierarchy within a section.
## Components
### Buttons
Primary buttons use the Boston Clay accent with cream text. The hover state darkens the clay by roughly 15%. Padding is generous (12px vertical, 24px horizontal) to give the label breathing room.
Secondary buttons are outlined: 1px border in secondary, transparent background, secondary text. On hover, the background fills to neutral.
### Cards
Cards sit on the surface color with medium rounding and generous internal padding. No drop shadows by default. Use a 1px border in the neutral color if cards need visual separation from the background.
## Do's and Don'ts
- Do use the tertiary accent sparingly. One accent per viewport section maximum.
- Do maintain the spacing scale. Don't invent spacing values between the defined steps.
- Don't use secondary as a text color on dark backgrounds. It fails WCAG AA contrast.
- Don't mix Space Grotesk into body text. It's for labels and interactive elements only.