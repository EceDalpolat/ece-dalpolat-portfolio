import json

def balance_ai_emphasis(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements_en = {
        "multi-tenant HR analytics stack": "multi-tenant enterprise analytics stack",
        "HR analytics decisions": "enterprise analytics decisions",
        "HR AI platform": "B2B AI platform",
        "psychometric assessment data (AON cognitive, Saville behavioural, Assessment Center)": "complex behavioral and cognitive data",
        "psychometric data": "domain-specific behavioral data",
        "natural-language HR questions": "natural-language business intelligence queries",
        "answers natural-language HR questions": "answers natural-language analytical questions",
        "HR teams": "business teams",
        "HR evaluators": "domain experts",
        "downstream HR workflows": "downstream enterprise workflows",
        "raw HR/assessment inputs": "raw behavioral inputs",
    }
    
    replacements_tr = {
        "çok kiracılı İK analitik yığınının": "çok kiracılı kurumsal analitik yığınının",
        "İK analitik kararlarına": "kurumsal analitik kararlarına",
        "İK AI platformunda": "B2B AI platformunda",
        "psikometrik veri": "davranışsal veri",
        "doğal dilde İK sorularını": "doğal dilde iş zekası sorgularını",
        "İK sorularını": "iş zekası sorgularını",
        "İK ekiplerinin": "iş ekiplerinin",
        "İK değerlendiricileri": "alan uzmanları",
        "downstream İK iş akışları": "kurumsal iş akışları",
        "ham İK/değerlendirme girdilerini": "ham davranışsal verileri",
    }

    if "en.json" in filepath:
        reps = replacements_en
    else:
        reps = replacements_tr

    for old, new in reps.items():
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

balance_ai_emphasis("i18n/en.json")
balance_ai_emphasis("i18n/tr.json")
print("AI emphasis balanced.")
