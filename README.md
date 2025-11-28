# Resume Information Extraction using LoRA Fine-Tuned Llama 3B

This repository contains an end-to-end pipeline for training a lightweight resume information extractor using a LoRA-fine-tuned **meta-llama/Llama-3.2-3B-Instruct** model.  
The system converts raw, unstructured resume text into structured JSON fields such as:
 
- education  
- work experience  

Built for efficiency, accuracy, and easy reproducibility.

---

## 🚀 Features

- Parameter-efficient fine-tuning with **LoRA**
- Works on low-cost/free Colab GPUs  
- Handles messy and inconsistent resume formats  
- Produces clean, schema-consistent JSON  
- Training + inference notebooks included  
- Small sample dataset for demonstration  

---

## 📂 Project Structure

```
resume-extractor-lora/
│
├── notebooks/
│   ├── llama_test.ipynb          # LoRA fine-tuning notebook
│   ├── llama_training.ipynb      # Load adapter + test extraction
│
├── datasets/
│   └── dataset.jsonl # 3–5 sample entries for demo
│
│
├── scripts/
│   └── data_preprocess.py   # CSV → JSONL converter
│
├── requirements.txt
└── README.md
```

---

## 🧠 Training

The model was fine-tuned on a JSONL dataset using LoRA with:

-	EPOCHS = 3
-	PER_DEVICE_BATCH_SIZE = 1
-	GRADIENT_ACCUMULATION_STEPS = 8
-	LEARNING_RATE = 2e-4
-	MAX_LENGTH = 1024
-	LOGGING_STEPS = 50
-	SAVE_STEPS = 200


Checkpoints were saved in drive under:

```
/checkpoints-165/
```

Training logs and charts are available in `llama_training.ipynb`.

---

## 🧪 Inference

The Testing notebook loads:

- Base model: **meta-llama/Llama-3.2-3B-Instruct**
- Fine-tuned LoRA adapter from `checkpoints-165`

It demonstrates extraction on:

1. 5 random samples from the dataset  
2. A real-world unseen resume from the internet  

Example output is structured JSON following a fixed schema.

---


## 📦 Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

Run the notebooks in Google Colab or locally with GPU.

---



## 🌟 Project Summary

A clean, efficient, and reproducible pipeline for training a resume-to-JSON extractor using LoRA + Llama-3B. Ideal for ML assignments, research prototypes, and LLM fine-tuning demonstrations.
