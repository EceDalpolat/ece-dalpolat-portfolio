# Ön Yazı — GenAI / LLM Engineer (Fenix İK)

**Ece Dalpolat**  
ecedlplt9850@gmail.com · +90 552 360 9850 · İstanbul  
[Portföy](https://ecedalpolat.github.io/ece-dalpolat-portfolio/) · [LinkedIn](https://www.linkedin.com/in/ece-dalpolat-0265a0221/) · [GitHub](https://github.com/EceDalpolat)

---

Sayın Yetkili,

Fenix İnsan Kaynakları bünyesinde yayınlanan GenAI / LLM Engineer ilanınızı ilgiyle inceledim. İlanda tarif edilen “POC’ten production’a taşıma”, multi-agent mimariler ve RAG tabanlı çözümler; son bir yıldır Qkare’de günlük olarak yaptığım işin özeti. Bu nedenle başvurumu hem teknik uyum hem de üretim disiplini açısından güçlü bulduğum için yazıyorum.

**Kısaca kimim:** Yazılım mühendisliği mezunuyum, Işık Üniversitesi’nde Bilgi Teknolojileri yüksek lisansına devam ediyorum. Qkare’de Yapay Zeka Mühendisi olarak çok kiracılı İK analitik ürününde çalışıyorum; demo değil, kurumsal müşterilerin kullandığı sistemlerin ana mühendisliğini üstleniyorum. Miuul’da veri bilimi ve makine öğrenmesi öğretim asistanlığı yapıyorum.

**İlanınızdaki sorumluluklarla doğrudan örtüşen deneyimlerim:**

**Python ve production backend** — FastAPI ile mikroservisler (KPI Advisor, Skills Advisor, Analyzer API, agent gateway) tasarladım ve devreye aldım. Pydantic ile yapılandırılmış JSON çıktı, async HTTP (httpx), WebSocket (sesli koçluk ve analyzer), JWT tabanlı kimlik doğrulama ve çok kiracılı izolasyon üzerinde çalıştım.

**LLM uygulamaları ve OpenAI** — OpenAI API (JSON mode, structured output), prompt mühendisliği, token maliyeti optimizasyonu ve guardrail katmanları günlük işimin parçası. Kurumsal web sitesi chatbot’unda kural → semantik önbellek (FAISS / Milvus) → web scraping RAG → LLM cascade kurdum; hybrid prompt-injection koruması ekledim.

**LangChain ve multi-agent** — Analyzer Platform’da LangChain ReAct ajanı; Coach Platform’da LangGraph ile çok ajanlı orkestrasyon (Companion, Coach, Advisor, Mentor), POML prompt kütüphanesi ve OpenAI Realtime API ile sesli etkileşim. Referee Agent ile LLM-as-judge değerlendirme hattı kurdum (üretim öncesi kalite ölçümü).

**RAG ve vector store** — Embedding tabanlı semantik önbellek, benzerlik eşiği, cache write-back; canlı site içeriğinden RAG zeminleme (BeautifulSoup, html2text). FAISS ve Milvus ile çalıştım; chunking ve retrieval stratejisi tasarımına hakimim. (Pinecone / Qdrant / Chroma ile kavramsal deneyim aynı; yeni ortamda hızlı adapte olurum.)

**Ses (STT/TTS)** — Coach Platform’da OpenAI Realtime API, WebSocket ses sunucusu ve POML-aware ses promptları ile gerçek zamanlı sesli koçluk katmanını devreye aldım.

**Docker, CI/CD, DevOps** — GitLab CI/CD, pre-commit (Ruff, MyPy), pytest, çok aşamalı Dockerfile, per-agent Docker Compose, Kubernetes ortamında çalışma deneyimim var. Azure tarafında henüz üretim projem yok; ancak cloud-native deploy ve CI disiplinine alışığım.

**POC → production** — 8’den fazla AI sistemini “çalışıyor”dan “müşteriye açık” seviyeye taşıdım: dbt veri katmanı (109+ model, native RLS), ajanlar, danışman mikroservisleri ve merkezi agent gateway.

**Referans proje deneyimleri (ilanınızdaki maddeler):**

| İlan maddesi | Karşılığım |
|--------------|------------|
| Conversational AI / chatbot | QKare AI Assistant — cascade + güvenlik |
| RAG bilgi erişimi | Chatbot RAG katmanı; Skills Advisor’da RAG-lite |
| Multi-agent workflow | Coach Platform (LangGraph) |
| STT / sesli AI | Coach — OpenAI Realtime, WebSocket |
| Otomasyon / karar destek | KPI Advisor, Analyzer (doğal dil → SQL analitik) |

**İlanın istediği diğer başlıklar:** Hugging Face ile akademik/kişisel ML projelerimde (polen sınıflandırma, bal tahmini) model eğitimi deneyimim var; üretim fine-tuning henüz ana odağım değil ama transformer ve NLP temellerine hakimim. Agile sprint ortamında ekip içi çalışma, teknik dokümantasyon ve cross-functional iletişim Qkare’de rutinim.

**Dil:** İngilizce’yi teknik dokümantasyon, kod ve toplantılarda aktif kullanıyorum (B2; teknik bağlamda rahatım).

Üç yıllık “klasik” deneyim çizgisinde CV’m gönüllü ve araştırma rolleriyle birlikte 2022’den beri yazılım geliştiriyorum; son 12 ayı neredeyse tamamen production AI mühendisliğine ayırdım. Bu rolde değer üretebileceğime inanıyorum çünkü ilanınız “sadece model çağırmak” değil; güvenli, ölçeklenebilir ve iş hedefli sistem kurmak istiyor — tam da uzmanlaştığım alan bu.

Görüşme için uygun olduğum günleri paylaşmaktan memnuniyet duyarım. Portföyüm ve GitHub hesabım başvurumu destekleyen örnekler içeriyor.

Saygılarımla,

**Ece Dalpolat**
