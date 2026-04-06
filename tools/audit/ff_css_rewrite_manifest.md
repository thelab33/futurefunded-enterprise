# FF CSS Rewrite Manifest

## Inputs
- Template: `/home/elCUCO/futurefunded-enterprise/apps/web/app/templates/campaign/index.html`
- CSS: `/home/elCUCO/futurefunded-enterprise/apps/web/app/static/css/ff.css`
- Audit: `/home/elCUCO/futurefunded-enterprise/tools/audit/ff_css_contract_audit_v1.json`

## Audit summary
- HTML classes: 406
- HTML ids: 97
- HTML hooks: 138
- CSS class candidates: 385
- CSS id candidates: 95
- CSS hook candidates: 138

## Delta summary
- Missing CSS classes: 14
- Missing CSS ids: 0
- Missing CSS hooks: 0
- Dead CSS classes: 6
- Dead CSS ids: 0
- Missing JS hooks: 48

## Interpretation
This is a good candidate for a full authority rewrite.
The contract is mostly intact.
Main tasks:
1. Style the remaining missing classes
2. Remove dead selector drift
3. Reorganize CSS by section
4. Preserve existing hook contract and modal/drawer/checkout semantics
5. Re-run audit after rewrite

## Missing CSS classes
- `ff-checkoutContent`
- `ff-checkoutScroll`
- `ff-checkoutStage`
- `ff-modal--video`
- `ff-onboardModal__footer`
- `ff-sectionhead__text`
- `ff-sponsorModal__footer`
- `ff-teamsEmpty`
- `ff-themeToggle--desktop`
- `ff-topbarBrand--flagship`
- `ff-topbarGoal__metaRow`
- `ff-topbar__brandCluster`
- `ff-topbar__desktopActions`
- `ff-topbar__rightCluster`

## Dead CSS classes
- `ff-sponsorTierCard`
- `ff-sponsorTierCard__body`
- `ff-sponsorTierCard__foot`
- `ff-sponsorTierCard__head`
- `ff-storyPoster__picture`
- `is-visible`

## Dead CSS ids
- None

## Sections discovered
- `home` — 69 classes / 5 ids / 0 missing classes
- `impact` — 57 classes / 6 ids / 1 missing classes
- `teams` — 67 classes / 4 ids / 2 missing classes
- `sponsors` — 46 classes / 6 ids / 1 missing classes
- `story` — 54 classes / 3 ids / 1 missing classes
- `faq` — 49 classes / 3 ids / 0 missing classes
- `checkout` — 65 classes / 12 ids / 3 missing classes
- `press-video` — 40 classes / 4 ids / 1 missing classes
- `terms` — 35 classes / 3 ids / 0 missing classes
- `privacy` — 33 classes / 3 ids / 0 missing classes
- `sponsor-interest` — 30 classes / 7 ids / 0 missing classes
- `ff-onboarding` — 31 classes / 8 ids / 0 missing classes
- `ffOnboardPanel2` — 5 classes / 1 ids / 0 missing classes
- `ffOnboardPanel3` — 4 classes / 1 ids / 0 missing classes
- `ffOnboardPanel4` — 8 classes / 1 ids / 0 missing classes
