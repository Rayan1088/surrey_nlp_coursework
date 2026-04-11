# Experiment Discussion – COMM061 NLP Coursework

---

## Q2.1 – Baseline vs. Fine-tuned Transformer (Sentiment & Sarcasm)

This section compares classical machine learning approaches against a fine-tuned transformer model to understand the performance gap introduced by pre-training on large corpora.

The classical baseline uses TF-IDF vectorisation combined with either Logistic Regression or an SVM classifier. TF-IDF captures term frequency signals but is entirely bag-of-words and cannot model word order, context, or dialectal nuance. As a result, it struggles especially with sarcasm, where surface-level word frequency is often insufficient to determine the intended meaning.

RoBERTa-base, by contrast, is pre-trained on billions of tokens and has encoded deep contextual representations. When fine-tuned on the BESSTIE data, it consistently outperforms the classical baseline on both sentiment and sarcasm tasks. The gap is more pronounced for sarcasm (~0.20 Macro-F1 difference) than sentiment (~0.18), which is expected — sentiment carries stronger lexical signals, while sarcasm requires understanding pragmatic and contextual cues that only a contextualised model can capture.

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

LoRA works by injecting trainable low-rank matrices into specific transformer layers while keeping the base model weights frozen. This drastically reduces the number of trainable parameters, making it feasible to train variety-specific adapters without requiring full model fine-tuning for each dialect.

Each adapter (UK, IN, AU) is trained on its respective variety's training set and then evaluated on all three test sets. Results show that each adapter performs best on its native variety, confirming that variety-specific adaptation is beneficial. The AU Adapter achieves the best within-variety performance (Macro-F1 ~0.80), while cross-variety transfer degrades noticeably — particularly from IN to the inner-circle varieties.

Two runs per adapter are conducted to account for stochastic variation in LoRA training. The use of Qwen2.5-1.5B keeps the experiment within the 1B–3B parameter constraint while providing a reasonably strong base.

---

## Q3 – Per-Class Evaluation (Sarcasm)

This section provides a detailed breakdown of model performance at the class level to detect failure modes that aggregate metrics can obscure.

Macro-F1 is used as the primary metric because the sarcasm dataset is class-imbalanced — "Not Sarcastic" instances far outnumber "Sarcastic" ones in real-world data. A naive classifier that always predicts "Not Sarcastic" could achieve high accuracy but near-zero F1 on the sarcastic class; Macro-F1 penalises such behaviour by averaging equally across both classes.

Per-class results show that both RoBERTa-base and the Qwen2.5-1.5B AU LoRA Adapter maintain reasonable precision and recall on the minority "Sarcastic" class, with the LoRA adapter slightly outperforming RoBERTa. Confusion matrices for the best models are included to show specific patterns of misclassification, particularly cases where subtle or culturally-specific sarcasm is misidentified as non-sarcastic.

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