# PROMISE-16Class-SRS Benchmark Dataset 🚀

[![Dataset Version](https://img.shields.io/badge/Dataset-PROMISE__16Class__969-blue.svg)](https://github.com/umertanveer25/PROMISE-16Class-SRS)
[![Samples](https://img.shields.io/badge/Samples-969-orange.svg)](https://github.com/umertanveer25/PROMISE-16Class-SRS)
[![Compliance](https://img.shields.io/badge/Standard-ISO%2FIEC%2029148%20%7C%20ISO%2020926-green.svg)](https://github.com/umertanveer25/PROMISE-16Class-SRS)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

Official GitHub repository for **PROMISE-16Class-SRS**: The First Fine-Grained 16-Class Software Requirements Engineering (SRS) Benchmark Dataset (969 Requirements).

---

## 📌 Abstract & Overview

Traditional Requirements Engineering (RE) benchmarks evaluate models on coarse-grained binary classification (`Functional` vs. `Non-Functional`) or multi-class NFR classification (`Security`, `Performance`, etc.). However, functional requirements (`F`) account for **45.82%** of the standard 969-requirement PROMISE benchmark without any standardized sub-classification.

**PROMISE-16Class-SRS** sub-classifies the 444 Functional Requirements in `PROMISE` into **5 ISO/IEC 29148 & ISO 20926 compliant Functional Sub-Classes**:
1. `FR-UI` — User Interface & Visual Display (187 samples)
2. `FR-Integration` — Third-Party APIs, Services & Protocols (171 samples)
3. `FR-Data` — Database Persistence & Data Processing (37 samples)
4. `FR-Notification` — User Alerts, Email & SMS Dispatching (31 samples)
5. `FR-Logic` — Business Logic, Rules & Calculations (18 samples)

Combined with the 11 original Non-Functional (NFR) quality classes, **PROMISE-16Class-SRS** provides a unified 16-class fine-grained benchmark on the **969 standard requirements dataset**.

---

## 📊 16-Class Dataset Distribution (969 Requirements)

| Class Category | Class Name | Description | Sample Count | Percentage | Imbalance Ratio (IR) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Functional** | `FR-UI` | User Interface & Visual Displays | 187 | 19.30% | 15.58 : 1 |
| **Functional** | `FR-Integration` | System APIs & Protocols | 171 | 17.65% | 14.25 : 1 |
| **Non-Functional** | `NFR-SE` | Security | 125 | 12.90% | 10.42 : 1 |
| **Non-Functional** | `NFR-US` | Usability | 85 | 8.77% | 7.08 : 1 |
| **Non-Functional** | `NFR-O` | Operational | 77 | 7.95% | 6.42 : 1 |
| **Non-Functional** | `NFR-PE` | Performance | 67 | 6.91% | 5.58 : 1 |
| **Non-Functional** | `NFR-LF` | Look & Feel | 49 | 5.06% | 4.08 : 1 |
| **Functional** | `FR-Data` | Database Persistence & Records | 37 | 3.82% | 3.08 : 1 |
| **Non-Functional** | `NFR-A` | Availability | 31 | 3.20% | 2.58 : 1 |
| **Functional** | `FR-Notification` | Email/SMS Alerts & Notifications | 31 | 3.20% | 2.58 : 1 |
| **Non-Functional** | `NFR-MN` | Maintainability | 24 | 2.48% | 2.00 : 1 |
| **Non-Functional** | `NFR-SC` | Scalability | 22 | 2.27% | 1.83 : 1 |
| **Functional** | `FR-Logic` | Business Calculations & Rules | 18 | 1.86% | 1.50 : 1 |
| **Non-Functional** | `NFR-FT` | Fault Tolerance | 18 | 1.86% | 1.50 : 1 |
| **Non-Functional** | `NFR-L` | Legal & Compliance | 15 | 1.55% | 1.25 : 1 |
| **Non-Functional** | `NFR-PO` | Portability | 12 | 1.24% | 1.00 : 1 |
| **Total** | **16 Classes** | **Standard PROMISE Benchmark** | **969** | **100.00%** | **Max IR: 15.58 : 1** |

---

## 🛠️ Multi-Factor Context-Aware Hybrid Classification Engine

Sub-class labels are generated via a **Multi-Factor Hybrid Engine** combining four contextual factors:

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
├── PROMISE_FineGrained_16Class_969.csv   # Primary 969-row Benchmark Dataset
├── audit_fine_grained_dataset.py         # Audit & Verification Script
└── build_fine_grained_969.py             # Multi-Factor Dataset Generator Script
```

---

## 📖 Citation & Reference

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
