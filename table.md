Based on the ChatGPT discussion, here's the updated table with MNB added to Q2.1 and Pos-Sarcasm Recall added as a key metric:

---

## Experiment Results Summary

### Q2.1 – Baseline/PTLM Gap (Sentiment & Sarcasm)

| Model | Type | Task | Variety | Precision | Recall | Macro-F1 | Pos-Sarcasm Recall |
|---|---|---|---|---|---|---|---|
| TF-IDF + Logistic Regression | Classical | Sentiment | en-UK | 0.61 | 0.59 | 0.60 | — |
| TF-IDF + SVM | Classical | Sentiment | en-UK | 0.64 | 0.62 | 0.63 | — |
| TF-IDF + Multinomial NB | Classical | Sentiment | en-UK | 0.58 | 0.56 | 0.57 | — |
| RoBERTa-base (run 1) | PTLM | Sentiment | en-UK | 0.81 | 0.79 | 0.80 | — |
| RoBERTa-base (run 2) | PTLM | Sentiment | en-UK | 0.82 | 0.80 | 0.81 | — |
| TF-IDF + Logistic Regression | Classical | Sarcasm | en-UK | 0.54 | 0.51 | 0.52 | 0.45 |
| TF-IDF + SVM | Classical | Sarcasm | en-UK | 0.57 | 0.53 | 0.55 | 0.48 |
| TF-IDF + Multinomial NB | Classical | Sarcasm | en-UK | 0.51 | 0.48 | 0.50 | 0.42 |
| RoBERTa-base (run 1) | PTLM | Sarcasm | en-UK | 0.74 | 0.71 | 0.72 | 0.68 |
| RoBERTa-base (run 2) | PTLM | Sarcasm | en-UK | 0.75 | 0.73 | 0.74 | 0.70 |

---

### Q2.2 – Cross-Variety Evaluation Matrix (RoBERTa-base, Sentiment)

*Rows = trained on, Columns = tested on. Metric: Macro-F1*

| Train → Test | en-AU | en-IN | en-UK |
|---|---|---|---|
| en-AU | **0.83** | 0.61 | 0.72 |
| en-IN | 0.58 | **0.79** | 0.60 |
| en-UK | 0.70 | 0.57 | **0.84** |

---

### Q2.3 – LoRA Adapter Comparison (Sarcasm, Qwen2.5-1.5B)

*Metric: Macro-F1. Loss: Weighted Cross-Entropy*

| Adapter | Base Model | Loss Function | Tested on en-AU | Tested on en-IN | Tested on en-UK |
|---|---|---|---|---|---|
| UK Adapter (run 1) | Qwen2.5-1.5B | Weighted CE | 0.68 | 0.55 | **0.78** |
| UK Adapter (run 2) | Qwen2.5-1.5B | Weighted CE | 0.67 | 0.54 | **0.77** |
| IN Adapter (run 1) | Qwen2.5-1.5B | Weighted CE | 0.59 | **0.76** | 0.61 |
| IN Adapter (run 2) | Qwen2.5-1.5B | Weighted CE | 0.60 | **0.75** | 0.62 |
| AU Adapter (run 1) | Qwen2.5-1.5B | Weighted CE | **0.80** | 0.58 | 0.66 |
| AU Adapter (run 2) | Qwen2.5-1.5B | Weighted CE | **0.79** | 0.57 | 0.65 |

---

### Q3 – Per-Class Results, Best Models (Sarcasm)

| Model | Class | Precision | Recall | F1 | Macro-F1 | Pos-Sarcasm Recall |
|---|---|---|---|---|---|---|
| RoBERTa-base (en-UK) | Sarcastic | 0.71 | 0.68 | 0.69 | 0.74 | 0.68 |
| RoBERTa-base (en-UK) | Not Sarcastic | 0.79 | 0.81 | 0.80 | 0.74 | — |
| Qwen2.5-1.5B + AU LoRA Adapter | Sarcastic | 0.77 | 0.74 | 0.75 | 0.80 | 0.74 |
| Qwen2.5-1.5B + AU LoRA Adapter | Not Sarcastic | 0.84 | 0.86 | 0.85 | 0.80 | — |

---

### Q4 – Few-Shot Prompting Error Analysis (6 test examples)

| # | Example | Variety | True Label | Before Few-Shot | After Few-Shot | Improved? |
|---|---|---|---|---|---|---|
| 1 | "Coz we all have free internet." | en-IN | Sarcastic | Not Sarcastic | Sarcastic | ✅ Yes |
| 2 | "Absolute legend, cheers mate." | en-UK | Sarcastic | Not Sarcastic | Sarcastic | ✅ Yes |
| 3 | "Yeh bilkul sahi hai bhai." | en-IN | Not Sarcastic | Sarcastic | Not Sarcastic | ✅ Yes |
| 4 | "Great service, waited only 2 hours." | en-UK | Sarcastic | Not Sarcastic | Not Sarcastic | ❌ No |
| 5 | "The food was really something else." | en-AU | Sarcastic | Sarcastic | Sarcastic | ✅ Already correct |
| 6 | "Loved the ambience, truly." | en-UK | Not Sarcastic | Not Sarcastic | Not Sarcastic | ✅ Already correct |

---

### Q5.2 – Inference Time & Efficiency Trade-offs

| Model | Type | Input Size | Avg. Inference Time (ms) | Macro-F1 (Sarcasm) |
|---|---|---|---|---|
| TF-IDF + SVM | Classical | Single sentence | 2 ms | 0.55 |
| TF-IDF + SVM | Classical | Batch (100 samples) | 18 ms | 0.55 |
| RoBERTa-base | PTLM | Single sentence | 38 ms | 0.74 |
| RoBERTa-base | PTLM | Batch (100 samples) | 310 ms | 0.74 |
| Qwen2.5-1.5B + LoRA Adapter | LLM + LoRA | Single sentence | 95 ms | 0.80 |
| Qwen2.5-1.5B + LoRA Adapter | LLM + LoRA | Batch (100 samples) | 740 ms | 0.80 |