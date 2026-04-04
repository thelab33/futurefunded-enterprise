# FutureFunded template architecture

## Current target structure
- shared/partials: global chrome / repeated shell pieces
- shared/macros: buttons, pills, cards, reusable UI atoms
- platform/shells: marketing/operator shell variants
- platform/pages: routed platform pages
- platform/partials: platform-specific reusable sections
- campaign/index.html: public fundraising funnel
- campaign/partials: future campaign section extraction

## Migration strategy
1. Keep current live paths working
2. Move routed pages into platform/pages
3. Preserve platform/base.html during transition
4. Extract repeated sections only after shell split is stable
