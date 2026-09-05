import os
import re
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Functional Sub-Class Lexicons & Prototype Definitions (ISO 29148 / ISO 20926 Compliant)
PROTOTYPES = {
    'FR-UI': (
        "user interface screen display view show button form menu layout page render click select input "
        "dialog window visual interface dashboard gui icon tab text box checkbox drop-down theme navigation"
    ),
    'FR-Data': (
        "store database save record table field query fetch delete update insert persist archive repository "
        "dataset backup export import sql entity schema column index retrieval data storage file entry"
    ),
    'FR-Logic': (
        "calculate compute process validation rule business logic verify check evaluate score tax interest "
        "algorithm formula decision determine aggregate total count transform compare analyze workflow condition"
    ),
    'FR-Integration': (
        "api external system interface integrate service call endpoint protocol import export web service "
        "third-party connector socket rest soap sync middleware Gateway backend system communication payload"
    ),
    'FR-Notification': (
        "notify alert email sms message send warn broadcast push notification inform prompt pop-up signal "
        "text message dispatch transmission confirmation alert message reminder user notification"
    )
}

# Domain Action Verbs
ACTION_VERBS = {
    'FR-UI': {'display', 'show', 'render', 'click', 'select', 'navigate', 'view', 'press', 'toggle', 'enter', 'open', 'close', 'browse', 'format'},
    'FR-Data': {'store', 'save', 'persist', 'delete', 'update', 'query', 'fetch', 'archive', 'insert', 'retrieve', 'backup', 'export', 'import'},
    'FR-Logic': {'calculate', 'compute', 'validate', 'verify', 'evaluate', 'process', 'determine', 'generate', 'score', 'convert', 'aggregate', 'summarize', 'apply', 'compare'},
    'FR-Integration': {'connect', 'interface', 'transmit', 'receive', 'sync', 'integrate', 'call', 'communicate', 'fetch', 'post', 'request'},
    'FR-Notification': {'notify', 'alert', 'email', 'send', 'warn', 'broadcast', 'inform', 'push', 'signal', 'remind', 'dispatch'}
}

# Entity Target Keywords
ROLE_KEYWORDS = {
    'FR-UI': {'screen', 'display', 'button', 'menu', 'page', 'layout', 'window', 'form', 'gui', 'tab', 'textbox', 'icon', 'dropdown', 'interface'},
    'FR-Data': {'database', 'db', 'table', 'record', 'field', 'column', 'file', 'storage', 'dataset', 'repository', 'archive', 'schema'},
    'FR-Logic': {'tax', 'interest', 'rule', 'formula', 'total', 'discount', 'amount', 'score', 'rate', 'validation', 'calculation', 'logic'},
    'FR-Integration': {'api', 'service', 'gateway', 'third-party', 'system', 'endpoint', 'server', 'protocol', 'rest', 'soap', 'connector'},
    'FR-Notification': {'email', 'sms', 'message', 'alert', 'notification', 'reminder', 'broadcast', 'push', 'mail'}
}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]
    return ' '.join(tokens), tokens

# Pre-build prototype vectors for Semantic Cosine Factor
proto_labels = list(PROTOTYPES.keys())
proto_texts = [PROTOTYPES[k] for k in proto_labels]
vectorizer = TfidfVectorizer().fit(proto_texts)
proto_vectors = vectorizer.transform(proto_texts)

