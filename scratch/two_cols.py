import re

HTML_PATH = "index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove ga-projects-grid wrapper
html = html.replace('<div class="ga-projects-grid">\n    <!-- ANALYTICS — featured -->', '<!-- ANALYTICS — featured -->')
html = html.replace('    </div>\n\n    <!-- other projects grid -->', '    <!-- other projects grid -->')

# 2. Update the CSS for ga-project
# We want to change .ga-project, .ga-header, .ga-metrics, and remove .ga-projects-grid CSS
css_to_remove_regex = r"\.ga-projects-grid\s*{[^}]+}\s*@media\s*\([^)]+\)\s*{\s*\.ga-projects-grid\s*{[^}]+}\s*}\s*\.ga-projects-grid\s*\.ga-project\s*{[^}]+}\s*\.ga-projects-grid\s*\.ga-body\s*{[^}]+}\s*\.ga-projects-grid\s*\.ga-stack\s*{[^}]+}"

html = re.sub(css_to_remove_regex, "", html, flags=re.MULTILINE)

# Now, we need to modify .ga-project to be a two-column grid
project_css = """
/* ── GA PROJECT (special) ── */
#projects .section-title { margin-bottom: 2rem; }
.ga-project {
  position: relative;
  background: var(--surface-2);
  border-radius: calc(var(--radius) + 2px);
  margin-bottom: 3rem;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--surface-3);
  transition: transform 0.25s, box-shadow 0.25s;
  
  /* TWO COLUMN LAYOUT */
  display: grid;
  grid-template-columns: 320px 1fr;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    "header body"
    "metrics body";
}
@media (max-width: 900px) {
  .ga-project {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "metrics"
      "body";
  }
}
.ga-project::before {
"""

html = html.replace("""/* ── GA PROJECT (special) ── */
#projects .section-title { margin-bottom: 2rem; }
.ga-project {
  position: relative;
  background: var(--surface-2);
  border-radius: calc(var(--radius) + 2px);
  margin-bottom: 2rem;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--surface-3);
  transition: transform 0.25s, box-shadow 0.25s;
}
.ga-project::before {""", project_css)

# Update header and metrics to use grid-area
header_css = """
.ga-header {
  grid-area: header;
  background: linear-gradient(135deg, #0c0e14 0%, #1a1d2e 50%, #1e1b4b 100%);
"""
html = html.replace(".ga-header {\n  background: linear-gradient", header_css)

metrics_css = """
.ga-metrics {
  grid-area: metrics;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background: linear-gradient(180deg, #f8f9fd 0%, #fff 100%);
  border-right: 1px solid var(--surface-3);
}
@media (max-width: 900px) {
  .ga-metrics {
    flex-direction: row;
    flex-wrap: wrap;
    border-right: none;
    border-bottom: 1px solid var(--surface-3);
    padding: 1.35rem 2rem;
    gap: 1.5rem 2rem;
  }
}
.ga-metric {"""
html = html.replace(""".ga-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem 2rem;
  padding: 1.35rem 2rem;
  background: linear-gradient(180deg, #f8f9fd 0%, #fff 100%);
  border-bottom: 1px solid var(--surface-3);
}
.ga-metric {""", metrics_css)


body_css = """
.ga-body { 
  grid-area: body;
  padding: 2.5rem; 
  background: var(--surface-2); 
  display: flex;
  flex-direction: column;
}
"""
html = html.replace(".ga-body { padding: 2rem; background: var(--surface-2); }", body_css)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Project self-two-column layout applied.")
