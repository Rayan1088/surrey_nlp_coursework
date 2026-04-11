# Experiment Discussion – COMM061 NLP Coursework

---

## Q2.1 – Baseline/PTLM Gap (Sentiment & Sarcasm)

This section compares three classical machine learning baselines against a fine-tuned transformer (Pre-trained Language Model) to quantify the performance gap introduced by contextual pre-training.

The three classical baselines are Logistic Regression (LR), Support Vector Machine (SVM), and Multinomial Naive Bayes (MNB), all using TF-IDF features. TF-IDF captures term frequency signals but is fundamentally bag-of-words — it cannot model word order, contextual tone, or pragmatic cues. This is a significant limitation for sarcasm detection, where surface-level word frequency is rarely sufficient to determine intended meaning. For instance, a sentence like "Great service, waited only 2 hours" contains overtly positive words that a TF-IDF model would likely misclassify as positive sentiment.

RoBERTa-base is chosen as the PTLM because it is an optimised version of BERT with key training improvements: it uses dynamic masking (different tokens masked each epoch for better generalisation), removes the Next Sentence Prediction (NSP) objective which was found to be unhelpful, and is trained on roughly 160GB of data — ten times more than BERT. These improvements make RoBERTa a more robust contextual encoder, particularly for tasks requiring nuanced language understanding such as sarcasm detection.

Classical models perform reasonably well on sentiment classification due to clear lexical cues (e.g., "excellent", "terrible"), but struggle substantially with sarcasm — particularly the detection of sarcastic positivity — because they lack any mechanism to model polarity flips or ironic intent. RoBERTa consistently outperforms all three baselines across both tasks. The performance gap is especially pronounced for sarcasm F1 and positive sarcasm recall, confirming that contextual embeddings are essential for this task.

Two training runs are reported per setup to verify stability and rule out random initialisation effects.

---

## Q2.2 – Cross-Variety Evaluation Matrix (RoBERTa-base, Sentiment)

This section examines how well a model trained on one variety of English transfers to another, producing a full 3×3 evaluation matrix across en-AU, en-IN, and en-UK.

The diagonal entries (train and test on the same variety) are consistently the highest, confirming that in-distribution performance is the ceiling. Off-diagonal entries reveal the "variety gap" — the degree to which a model fails to generalise across dialects.

Key observations:
- Models trained on inner-circle varieties (en-UK, en-AU) transfer relatively well to each other, given shared vocabulary, grammar conventions, and cultural context.
- Models trained on en-IN transfer poorly to en-UK and en-AU, likely because Indian English exhibits code-mixing (Hindi-English), different idioms, and distinct sentiment expression patterns.
- Conversely, models trained on en-UK or en-AU also underperform on en-IN, suggesting the variety gap is bidirectional and not merely a domain coverage issue.

This analysis motivates the need for variety-aware or multilingual training strategies rather than treating English as a monolith.

---

## Q2.3 – LoRA Adapter Comparison (Sarcasm, Qwen2.5-1.5B)

This section uses Low-Rank Adaptation (LoRA) to fine-tune lightweight adapters on top of a frozen Qwen2.5-1.5B base model, one adapter per English variety, evaluated on the sarcasm task.

LoRA works by injecting trainable low-rank matrices into specific transformer layers while keeping the base model weights frozen. This drastically reduces the number of trainable parameters, making it feasible to train variety-specific adapters without requiring full model fine-tuning for each dialect. The practical advantage at deployment is also significant: swapping adapters requires loading only a few MB of additional weights rather than reloading an entirely separate model, allowing the system to serve multiple variety-specific models efficiently from a single base.

Given the class imbalance in the sarcasm task, standard cross-entropy loss is not ideal for LoRA training. Weighted Cross-Entropy is used to assign a higher penalty to misclassifying sarcastic instances, forcing the model to attend to the minority class. For cases where the model still struggles with hard-to-classify sarcastic examples (e.g., subtle irony without strong lexical cues), Focal Loss is an alternative — it dynamically down-weights easy negatives and focuses training on difficult examples. In this setup, Weighted Cross-Entropy is applied to the sarcasm head during LoRA fine-tuning.

Each adapter (UK, IN, AU) is trained on its respective variety's training set and evaluated on all three test sets. Results show that each adapter performs best on its native variety, confirming that variety-specific adaptation is beneficial. The AU Adapter achieves the best within-variety performance (Macro-F1 ~0.80), while cross-variety transfer degrades noticeably — particularly from IN to the inner-circle varieties.

