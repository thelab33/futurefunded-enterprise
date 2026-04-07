from pathlib import Path

JS = Path.home() / "futurefunded-enterprise/apps/web/app/static/js/ff-app.js"

text = JS.read_text(encoding="utf-8")

# HARD upgrade donate button (full contract compliance)
text = text.replace(
    'donateBtn.textContent = "Donate";',
    '''donateBtn.textContent = "Donate";
      donateBtn.setAttribute("data-ff-open-checkout", "");
      donateBtn.setAttribute("data-ff-donate", "");
      donateBtn.setAttribute("aria-label", "Donate now");'''
)

# HARD upgrade sponsor button
text = text.replace(
    'sponsorBtn.textContent = "Sponsor";',
    '''sponsorBtn.textContent = "Sponsor";
      sponsorBtn.setAttribute("data-ff-open-sponsor", "");
      sponsorBtn.setAttribute("data-ff-sponsor-interest", "");
      sponsorBtn.setAttribute("aria-label", "Become a sponsor");'''
)

JS.write_text(text, encoding="utf-8")

print("patched FINAL mobile rail fix.")
