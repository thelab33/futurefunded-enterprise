from pathlib import Path

JS = Path.home() / "futurefunded-enterprise/apps/web/app/static/js/ff-app.js"

text = JS.read_text(encoding="utf-8")

# Upgrade donate button to match contract selector
text = text.replace(
    'donateBtn.textContent = "Donate";',
    '''donateBtn.textContent = "Donate";
      donateBtn.setAttribute("data-ff-open-checkout", "");'''
)

# Upgrade sponsor button to match contract selector
text = text.replace(
    'sponsorBtn.textContent = "Sponsor";',
    '''sponsorBtn.textContent = "Sponsor";
      sponsorBtn.setAttribute("data-ff-open-sponsor", "");'''
)

JS.write_text(text, encoding="utf-8")

print("patched mobile rail contract alignment.")
