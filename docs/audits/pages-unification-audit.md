# FutureFunded pages unification audit

| kind | weight | sections | forms | dialogs | cards | pills | buttons | inputs | file |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| campaign | 2540 | 49 | 3 | 31 | 40 | 183 | 217 | 36 | `apps/web/app/templates/campaign/index.html` |
| onboarding | 84 | 1 | 1 | 0 | 6 | 0 | 4 | 8 | `apps/web/app/templates/platform/onboarding.html` |
| dashboard | 70 | 1 | 0 | 0 | 8 | 0 | 9 | 0 | `apps/web/app/templates/platform/dashboard.html` |
| home | 58 | 1 | 0 | 0 | 10 | 8 | 6 | 0 | `apps/web/app/templates/platform/home.html` |
| home | 17 | 1 | 0 | 0 | 2 | 4 | 0 | 0 | `apps/web/app/templates/partials/integration_health_panel.html` |
| home | 9 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | `apps/web/app/templates/platform/base.html` |

## Heaviest files

- **campaign** `apps/web/app/templates/campaign/index.html` → weight 2540
- **onboarding** `apps/web/app/templates/platform/onboarding.html` → weight 84
- **dashboard** `apps/web/app/templates/platform/dashboard.html` → weight 70
- **home** `apps/web/app/templates/platform/home.html` → weight 58
- **home** `apps/web/app/templates/partials/integration_health_panel.html` → weight 17
- **home** `apps/web/app/templates/platform/base.html` → weight 9

## Summary by page type

- **campaign**: 1 file(s), avg weight 2540.0
- **dashboard**: 1 file(s), avg weight 70.0
- **home**: 3 file(s), avg weight 28.0
- **onboarding**: 1 file(s), avg weight 84.0

## Campaign verdict

- Heaviest campaign file: `apps/web/app/templates/campaign/index.html` → weight 2540, sections=49, forms=3, dialogs=31, cards=40, pills=183, buttons=217, inputs=36
- Verdict: campaign is likely carrying too many responsibilities in one template.
