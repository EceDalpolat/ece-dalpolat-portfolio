import re

HTML_PATH = "index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Move <p class="ga-desc"> from inside .ga-body to just before it
# The pattern is:
#       </div>
#       <div class="ga-body">
#         <p class="ga-desc" ...>...</p>
pattern = re.compile(r'(</div>\s*<div class="ga-body">)\s*(<p class="ga-desc"[^>]*>.*?</p>)', re.DOTALL)

def replacer(match):
    # match.group(1) is '</div>\n      <div class="ga-body">'
    # match.group(2) is '<p class="ga-desc"...>...</p>'
    # We want: 
    #       </div>
    #       <p class="ga-desc"...>...</p>
    #       <div class="ga-body">
    
    # Wait, the </div> in group 1 is the closing of <div class="ga-metrics">
    # So it looks like:
    #       </div> <!-- ga-metrics -->
    #       <div class="ga-body">
    
    # We will just swap them:
    body_start = match.group(1)
    desc = match.group(2)
    
    # Split the body_start to inject desc before <div class="ga-body">
    parts = body_start.rsplit('<div class="ga-body">', 1)
    
    new_str = parts[0] + desc + '\n      <div class="ga-body">'
    return new_str

new_html = pattern.sub(replacer, html)

# Now update the CSS
css_updates = {
    # 1. Update ga-project grid-template-areas
    """"header body"
    "metrics body";""": """"header body"
    "desc body"
    "metrics body";""",
    
    # 2. Update ga-project mobile grid
    """"header"
      "metrics"
      "body";""": """"header"
      "desc"
      "metrics"
      "body";""",
      
    # 3. Add CSS for ga-desc
    ".ga-desc {\n  font-size: 15px;": """.ga-desc {
  grid-area: desc;
  font-size: 15px;
  padding: 1.5rem 2rem 0;
  border-right: 1px solid var(--surface-3);""",
  
    # Remove border-right from metrics if max-width < 900px, wait, 
    # .ga-desc needs a border removal on mobile too.
}

for old, new in css_updates.items():
    new_html = new_html.replace(old, new)
    
# Let's add the media query for ga-desc
mobile_css = """@media (max-width: 900px) {
  .ga-metrics {"""
  
new_mobile_css = """@media (max-width: 900px) {
  .ga-desc {
    border-right: none;
    padding: 1.5rem 1.5rem 0;
  }
  .ga-metrics {"""
new_html = new_html.replace(mobile_css, new_mobile_css)


with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Description moved to left column.")
