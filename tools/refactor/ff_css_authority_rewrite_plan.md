# FF CSS Authority Rewrite Plan

Generated: 2026-04-05T15:40:51

## Rewrite order

### 1. Foundation + chrome
- ff-topbarBrand--flagship
- ff-topbarGoal__metaRow
- ff-topbar__brandCluster
- ff-topbar__desktopActions
- ff-topbar__rightCluster
- ff-themeToggle--desktop

### 2. Checkout
- ff-checkoutContent
- ff-checkoutScroll
- ff-checkoutStage

### 3. Shared section headers
- ff-sectionhead__text

### 4. Teams / empty states
- ff-teamsEmpty

### 5. Modal / footer polish
- ff-modal--video
- ff-onboardModal__footer
- ff-sponsorModal__footer

## Execution passes

### Pass A
- tokens
- base
- shell
- controls
- topbar

### Pass B
- hero
- story
- impact
- teams
- sponsors
- faq
- footer

### Pass C
- checkout
- sponsor modal
- video modal
- onboarding modal
- dark mode
- responsive polish

## Cleanup after rewrite
- remove dead css classes only after proof
- rerun audit v2
- visual smoke pass desktop/mobile
