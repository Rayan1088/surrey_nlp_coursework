## Experiment Results Summary

### Q2.1 – Baseline vs. Fine-tuned Transformer (Sentiment & Sarcasm)

| Model | Task | Variety | Precision | Recall | Macro-F1 |
|---|---|---|---|---|---|
| TF-IDF + Logistic Regression | Sentiment | en-UK | 0.61 | 0.59 | 0.60 |
| TF-IDF + SVM | Sentiment | en-UK | 0.64 | 0.62 | 0.63 |
| RoBERTa-base (run 1) | Sentiment | en-UK | 0.81 | 0.79 | 0.80 |
| RoBERTa-base (run 2) | Sentiment | en-UK | 0.82 | 0.80 | 0.81 |
| TF-IDF + Logistic Regression | Sarcasm | en-UK | 0.54 | 0.51 | 0.52 |
| TF-IDF + SVM | Sarcasm | en-UK | 0.57 | 0.53 | 0.55 |
| RoBERTa-base (run 1) | Sarcasm | en-UK | 0.74 | 0.71 | 0.72 |
| RoBERTa-base (run 2) | Sarcasm | en-UK | 0.75 | 0.73 | 0.74 |

---

### Q2.2 – Cross-Variety Evaluation Matrix (RoBERTa-base, Sentiment)

*Rows = trained on, Columns = tested on*

| Train → Test | en-AU | en-IN | en-UK |
|---|---|---|---|
| en-AU | **0.83** | 0.61 | 0.72 |
| en-IN | 0.58 | **0.79** | 0.60 |
| en-UK | 0.70 | 0.57 | **0.84** |

---

### Q2.3 – LoRA Adapter Comparison (Sarcasm, 1B–3B LLM base)

| Adapter | Base Model | Tested on en-AU | Tested on en-IN | Tested on en-UK |
|---|---|---|---|---|
| UK Adapter (run 1) | Qwen2.5-1.5B | 0.68 | 0.55 | **0.78** |
| UK Adapter (run 2) | Qwen2.5-1.5B | 0.67 | 0.54 | **0.77** |
| IN Adapter (run 1) | Qwen2.5-1.5B | 0.59 | **0.76** | 0.61 |
| IN Adapter (run 2) | Qwen2.5-1.5B | 0.60 | **0.75** | 0.62 |
| AU Adapter (run 1) | Qwen2.5-1.5B | **0.80** | 0.58 | 0.66 |
| AU Adapter (run 2) | Qwen2.5-1.5B | **0.79** | 0.57 | 0.65 |

---

### Q3 – Per-Class Results, Best Models (Sarcasm)

| Model | Class | Precision | Recall | F1 | Macro-F1 |
|---|---|---|---|---|---|
| RoBERTa-base (en-UK) | Sarcastic | 0.71 | 0.68 | 0.69 | 0.74 |
| RoBERTa-base (en-UK) | Not Sarcastic | 0.79 | 0.81 | 0.80 | 0.74 |
| Qwen2.5-1.5B + AU LoRA Adapter | Sarcastic | 0.77 | 0.74 | 0.75 | 0.80 |
| Qwen2.5-1.5B + AU LoRA Adapter | Not Sarcastic | 0.84 | 0.86 | 0.85 | 0.80 |

---

### Q4 – Few-Shot Prompting Error Analysis (6 test examples)

| Example | True Label | Before Few-Shot | After Few-Shot | Improved? |
|---|---|---|---|---|
| "Coz we all have free internet." | Sarcastic | Not Sarcastic | Sarcastic | ✅ Yes |
| "Absolute legend, cheers mate." | Sarcastic | Not Sarcastic | Sarcastic | ✅ Yes |
| "Yeh bilkul sahi hai bhai." | Not Sarcastic | Sarcastic | Not Sarcastic | ✅ Yes |
| "Great service, waited only 2 hours." | Sarcastic | Not Sarcastic | Not Sarcastic | ❌ No |
| "The food was really something else." | Sarcastic | Sarcastic | Sarcastic | ✅ Already correct |
| "Loved the ambience, truly." | Not Sarcastic | Not Sarcastic | Not Sarcastic | ✅ Already correct |

---

### Q5.2 – Inference Time (Efficiency)

| Model | Input Size | Avg. Inference Time (ms) |
|---|---|---|
| TF-IDF + SVM | Single sentence | 2 ms |
| TF-IDF + SVM | Batch (100 samples) | 18 ms |
| RoBERTa-base | Single sentence | 38 ms |
| RoBERTa-base | Batch (100 samples) | 310 ms |
| Qwen2.5-1.5B + LoRA Adapter | Single sentence | 95 ms |
| Qwen2.5-1.5B + LoRA Adapter | Batch (100 samples) | 740 ms |