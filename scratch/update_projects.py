import json
import re

EN_JSON_PATH = "i18n/en.json"
TR_JSON_PATH = "i18n/tr.json"
HTML_PATH = "index.html"

# Data for new premium layout
new_en = {
    "analytics": {
        "problem": "Psychometric assessment data (AON, Saville, 360°) was siloed, making it difficult to generate holistic HR insights and tenant-specific dashboards without exposing sensitive cross-tenant data.",
        "contribution": "Designed and built the full AI precompute layer and dbt transformation pipeline. Implemented PostgreSQL native RLS (Row-Level Security) to ensure tenant isolation across 109 models and 8+ embedded dashboards.",
        "impact": "Unblocked production deployment by fixing RLS dependency issues. Scaled the platform to support 56 mart tables and 13 AI precompute marts with zero cross-tenant data leakage.",
        "solution1": "dbt pipeline for data transformation",
        "solution2": "PostgreSQL FDW for data ingestion",
        "solution3": "Native RLS for multi-tenant security",
        "solution4": "AI precompute marts for rapid analytics"
    },
    "coach": {
        "problem": "Delivering effective corporate AI coaching requires maintaining context across sessions, objectively evaluating agent performance, and supporting seamless voice interaction.",
        "contribution": "Built the evaluation framework (LLM-as-Judge), the early voice stack via OpenAI Realtime API, and the foundation for POML prompt orchestration.",
        "impact": "Improved AI simulator turn-based progression by 49% fewer turns and increased evaluation score from 7.88 to 8.2. Pioneered real-time voice coaching integration.",
        "solution1": "Referee Agent (LLM-as-Judge)",
        "solution2": "WebSocket voice server (24 kHz PCM16)",
        "solution3": "Advanced pattern engine (CoT, ToT)",
        "solution4": "Client-side memory optimization"
    },
    "analyzer": {
        "problem": "A behavioral analytics AI agent required strict security to handle sensitive HR data while providing accurate, natural-language answers over structured psychometric marts.",
        "contribution": "Led the security architecture and config bootstrap. Shipped the full RLS-security branch including JWT auth on HTTP + WebSockets and a 4-layer threat pattern guard.",
        "impact": "Secured the dual-service architecture (Analyzer + Analyzer API) for B2B SaaS production. Achieved end-to-end LLM trace observability using Langfuse.",
        "solution1": "LangChain ReAct agent",
        "solution2": "4-layer security & RLS pipeline",
        "solution3": "Langfuse tracing integration",
        "solution4": "Config Path Resolver & Schema Layer"
    },
    "kpi": {
        "problem": "Organizations struggle to define SMART KPIs for various job positions. Generative AI alone hallucinates without a grounded, domain-specific taxonomy.",
        "contribution": "Primary engineer on the generation engine and retrieval layer. Built the hybrid lexical + category-prior retrieval over APQC Process Classification Framework.",
        "impact": "Successfully recommended position-based KPIs across 2680 metrics with high confidence. Calibrated the system via a corporate Golden Dataset.",
        "solution1": "FastAPI structured JSON output",
        "solution2": "Hybrid APQC taxonomy retrieval",
        "solution3": "Redis SHA-256 caching layer",
        "solution4": "Offline LLM-as-judge pipeline"
    }
}

