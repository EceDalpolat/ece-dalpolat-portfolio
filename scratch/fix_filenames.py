import json

def replace_in_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements_en = {
        "apply_native_rls post-hook macro": "native RLS deployment macros",
        "feature_engineering.py": "feature engineering pipelines",
        "clustering_model.py and advanced_model.py": "modular clustering pipelines",
        "EDA.py": "exploratory data analysis modules",
        "autoMl1.py": "automated model search modules",
        "multi_cluster_analysis.py": "cross-algorithm analysis tools",
        "voice_config.py": "voice configuration modules",
        "master_prompt.yaml": "master prompt configurations",
        "tools/__init__": "module initialization",
        "base_llm.py": "core LLM processing modules",
        "main.py": "the application entry point",
        "API.md": "API documentation",
        "generate_agents_pipeline.py": "pipeline generation scripts",
        "app.py": "the main orchestration layer",
        "security/hybrid_security.py": "hybrid security modules",
        "config.py": "centralized configuration modules"
    }
    
    replacements_tr = {
        "apply_native_rls post-hook makrosu": "doğal RLS dağıtım makroları",
        "feature_engineering.py ile": "Özellik mühendisliği (feature engineering) boru hatları ile",
        "clustering_model.py ve advanced_model.py ile": "Modüler kümeleme algoritmaları ile",
        "Keşifsel profilleme için EDA.py;": "Keşifsel veri analizi modülleri kullanılarak;",
        "autoMl1.py;": "otomatik model arama modülleri;",
        "aktarmak için multi_cluster_analysis.py.": "aktarmak için çapraz algoritma analiz araçları geliştirdim.",
        "voice_config.py ve": "ses konfigürasyon modülleri ve",
        "master_prompt.yaml render'ını": "Ana prompt (master prompt) yapılandırmalarının derlenmesini",
        "tools/__init__": "modül ilklendirme (init)",
        "base_llm.py'de": "Çekirdek LLM işlem modüllerinde",
        "main.py'de": "uygulama giriş noktasında",
        "API.md entegrasyon": "API dokümantasyonu entegrasyon",
        "generate_agents_pipeline.py;": "pipeline (boru hattı) üretim betikleri;",
        "app.py'de": "Ana orkestrasyon katmanında",
        "security/hybrid_security.py": "Hibrit güvenlik modülleri,",
        "config.py'de": "merkezi konfigürasyon modüllerinde"
    }

    if "en.json" in filepath:
        reps = replacements_en
    else:
        reps = replacements_tr

    for old, new in reps.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

replace_in_json("i18n/en.json")
replace_in_json("i18n/tr.json")
print("JSON replacements complete.")
