from pathlib import Path
from textwrap import dedent

ROOT = Path.home() / "futurefunded-enterprise"
SALES = ROOT / "docs" / "sales"
SALES.mkdir(parents=True, exist_ok=True)

files = {
    "README.md": dedent("""
        # FutureFunded Sales Assets

        This folder contains the founder-ready sales pack for FutureFunded.

        ## Recommended order
        1. Read `one-pager.md`
        2. Use `outreach-playbook.md` to start conversations
        3. Use `demo-talk-track.md` during live walkthroughs
        4. Use `objection-handling.md` when buyers hesitate
        5. Use `follow-up-templates.md` after calls and demos

        ## Positioning in one line
        FutureFunded helps youth teams, schools, nonprofits, and clubs launch a premium fundraising page, sponsor-ready packages, and recurring support from one clean system.

        ## Current pricing path
        - Starter: $49 setup
        - Growth: $79/mo
        - White-label: Custom

        ## Core close
        Start on Starter, prove the fundraiser, then upgrade to Growth once sponsor packages and recurring support start paying for the platform.
    """).strip() + "\n",

    "one-pager.md": dedent("""
        # FutureFunded — Founder One-Pager

        ## What it is
        FutureFunded is a premium fundraising platform for youth teams, schools, nonprofits, and clubs. It gives organizations a clean public fundraiser, sponsor-ready packages, and recurring support lanes from one system.

        ## What problem it solves
        Most organizations still fundraise with a mix of scattered links, weak sponsor presentation, and no operator workflow. That makes fundraising feel small, manual, and hard to trust.

        ## What FutureFunded changes
        FutureFunded gives buyers:
        - a public fundraiser that looks credible on desktop and mobile
        - a sponsor lane that feels like a real business opportunity
        - a launch flow that gets the organization live fast
        - an operator dashboard that makes the platform feel like a system, not just a page

        ## Why buyers respond to it
        It helps them say:
        - “This looks trustworthy.”
        - “This feels easy to launch.”
        - “Sponsors would actually take this seriously.”
        - “We can start simple and grow later.”

        ## What they get in the first launch
        - a branded public fundraiser
        - donation flow and mobile-ready conversion path
        - sponsor spotlight / sponsor packages
        - launch onboarding
        - operator dashboard
        - pricing path for future growth

        ## Who it is for
        - youth sports programs
        - booster clubs
        - schools
        - nonprofits
        - clubs and local organizations

        ## Pricing story
        - **Starter — $49 setup**  
          Best for getting live fast and proving the offer.
        - **Growth — $79/mo**  
          Best when sponsor packages and recurring support become part of the operating model.
        - **White-label — Custom**  
          Best for schools, nonprofits, and institutions that need a more premium branded rollout.

        ## Founder close
        Most organizations should start on Starter, get the fundraiser live, then move to Growth once sponsor packages and recurring support start paying for the platform.

        ## Call to action
        If this looked like your program, we could launch your version this week.
    """).strip() + "\n",

    "outreach-playbook.md": dedent("""
        # Outreach Playbook

        ## Cold DM — coach / program director
        Hey — I’ve been building a premium fundraising platform for teams and programs that want something cleaner than a basic donation page. It gives you a branded fundraiser, sponsor-ready packages, and a simple launch flow so it actually feels like a real product. I can show you a live example if you want.

        ## Warm intro message
        I’ve got something I’d love to show you. It’s a fundraising system for programs that need more than a donate link — public fundraiser, sponsor lane, and operator side all in one clean setup. I think it would fit organizations that want to look more credible with families and local sponsors.

        ## Short email opener
        Subject: A cleaner fundraising system for your program

        I’ve been building a fundraising platform for youth teams, schools, nonprofits, and clubs that want a more premium setup than a basic donation page. It includes a public fundraiser, sponsor-ready packages, and a launch flow that makes it easy to get live fast. Happy to send over a live example or walk you through it in a few minutes.

        ## Follow-up bump
        Wanted to bump this in case it got buried. The reason I think this is relevant is that it helps programs look more credible with both supporters and sponsors — without needing a full custom build.

        ## Best outreach angle
        Don’t lead with features first. Lead with:
        - cleaner trust
        - better sponsor presentation
        - faster launch
        - easy first step

        ## What not to say
        - “It does everything.”
        - “It’s like 10 platforms in one.”
        - “It’s still early but…”

        ## What to say instead
        - “It gets your public fundraiser live fast.”
        - “It helps sponsors take you seriously.”
        - “You can start simple and grow into more.”
    """).strip() + "\n",

    "demo-talk-track.md": dedent("""
        # Demo Talk Track

        ## 30-second opener
        FutureFunded is built for teams, schools, nonprofits, and clubs that want a cleaner fundraising system than a basic donation page. It gives you a public fundraiser, sponsor-ready packages, and a simple launch workflow so the whole thing feels credible and easy to buy.

        ## 5-minute demo flow

        ### 1. Open platform home
        “This is the public-facing system. The goal is to make fundraising look trustworthy, modern, and sponsor-ready.”

        ### 2. Open the live fundraiser
        “This is what supporters actually see. It works on mobile, has a clear giving path, and gives bigger supporters a sponsor lane instead of only a donate button.”

        ### 3. Open onboarding
        “This is how we launch your version fast — organization, fundraiser, branding, and handoff into the operator side.”

        ### 4. Open dashboard
        “This is what makes it more than a page. You can manage the fundraiser, sponsor packages, and recurring support from one operator view.”

        ### 5. Open pricing
        “Most groups start on Starter to get live fast. Once sponsor packages and recurring support are working, Growth becomes the smart default because it starts paying for itself.”

        ## Core close
        “If this looked like your program, would you want us to launch your version this week?”

        ## Stronger close if the call is going well
        “The simplest next step is to start on Starter, get the public fundraiser live, and then expand once the sponsor lane starts working.”

        ## What the buyer should feel by the end
        - this looks credible
        - this feels easy
        - we could launch this
        - this is not just another donation link
    """).strip() + "\n",

    "objection-handling.md": dedent("""
        # Objection Handling

        ## “We need to think about it.”
        Totally fair. The simplest way to de-risk it is to start with the public fundraiser first, prove the surface, and then expand only once it’s working for you.

        ## “We’re not ready for a full platform.”
        That’s exactly why Starter exists. You don’t need the full expansion path on day one — you just need the fundraiser live and looking credible.

        ## “We need sponsor money, not just donations.”
        That’s why the sponsor lane is built in this early. The platform is designed to help you bring in direct support and make a stronger ask to local businesses.

        ## “We already have a donation page.”
        That makes sense. The difference here is that this is not just a donation page — it gives you sponsor packaging, cleaner trust, and an operator workflow so the product feels bigger than a link.

        ## “We don’t know if our people would use it.”
        That’s why the launch path stays simple. Start with the fundraiser, share it with supporters, and use that as the first proof point before expanding.

        ## “We don’t have time for a complicated setup.”
        The point is to remove complexity, not add it. The launch flow is designed so you can get your version live fast and improve it from there.

        ## “We need approval.”
        That’s normal. The best next step is to review the live example together and decide whether Starter is enough for the first launch or whether you want the stronger institutional version.
    """).strip() + "\n",

    "follow-up-templates.md": dedent("""
        # Follow-Up Templates

        ## After a good demo
        Thanks again for taking a look. The main reason I think this fits your program is that it gives you a cleaner public fundraiser, a stronger sponsor story, and a simple path to launch. The easiest next step is to start on Starter, get your version live, and expand once the sponsor lane starts working.

        ## After a “not yet”
        Totally understand. I’d keep the first step simple: launch the fundraiser first, use it as the proof point, and only expand into Growth once you’re ready for sponsor packages and recurring support.

        ## After a soft maybe
        The reason I’d still take a serious look at it is that it solves the trust problem and the sponsor presentation problem at the same time. Even getting the public fundraiser live can change how supporters and local businesses respond.

        ## Re-engagement message
        Wanted to circle back because this is the kind of product that tends to make the most sense once a program is actively fundraising or talking to sponsors. Happy to reopen the live example and walk through it together.

        ## Strong close email
        Subject: Want us to launch your version this week?

        Appreciate the conversation. From what you shared, the cleanest next step is to launch the public fundraiser first, then decide whether Growth makes sense once sponsor packages and recurring support are active. If you want to move, we can start with Starter and get your version live this week.
    """).strip() + "\n",
}

for name, content in files.items():
    (SALES / name).write_text(content, encoding="utf-8")

print("wrote sales asset pack:")
for name in files:
    print(" -", SALES / name)