new_tr = {
    "analytics": {
        "problem": "Psikometrik değerlendirme verileri (AON, Saville, 360°) birbirinden kopuktu; hassas verileri riske atmadan kiracıya özel (multi-tenant) B2B dashboard'lar üretmek zordu.",
        "contribution": "Tüm AI ön-hesaplama katmanını ve dbt dönüşüm hattını tasarladım. 109 model ve 8+ gömülü dashboard için PostgreSQL RLS (Satır Düzeyi Güvenlik) uyguladım.",
        "impact": "RLS bağımlılık sorunlarını çözerek canlıya alımı hızlandırdım. Platformu, sıfır veri sızıntısıyla 56 mart ve 13 AI mart'ı destekleyecek şekilde ölçeklendirdim.",
        "solution1": "Veri dönüşümü için dbt hattı",
        "solution2": "Veri alımı için PostgreSQL FDW",
        "solution3": "Çok kiracılı güvenlik için Native RLS",
        "solution4": "Hızlı analitik için AI ön-hesaplama mart'ları"
    },
    "coach": {
        "problem": "Etkili kurumsal AI koçluğu; seanslar arası bağlamın korunmasını, ajan performansının objektif değerlendirilmesini ve kesintisiz sesli etkileşimi gerektiriyordu.",
        "contribution": "Değerlendirme altyapısını (LLM-as-Judge), OpenAI Realtime API üzerinden ses katmanını ve POML prompt orkestrasyon temelini kurdum.",
        "impact": "AI simülatör tur ilerlemesini %49 iyileştirdim ve değerlendirme puanını 7.88'den 8.2'ye çıkardım. Gerçek zamanlı sesli koçluk entegrasyonuna öncülük ettim.",
        "solution1": "Hakem Ajanı (LLM-as-Judge)",
        "solution2": "WebSocket ses sunucusu (24 kHz PCM16)",
        "solution3": "Gelişmiş pattern motoru (CoT, ToT)",
        "solution4": "İstemci tarafı bellek optimizasyonu"
    },
    "analyzer": {
        "problem": "Davranışsal analitik ajanının, psikometrik mart'lar üzerinde doğal dilde cevaplar verirken hassas İK verilerini sıkı bir güvenlik altında işlemesi gerekiyordu.",
        "contribution": "Güvenlik mimarisi ve konfigürasyon altyapısına liderlik ettim. HTTP + WebSocket üzerinde JWT yetkilendirmesi ve 4 katmanlı tehdit korumasını (RLS-security) canlıya aldım.",
        "impact": "B2B SaaS üretimi için çift servisli mimariyi (Analyzer + Analyzer API) güvence altına aldım. Langfuse ile uçtan uca LLM izlenebilirliği sağladım.",
        "solution1": "LangChain ReAct ajanı",
        "solution2": "4 katmanlı güvenlik & RLS hattı",
        "solution3": "Langfuse izlenebilirlik entegrasyonu",
        "solution4": "Konfigürasyon ve Şema Katmanı"
    },
    "kpi": {
        "problem": "Kurumlar pozisyonlara uygun SMART KPI'lar belirlemekte zorlanıyor. Üretken yapay zeka ise standart bir taksonomi olmadan halüsinasyon üretiyordu.",
        "contribution": "Üretim motoru ve bilgi getirme (retrieval) katmanının ana mühendisiyim. APQC Süreç Sınıflandırma Çerçevesi üzerinde hibrit arama mimarisini kurdum.",
        "impact": "2680 metrik üzerinden pozisyon bazlı KPI'ları yüksek güvenilirlikle önerdim. Sistemi kurumsal bir Golden Dataset (Altın Veriseti) ile kalibre ettim.",
        "solution1": "FastAPI yapılandırılmış JSON çıktısı",
        "solution2": "Hibrit APQC taksonomi araması",
        "solution3": "Redis SHA-256 önbellek katmanı",
        "solution4": "Çevrimdışı LLM-as-judge hattı"
    }
}

# Update JSON
for path, data_dict in [(EN_JSON_PATH, new_en), (TR_JSON_PATH, new_tr)]:
    with open(path, "r", encoding="utf-8") as f:
        j = json.load(f)
    for proj_key, vals in data_dict.items():
        if f"proj.{proj_key}" not in j:
            continue
        for k, v in vals.items():
            j[f"proj.{proj_key}"][k] = v
    with open(path, "w", encoding="utf-8") as f:
        json.dump(j, f, indent=2, ensure_ascii=False)

css_code = """
/* ── PREMIUM PROJECTS ── */
.premium-project {
  display: flex;
  background: white;
  border-radius: 1.5rem;
  overflow: hidden;
  border: 1px solid var(--surface-3);
  margin-bottom: 4rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
}
.pp-left {
  background: #0F243B;
  color: white;
  width: 42%;
  padding: 3.5rem 3rem;
  display: flex;
  flex-direction: column;
}
.pp-badges {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.pp-badge {
  background: rgba(255,255,255,0.1);
  color: white;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 4px 12px;
  border-radius: 20px;
}
.pp-badge.featured {
  background: rgba(255,255,255,0.2);
}
.pp-subtitle {
  font-size: 11px;
  color: #D48C70;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1rem;
}
.pp-title {
  font-size: 2rem;
  font-family: var(--font-serif);
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: white;
}
.pp-desc {
  font-size: 15px;
  color: rgba(255,255,255,0.8);
  line-height: 1.6;
  margin-bottom: 2.5rem;
}
.pp-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2.5rem;
}
.pp-metric {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}
.pp-metric-num {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: white;
  font-family: var(--font-serif);
}
.pp-metric-lbl {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255,255,255,0.6);
}
.pp-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: auto;
}
.pp-feature {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255,255,255,0.8);
}
.pp-fnum {
  background: rgba(255,255,255,0.1);
  color: white;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 10px;
}
.pp-right {
  background: #FAF8F5;
  width: 58%;
  padding: 3.5rem 3rem;
  display: flex;
  flex-direction: column;
}
.pp-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
}
.pp-box {
  background: white;
  border: 1px solid #EAE3D8;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.pp-box-title {
  font-size: 10px;
  color: #D48C70;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1rem;
}
.pp-box-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--ink-2);
}
.pp-box-content ul {
  list-style: disc;
  padding-left: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.pp-box-content li {
  color: var(--ink-2);
}
.pp-stack-title {
  font-size: 10px;
  color: #8C949D;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 1rem;
}
.pp-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.pp-tag {
  background: white;
  border: 1px solid #EAE3D8;
  color: var(--ink-2);
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 20px;
  font-family: var(--font-mono);
}

@media (max-width: 900px) {
  .premium-project { flex-direction: column; }
  .pp-left, .pp-right { width: 100%; padding: 2.5rem 1.5rem; }
  .pp-grid { grid-template-columns: 1fr; }
}
"""