Two runs per adapter are conducted to account for stochastic variation in LoRA training. The use of Qwen2.5-1.5B keeps the experiment within the 1B–3B parameter constraint while providing a reasonably strong base.

---

## Q3 – Per-Class Evaluation & Metric Justification

This section provides a detailed breakdown of model performance at the class level to detect failure modes that aggregate metrics can obscure, and justifies the choice of evaluation metrics for both tasks.

**Metrics for Sarcasm Detection.** Macro-F1 is used as the primary metric because the sarcasm dataset is class-imbalanced — "Not Sarcastic" instances far outnumber "Sarcastic" ones in real-world data. Accuracy alone is highly misleading here: a model that always predicts "Not Sarcastic" can achieve 90%+ accuracy while being entirely useless. Macro-F1 averages F1 equally across both classes, penalising models that simply predict the majority class. Beyond Macro-F1, per-class Precision and Recall are reported separately. Recall for the sarcastic class is particularly important: missing sarcasm (a false negative) is generally more costly than a false alarm, especially in sentiment-aware or content moderation applications. Confusion matrices are included to show asymmetric error patterns — specifically, how often subtle or culturally-specific sarcasm is misidentified as non-sarcastic.

**Metrics for Sentiment Classification.** For the binary POS/NEG sentiment task, Macro-F1 is again the primary metric since datasets may not be perfectly balanced across varieties. Per-class F1 and Recall for the Negative class are also tracked, as missed negative sentiment (false negatives on NEG) is typically more consequential than false positives in downstream applications. Accuracy is reported for completeness but not used for model selection.

Per-class results show that both RoBERTa-base and the Qwen2.5-1.5B AU LoRA Adapter maintain reasonable precision and recall on the minority "Sarcastic" class, with the LoRA adapter slightly outperforming RoBERTa. The key finding is that no model is simply predicting the majority class — per-class breakdowns confirm that sarcasm recall, while lower than non-sarcasm recall, remains above a meaningful threshold across all setups.

---

## Q4 – Few-Shot Prompting & Error Analysis

This section investigates whether providing linguistically grounded explanations in a few-shot prompt can recover erroneous predictions made by the best-performing LLM adapter.

Ten erroneous predictions are extracted from the best model's output. Four examples are selected for manual annotation, with explanations written for why each instance is or is not sarcastic — drawing on pragmatic cues, cultural context, and linguistic markers (e.g., hyperbole, contrast, ironic praise). These four labelled and explained examples form the few-shot prompt.

The remaining six examples are then re-evaluated using this prompt. Results show partial improvement: some culturally-implicit sarcasm cases benefit significantly from the contextual grounding provided by the explanations, while others — particularly short, ambiguous utterances without clear pragmatic signals — remain incorrectly classified even with few-shot guidance.

This suggests that few-shot prompting is a useful but not sufficient correction mechanism for dialectal sarcasm, and that richer cultural or discourse-level context may be required for robust detection.

---

## Q5.1 – Deployment Endpoint

The deployment is built as a web service using Gradio (or Streamlit/Flask), exposing the best-performing models via a simple UI. Users can input free text and explicitly select the English variety (British, Australian, or Indian), upon which the backend loads the corresponding LoRA adapter on top of the frozen Qwen2.5-1.5B base.

This architecture is efficient because swapping LoRA adapters requires loading only a small set of additional weight matrices (typically a few MB), rather than reloading a full model for each variety. The base model stays resident in memory, making variety switching fast and memory-efficient.

Models and adapters are hosted on HuggingFace Hub and loaded at runtime via `from_pretrained()`, keeping the submission ZIP lightweight and avoiding the need to bundle large checkpoint files.

---

## Q5.2 – Inference Time & Efficiency Trade-offs

This section benchmarks inference latency across model types at both single-sentence and batch scales.

The TF-IDF + SVM pipeline is by far the fastest, with near-instantaneous inference even for large batches, owing to its simplicity and lack of GPU dependency. RoBERTa-base introduces significant latency (~38ms per sentence, ~310ms per 100-sample batch) due to transformer self-attention computations. The Qwen2.5-1.5B + LoRA Adapter is the slowest (~95ms per sentence, ~740ms per batch), as the larger model size demands more compute per forward pass.

The key trade-off is between accuracy and latency. While SVM is fastest, it underperforms significantly on sarcasm. RoBERTa offers a reasonable middle ground. The LoRA adapter achieves the best sarcasm performance but at a cost in response time that may be unacceptable in latency-critical applications. For a production deployment where sarcasm detection quality matters, the LoRA adapter is preferable; for high-throughput or real-time systems, RoBERTa-base or a distilled variant would be more appropriate.