def classify_functional_req(req_text):
    cleaned_str, tokens = clean_text(req_text)
    if not tokens:
        return 'FR-Logic' # Fallback default
    
    # 1. Semantic Vector Cosine Similarity (S_semantic)
    req_vec = vectorizer.transform([cleaned_str])
    cos_sims = cosine_similarity(req_vec, proto_vectors)[0]
    s_semantic = {proto_labels[i]: cos_sims[i] for i in range(len(proto_labels))}
    
    # 2. Action Verb Alignment (W_action) via POS Tagging
    tagged = nltk.pos_tag(tokens)
    verbs = {w for w, pos in tagged if pos.startswith('VB')}
    
    w_action = {cls: 0.0 for cls in proto_labels}
    for cls in proto_labels:
        matches = verbs.intersection(ACTION_VERBS[cls])
        if matches:
            w_action[cls] = len(matches) * 0.35
            
    # 3. Direct Object & Entity Role Context (W_role)
    nouns = {w for w, pos in tagged if pos.startswith('NN')}
    w_role = {cls: 0.0 for cls in proto_labels}
    for cls in proto_labels:
        matches = nouns.intersection(ROLE_KEYWORDS[cls])
        if matches:
            w_role[cls] = len(matches) * 0.25
            
    # 4. Domain Keyword & Modality Heuristics (W_domain)
    w_domain = {cls: 0.0 for cls in proto_labels}
    text_lower = req_text.lower()
    
    if re.search(r'\b(email|sms|alert|notify|notification|message to user)\b', text_lower):
        w_domain['FR-Notification'] += 0.4
    if re.search(r'\b(screen|display|ui|button|click|view|show user|form|gui)\b', text_lower):
        w_domain['FR-UI'] += 0.3
    if re.search(r'\b(database|store|save|db|table|record|persist|delete from)\b', text_lower):
        w_domain['FR-Data'] += 0.3
    if re.search(r'\b(api|external|integrate|third-party|web service|endpoint)\b', text_lower):
        w_domain['FR-Integration'] += 0.35
    if re.search(r'\b(calculate|compute|formula|validation|interest|tax|verify rule)\b', text_lower):
        w_domain['FR-Logic'] += 0.3
        
    # Unified Hybrid Multi-Factor Formula:
    # Score = 0.50 * S_semantic + 0.20 * W_action + 0.15 * W_role + 0.15 * W_domain
    final_scores = {}
    for cls in proto_labels:
        score = (0.50 * s_semantic[cls]) + (0.20 * w_action[cls]) + (0.15 * w_role[cls]) + (0.15 * w_domain[cls])
        final_scores[cls] = score
        
    # Return highest scoring Functional Sub-Class
    best_cls = max(final_scores, key=final_scores.get)
    return best_cls

def main():
    dataset_path = 'B:/Umer Data/Research/Phase 1/promise.csv'
    if not os.path.exists(dataset_path):
        dataset_path = 'B:/Promise/nfr.csv'
        
    print(f"Loading raw PROMISE dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path, encoding='latin1')
    
    class_col = 'Class' if 'Class' in df.columns else 'class'
    req_col = 'RequirementText' if 'RequirementText' in df.columns else 'requirement'
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original Class distribution:\n{df[class_col].value_counts()}\n")
    
    fine_grained_labels = []
    
    for idx, row in df.iterrows():
        orig_cls = str(row[class_col]).strip()
        req_txt = str(row[req_col])
        
        if orig_cls.upper() == 'F':
            # Sub-classify Functional Requirement into 5 granular classes
            fg_cls = classify_functional_req(req_txt)
        else:
            # Format Non-Functional Requirement class name
            fg_cls = f"NFR-{orig_cls.upper()}"
            
        fine_grained_labels.append(fg_cls)
        
    df['fine_grained_class'] = fine_grained_labels
    
    output_dir = r'C:\Users\umert\.gemini\antigravity\brain\3c8ef2d2-19ed-4816-bf7e-5ae4601d1469'
    output_path = os.path.join(output_dir, 'PROMISE_EXP_FineGrained_16Class.csv')
    df.to_csv(output_path, index=False)
    print(f"[OK] Fine-Grained 16-Class Dataset successfully generated and saved to:\n   {output_path}\n")
    
    dist = df['fine_grained_class'].value_counts()
    print("==========================================================")
    print("      PROMISE_EXP Fine-Grained 16-Class Distribution      ")
    print("==========================================================")
    for cls_name, count in dist.items():
        pct = (count / len(df)) * 100
        print(f"  {cls_name:<20}: {count:>5} samples ({pct:>5.2f}%)")
    print("----------------------------------------------------------")
    
    max_c = dist.max()
    min_c = dist.min()
    ir = max_c / min_c
    print(f"Total Requirements : {len(df)}")
    print(f"Total Classes      : {len(dist)}")
    print(f"Max Class Count    : {dist.index[0]} ({max_c})")
    print(f"Min Class Count    : {dist.index[-1]} ({min_c})")
    print(f"Imbalance Ratio    : {ir:.2f} : 1")
    print("==========================================================")
    
    # Display sample rows of each FR sub-class for verification
    print("\nSample Sub-Classified Requirements:")
    fr_df = df[df['fine_grained_class'].str.startswith('FR-')]
    for sub_c in ['FR-UI', 'FR-Data', 'FR-Logic', 'FR-Integration', 'FR-Notification']:
        sample = fr_df[fr_df['fine_grained_class'] == sub_c].head(2)
        print(f"\n--- {sub_c} ---")
        for _, s_row in sample.iterrows():
            print(f"  [{s_row[class_col]} -> {s_row['fine_grained_class']}]: {s_row[req_col][:100]}...")

if __name__ == '__main__':
    main()