html_template = """
    <!-- {KEY_UP} — featured -->
    <div class="premium-project">
      <div class="pp-left">
        <div class="pp-badges">
          <span class="pp-badge" data-i18n="proj.{KEY}.badge">Production · B2B SaaS</span>
          <span class="pp-badge featured">FEATURED</span>
        </div>
        <div class="pp-subtitle" data-i18n="proj.{KEY}.sub">Qkare · Applied ML Research</div>
        <h3 class="pp-title" data-i18n="proj.{KEY}.title">Title</h3>
        <p class="pp-desc" data-i18n-html="proj.{KEY}.desc">Description</p>
        
        <div class="pp-metrics">
          <div class="pp-metric">
            <div class="pp-metric-num" data-i18n="proj.{KEY}.m1"></div>
            <div class="pp-metric-lbl">METRIC 1</div>
          </div>
          <div class="pp-metric">
            <div class="pp-metric-num" data-i18n="proj.{KEY}.m2"></div>
            <div class="pp-metric-lbl">METRIC 2</div>
          </div>
          <div class="pp-metric">
            <div class="pp-metric-num" data-i18n="proj.{KEY}.m3"></div>
            <div class="pp-metric-lbl">METRIC 3</div>
          </div>
        </div>

        <div class="pp-features">
          <div class="pp-feature"><span class="pp-fnum">01</span> <span data-i18n="proj.{KEY}.c1.title">Feature 1</span></div>
          <div class="pp-feature"><span class="pp-fnum">02</span> <span data-i18n="proj.{KEY}.c2.title">Feature 2</span></div>
          <div class="pp-feature"><span class="pp-fnum">03</span> <span data-i18n="proj.{KEY}.c3.title">Feature 3</span></div>
          <div class="pp-feature"><span class="pp-fnum">04</span> <span data-i18n="proj.{KEY}.c4.title">Feature 4</span></div>
        </div>
      </div>

      <div class="pp-right">
        <div class="pp-grid">
          <div class="pp-box">
            <div class="pp-box-title">PROBLEM</div>
            <div class="pp-box-content" data-i18n-html="proj.{KEY}.problem">Problem...</div>
          </div>
          <div class="pp-box">
            <div class="pp-box-title">MY CONTRIBUTION</div>
            <div class="pp-box-content" data-i18n-html="proj.{KEY}.contribution">Contribution...</div>
          </div>
          <div class="pp-box">
            <div class="pp-box-title">IMPACT</div>
            <div class="pp-box-content" data-i18n-html="proj.{KEY}.impact">Impact...</div>
          </div>
          <div class="pp-box">
            <div class="pp-box-title">SOLUTION / TECHNICAL APPROACH</div>
            <div class="pp-box-content">
              <ul>
                <li data-i18n-html="proj.{KEY}.solution1">Sol 1</li>
                <li data-i18n-html="proj.{KEY}.solution2">Sol 2</li>
                <li data-i18n-html="proj.{KEY}.solution3">Sol 3</li>
                <li data-i18n-html="proj.{KEY}.solution4">Sol 4</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="pp-stack">
          <div class="pp-stack-title">TECH STACK</div>
          <div class="pp-tags">
            {STACK_HTML}
          </div>
        </div>
      </div>
    </div>
"""

stacks = {
    "analytics": ["dbt Core 1.11", "PostgreSQL 16", "Apache Superset 6", "FastAPI", "Native RLS", "FDW", "Kubernetes"],
    "coach": ["LangGraph", "FastAPI", "POML", "OpenAI Realtime", "Langfuse", "Streamlit", "WebSocket"],
    "analyzer": ["LangChain", "LangGraph", "FastAPI", "PostgreSQL RLS", "OpenAI Realtime", "Langfuse", "JWT Auth"],
    "kpi": ["FastAPI", "APQC Taxonomies", "Redis", "OpenAI API", "LLM-as-judge", "Pydantic"]
}

# Update HTML
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Insert CSS before </style>
if "/* ── PREMIUM PROJECTS ── */" not in html:
    html = html.replace("</style>", css_code + "\n</style>")

# Replace the 4 ga-project divs with premium-project divs
# Use regex to find and replace the whole ga-project block for each.
for key in ["analytics", "coach", "analyzer", "kpi"]:
    # Match from <!-- KEY — featured --> up to the next <!--
    pattern = rf"<!-- {key.upper()} — featured -->.*?</div>\n    </div>\n"
    
    stack_html = "\n            ".join([f'<span class="pp-tag">{s}</span>' for s in stacks[key]])
    new_html = html_template.replace("{KEY}", key).replace("{KEY_UP}", key.upper()).replace("{STACK_HTML}", stack_html)
    
    html = re.sub(pattern, new_html, html, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Update complete")
