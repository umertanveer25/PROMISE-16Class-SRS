import os
import pandas as pd
import numpy as np

def audit_dataset(file_path, name):
    print("=" * 70)
    print(f"               AUDIT REPORT: {name}               ")
    print("=" * 70)
    
    if not os.path.exists(file_path):
        print(f"ERROR: Dataset file not found at {file_path}")
        return None
        
    df = pd.read_csv(file_path)
    total_rows = len(df)
    
    # 1. Null / Missing Checks
    null_counts = df.isnull().sum().to_dict()
    print(f"1. DATA INTEGRITY & NULL CHECK:")
    print(f"   Total Samples : {total_rows}")
    print(f"   Total Columns : {len(df.columns)} ({df.columns.tolist()})")
    print(f"   Null Values   : {null_counts}")
    
    # 2. Duplicate Checks
    req_col = [c for c in df.columns if 'req' in c.lower() or 'text' in c.lower()][0]
    duplicates = df[req_col].duplicated().sum()
    print(f"\n2. DUPLICATE TEXT CHECK:")
    print(f"   Exact Duplicate Requirements : {duplicates} ({duplicates/total_rows*100:.2f}%)")
    
    # 3. Class Distribution & Imbalance
    cls_col = 'fine_grained_class'
    dist = df[cls_col].value_counts()
    print(f"\n3. 16-CLASS DISTRIBUTION AUDIT:")
    
    fr_classes = [c for c in dist.index if c.startswith('FR-')]
    nfr_classes = [c for c in dist.index if c.startswith('NFR-')]
    
    fr_count = df[df[cls_col].isin(fr_classes)].shape[0]
    nfr_count = df[df[cls_col].isin(nfr_classes)].shape[0]
    
    print(f"   Functional Sub-Classes Total     : {fr_count} ({fr_count/total_rows*100:.2f}%)")
    print(f"   Non-Functional Classes Total     : {nfr_count} ({nfr_count/total_rows*100:.2f}%)")
    print("-" * 70)
    print(f"   {'Class Label':<20} | {'Sample Count':<12} | {'Percentage':<10} | {'Category'}")
    print("-" * 70)
    
    for cls_name, count in dist.items():
        pct = (count / total_rows) * 100
        cat = "Functional Sub-Class" if cls_name.startswith('FR-') else "Quality NFR Class"
        print(f"   {cls_name:<20} | {count:>12} | {pct:>9.2f}% | {cat}")
        
    print("-" * 70)
    max_c = dist.max()
    min_c = dist.min()
    max_cls = dist.index[0]
    min_cls = dist.index[-1]
    ir = max_c / min_c
    print(f"   Majority Class : {max_cls} ({max_c})")
    print(f"   Minority Class : {min_cls} ({min_c})")
    print(f"   Imbalance Ratio: {ir:.2f} : 1")
    print("=" * 70)
    
    # 4. Verification Exemplars
    print(f"\n4. VERIFICATION EXEMPLARS PER SUB-CLASS:")
    for cls_name in fr_classes:
        sample_txt = df[df[cls_col] == cls_name][req_col].iloc[0]
        cleaned_txt = sample_txt.replace('\n', ' ').strip()
        print(f"   [{cls_name}]: \"{cleaned_txt[:90]}...\"")
    print("=" * 70 + "\n")
    
    return {
        'total': total_rows,
        'fr_count': fr_count,
        'nfr_count': nfr_count,
        'num_classes': len(dist),
        'imbalance_ratio': ir,
        'distribution': dist
    }

def main():
    base_dir = r"C:\Users\umert\.gemini\antigravity\brain\3c8ef2d2-19ed-4816-bf7e-5ae4601d1469"
    exp_path = os.path.join(base_dir, "PROMISE_EXP_FineGrained_16Class.csv")
    std_path = os.path.join(base_dir, "PROMISE_FineGrained_16Class_969.csv")
    
    audit_exp = audit_dataset(exp_path, "PROMISE_EXP 16-Class Benchmark (3,677 Rows)")
    audit_std = audit_dataset(std_path, "PROMISE Standard 16-Class Benchmark (969 Rows)")

if __name__ == '__main__':
    main()
