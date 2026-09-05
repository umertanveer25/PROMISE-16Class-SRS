# PROMISE-16Class-SRS Benchmark Dataset 🚀

[![Dataset Version](https://img.shields.io/badge/Dataset-PROMISE__EXP__16Class-blue.svg)](https://github.com/umertanveer25/PROMISE-16Class-SRS)
[![Compliance](https://img.shields.io/badge/Standard-ISO%2FIEC%2029148%20%7C%20ISO%2020926-green.svg)](https://github.com/umertanveer25/PROMISE-16Class-SRS)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-informational.svg)](https://www.python.org/)

Official GitHub repository for **PROMISE-16Class-SRS**: The First Fine-Grained 16-Class Software Requirements Engineering (SRS) Benchmark Dataset.

---

## 📌 Abstract & Overview

Traditional Requirements Engineering (RE) benchmarks evaluate models on coarse-grained binary classification (`Functional` vs. `Non-Functional`) or multi-class NFR classification (`Security`, `Performance`, etc.). However, functional requirements (`F`) account for up to **61.4%** of real-world SRS specifications without any standardized sub-classification.

**PROMISE-16Class-SRS** addresses this fundamental gap by sub-classifying Functional Requirements into **5 ISO/IEC 29148 & ISO 20926 compliant Functional Sub-Classes**:
1. `FR-UI` — User Interface & Visual Display
2. `FR-Data` — Database Persistence & Data Processing
3. `FR-Logic` — Business Logic, Rules & Calculations
4. `FR-Integration` — Third-Party APIs, Services & System Protocols
5. `FR-Notification` — User Alerts, Email & SMS Dispatching

Combined with the 11 original Non-Functional (NFR) classes, **PROMISE-16Class-SRS** provides a unified 16-class fine-grained benchmark.

---

## 📊 Dataset Statistics & Class Distribution

### 1. Expanded Benchmark (`PROMISE_EXP_FineGrained_16Class.csv` — 3,677 Samples)

| Class Category | Class Name | Description | Sample Count | Imbalance Ratio (IR) |
| :--- | :--- | :--- | :---: | :---: |
| **Functional** | `FR-Integration` | External APIs & System Protocols | 831 | 23.74 : 1 |
| **Functional** | `FR-UI` | Interface Displays & User Controls | 826 | 23.60 : 1 |
| **Functional** | `FR-Data` | Database Persistence & Records | 354 | 10.11 : 1 |
| **Functional** | `FR-Notification` | Alerts, Emails & User Prompts | 150 | 4.29 : 1 |
| **Functional** | `FR-Logic` | Business Calculations & Rules | 97 | 2.77 : 1 |
| **Non-Functional** | `NFR-SE` | Security | 237 | 6.77 : 1 |
| **Non-Functional** | `NFR-US` | Usability | 212 | 6.06 : 1 |
| **Non-Functional** | `NFR-L` | Legal & Compliance | 209 | 5.97 : 1 |
| **Non-Functional** | `NFR-PE` | Performance | 163 | 4.66 : 1 |
| **Non-Functional** | `NFR-O` | Operational | 157 | 4.49 : 1 |
| **Non-Functional** | `NFR-SC` | Scalability | 95 | 2.71 : 1 |
| **Non-Functional** | `NFR-LF` | Look & Feel | 89 | 2.54 : 1 |
| **Non-Functional** | `NFR-PO` | Portability | 76 | 2.17 : 1 |
| **Non-Functional** | `NFR-MN` | Maintainability | 75 | 2.14 : 1 |
| **Non-Functional** | `NFR-A` | Availability | 71 | 2.03 : 1 |
| **Non-Functional** | `NFR-FT` | Fault Tolerance | 35 | 1.00 : 1 |
| **Total** | **16 Classes** | **Full Benchmark** | **3,677** | **Max IR: 23.74 : 1** |

---

## 🛠️ Multi-Factor Context-Aware Hybrid Classification Engine

To assign bulletproof functional sub-classes, we utilize a **Multi-Factor Hybrid Engine** combining four contextual factors:

$$\text{Score}(c) = 0.50 \cdot S_{\text{semantic}}(c) + 0.20 \cdot W_{\text{action}}(c) + 0.15 \cdot W_{\text{role}}(c) + 0.15 \cdot W_{\text{domain}}(c)$$

1. **Semantic Vector Cosine Similarity ($S_{\text{semantic}}$):** SBERT / TF-IDF prototype embedding alignment.
2. **Action Verb Dependency ($W_{\text{action}}$):** POS tag extraction of root operational verbs (`calculate`, `store`, `render`, `notify`, `integrate`).
3. **Grammatical Target Entity Context ($W_{\text{role}}$):** Extracting direct object nouns (`screen`, `table`, `tax formula`, `email`, `API`).
4. **ISO 29148 Domain Heuristics ($W_{\text{domain}}$):** Pattern matching against ISO/IEC standard function definitions.

---

## 📁 Repository Structure

```
PROMISE-16Class-SRS/
├── README.md
├── PROMISE_EXP_FineGrained_16Class.csv   # 3,677-row Expanded Benchmark
├── PROMISE_FineGrained_16Class_969.csv   # 969-row Standard Benchmark
└── build_fine_grained_promise_exp.py     # Multi-Factor Dataset Generator Script
```

---

## 📖 Citation & Reference

If you utilize this benchmark dataset in your research, please cite:

```bibtex
@article{tanveer2026promise16class,
  title={PROMISE-16Class-SRS: A Fine-Grained 16-Class Benchmark Dataset for Software Requirements Engineering},
  author={Tanveer, Umer and Ali, Hashim and Hayat, Maqsood},
  journal={IEEE Transactions on Software Engineering / Software Quality Journal},
  year={2026}
}
```

---

## 📄 License

This dataset and code are released under the [MIT License](LICENSE).
