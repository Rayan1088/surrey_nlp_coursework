
File structure for NLP Sequence Classification Project
```
nlp-sequence-classification/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md                 # Dataset description + link (NO actual data)
│   └── sample/                   # Optional small samples only
│
├── notebooks/
│   ├── main.ipynb               # REQUIRED entry notebook (as per coursework)
│   ├── 01_data_analysis.ipynb
│   ├── 02_baseline_models.ipynb
│   ├── 03_transformer_models.ipynb
│   ├── 04_cross_variety.ipynb
│   ├── 05_llm_experiments.ipynb
│   └── 06_evaluation.ipynb
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   ├── loader.py             # Load dataset from HuggingFace
│   │   ├── preprocessing.py
│   │   └── utils.py
│   │
│   ├── features/
│   │   ├── tfidf.py
│   │   └── embeddings.py
│   │
│   ├── models/
│   │   ├── baseline.py           # Logistic Regression / SVM
│   │   ├── transformer.py        # BERT / RoBERTa
│   │   ├── llm_adapter.py        # LoRA / lightweight LLM
│   │   └── utils.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py            # F1, Precision, Recall
│   │   ├── confusion_matrix.py
│   │   └── error_analysis.py
│   │
│   └── config/
│       └── config.yaml           # Hyperparameters
│
├── experiments/
│   ├── logs/                     # Training logs
│   ├── results/
│   │   ├── baseline/
│   │   ├── transformer/
│   │   └── cross_variety/
│   │
│   └── figures/                  # Plots for report
│
├── deployment/
│   ├── app.py                    # Main app (Gradio/Streamlit/Flask)
│   ├── model_loader.py           # Load correct model based on variety
│   └── utils.py
│
├── scripts/
│   ├── train_baseline.py
│   ├── train_transformer.py
│   ├── evaluate.py
│   └── run_inference.py
│
├── reports/
│   ├── report.pdf                # Final submission (separate upload required)
│   └── figures/
│
└── docs/
    └── project_plan.md           # Group declaration / notes
```