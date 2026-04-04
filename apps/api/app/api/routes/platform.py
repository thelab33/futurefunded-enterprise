from fastapi import APIRouter

router = APIRouter(prefix="/platform", tags=["platform"])


@router.get("/home")
def home_payload() -> dict:
    return {
        "page_title": "FutureFunded Platform Home",
        "hero": {
            "eyebrow": "AAU launch-ready",
            "title": "Give Connect ATX Elite a premium fundraising home.",
            "body": "Launch a sponsor-ready fundraising experience for youth boys basketball, starting with Connect ATX Elite — branded giving, booster support, and a cleaner story for families and local sponsors.",
            "primary_cta_label": "Launch Connect ATX Elite",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "Open dashboard",
            "secondary_cta_href": "/platform/dashboard",
            "pills": ["AAU ready", "Mobile first", "Sponsor-ready", "Booster support"],
        },
        "launch_cards": [
            {
                "title": "Live fundraiser page",
                "body": "A polished donation surface for Connect ATX Elite with cleaner hierarchy, stronger trust, and a fast path to support.",
            },
            {
                "title": "Sponsor packages",
                "body": "Credible local business support lanes that feel ready to share with community partners and parent networks.",
            },
            {
                "title": "Booster memberships",
                "body": "Monthly and annual support options that help the program build stability beyond one-time campaign pushes.",
            },
            {
                "title": "Program hub",
                "body": "A branded home for the AAU program with colors, campaign story, and room to grow into a fuller platform later.",
            },
        ],
        "status_cards": [
            {"label": "Backend", "value": "Live"},
            {"label": "Campaign", "value": "Live"},
            {"label": "Positioning", "value": "Premium"},
        ],
        "status_pills": ["Connect ATX Elite", "Spring Fundraiser", "Launchable now"],
        "left_feature": {
            "eyebrow": "Built for youth programs",
            "title": "One platform. Multiple support lanes.",
            "body": "Give youth basketball programs a premium fundraising product with direct giving, sponsor support, booster memberships, and branded organization pages in one place.",
            "pills": ["Youth sports", "Families", "Sponsors", "Boosters"],
        },
        "right_feature": {
            "eyebrow": "Launch lanes",
            "title": "Start with one team. Expand with confidence.",
            "body": "Begin with Connect ATX Elite, then expand into sponsor packages, recurring support, announcement bars, countdowns, and branded organization hubs without rebuilding from scratch.",
            "pills": ["Campaigns", "Memberships", "Sponsors", "Branding"],
        },
        "why_it_wins": {
            "eyebrow": "Why it wins",
            "title": "Built to feel like a product, not a fundraiser template.",
            "body": "FutureFunded helps families, supporters, and local sponsors understand the need faster and act with more confidence.",
            "cards": [
                {
                    "title": "Cleaner conversion surfaces",
                    "body": "Reduce hesitation with sharper hierarchy, stronger CTAs, and clearer support paths.",
                },
                {
                    "title": "Real-world team launch flow",
                    "body": "Spin up a real AAU organization with campaign defaults that are already sponsor-ready and parent-friendly.",
                },
            ],
        },
        "next_move": {
            "eyebrow": "Next move",
            "title": "Launch the real program, not a demo.",
            "body": "Use onboarding to create the real Connect ATX Elite organization, then manage the live fundraiser, sponsor packages, and booster support from the dashboard.",
            "primary_cta_label": "Create organization",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "Manage platform",
            "secondary_cta_href": "/platform/dashboard",
        },
    }


@router.get("/onboarding")
def onboarding_payload() -> dict:
    return {
        "page_title": "FutureFunded Onboarding",
        "eyebrow": "Step 1 · Launch Connect ATX Elite",
        "title": "Onboarding",
        "body": "Set up the real Connect ATX Elite program and Spring Fundraiser defaults, then hand off directly into the operating dashboard.",
        "organization": {
            "title": "Organization",
            "fields": [
                {"label": "Organization name", "name": "org_name", "value": "Connect ATX Elite"},
                {"label": "Organization slug", "name": "org_slug", "value": "connect-atx-elite"},
                {"label": "Primary color", "name": "primary_color", "value": "#f97316"},
                {"label": "Secondary color", "name": "secondary_color", "value": "#111827"},
            ],
        },
        "campaign": {
            "title": "Campaign",
            "fields": [
                {"label": "Campaign name", "name": "campaign_name", "value": "Spring Fundraiser"},
                {"label": "Campaign slug", "name": "campaign_slug", "value": "spring-fundraiser"},
                {"label": "Headline", "name": "headline", "value": "Fuel the season. Fund the future."},
                {"label": "Goal amount", "name": "goal_amount", "value": "10000.00"},
            ],
        },
        "submit_label": "Create org + campaign",
        "submit_href": "/platform/dashboard",
    }


@router.get("/dashboard")
def dashboard_payload() -> dict:
    return {
        "page_title": "FutureFunded Dashboard",
        "eyebrow": "Admin dashboard",
        "title": "FutureFunded command center",
        "body": "Manage the live Connect ATX Elite fundraiser, sponsor packages, and booster support from one premium workspace.",
        "overview_cards": [
            {"title": "Organizations", "body": "Active organizations in this workspace", "value": "1"},
            {"title": "Campaigns", "body": "Live fundraising campaigns you can manage", "value": "1"},
            {"title": "Sponsor tiers", "body": "Active support packages for local partners", "value": "2"},
            {"title": "Membership plans", "body": "Recurring support plans configured", "value": "2"},
        ],
        "actions": [
            {"label": "Create another org", "href": "/platform/onboarding", "variant": "primary"},
            {"label": "Open live campaign", "href": "/c/spring-fundraiser", "variant": "secondary"},
        ],
        "org_cards": [
            {
                "title": "Connect ATX Elite",
                "slug": "connect-atx-elite",
                "status": "Live",
                "campaign_name": "Spring Fundraiser",
                "campaign_url": "/c/spring-fundraiser",
            },
        ],
        "sponsor_tiers": [
            {
                "title": "Bronze Sponsor",
                "body": "Entry-tier local sponsor visibility for businesses that want to support the team and be seen on the campaign page.",
                "pills": ["$250.00", "Active"],
            },
            {
                "title": "Gold Sponsor",
                "body": "Premium sponsor placement and recognition with stronger visibility across the fundraising experience.",
                "pills": ["$1000.00", "Featured", "Active"],
            },
        ],
        "membership_plans": [
            {
                "title": "Booster Monthly",
                "body": "Monthly support for the Connect ATX Elite program.",
                "pills": ["$19.00", "monthly"],
            },
            {
                "title": "Booster Annual",
                "body": "Annual support with stronger recognition and long-term backing for the program.",
                "pills": ["$199.00", "yearly", "Featured"],
            },
        ],
    }
