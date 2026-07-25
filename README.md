# APT Stage Detection with Random Forest

Multi-class classification of Advanced Persistent Threat (APT) stages on the [DAPT 2020](https://www.kaggle.com/datasets/sowmyamyneni/dapt2020) network-flow benchmark using a Random Forest classifier.

## Pipeline

1. **Preprocess** multi-day public/private flow CSVs (`code/prepro_dapt.py`)
2. **Label** flows by APT stage
3. **Train / evaluate** a Random Forest model (`code/randomforest.py`)

## APT stage labels

| Stage | Label |
|---|---|
| Benign / BENIGN | 0 |
| Reconnaissance | 1 |
| Establish Foothold | 2 |
| Lateral Movement | 3 |
| Data Exfiltration | 4 |

## Project structure

```
apt-stage-detection/
├── code/
│   ├── prepro_dapt.py      # load, clean, encode, export dapt_data.csv
│   ├── randomforest.py     # train RF, CV, metrics, plots
│   └── requirements.txt
├── document/
│   └── stage-detection.pdf
└── README.md
```

## Dataset

Download DAPT 2020 from Kaggle:

[https://www.kaggle.com/datasets/sowmyamyneni/dapt2020](https://www.kaggle.com/datasets/sowmyamyneni/dapt2020)

Place the flow CSV files where `prepro_dapt.py` can read them. The script currently expects these paths (edit the paths in the script if your layout differs):

```
/csv/enp0s3-monday.pcap_Flow.csv
/csv/enp0s3-monday-pvt.pcap_Flow.csv
/csv/enp0s3-public-tuesday.pcap_Flow.csv
/csv/enp0s3-pvt-tuesday.pcap_Flow.csv
/csv/enp0s3-public-wednesday.pcap_Flow.csv
/csv/enp0s3-pvt-wednesday.pcap_Flow.csv
/csv/enp0s3-public-thursday.pcap_Flow.csv
/csv/enp0s3-pvt-thursday.pcap_Flow.csv
/csv/enp0s3-tcpdump-friday.pcap_Flow.csv
/csv/enp0s3-tcpdump-pvt-friday.pcap_Flow.csv
```

## Setup

```bash
cd code
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Preprocess

```bash
cd code
python prepro_dapt.py
```

This script:

- Loads Monday–Friday public and private flow CSVs and concatenates them
- Fixes column names for the Thursday private capture
- Ordinal-encodes `Src IP`, `Dst IP`, and `Flow ID`
- Parses `Timestamp`
- Maps `Stage` to the multi-class `Label` above
- Replaces `Infinity` / `NaN` values
- Writes cleaned data to `dapt_data.csv` (in the current working directory)
- Plots the class distribution

### 2. Train and evaluate

```bash
cd code
python randomforest.py
```

Requires `dapt_data.csv` in the working directory (produced by the preprocessing step).

This script:

- Drops `Timestamp`, `Stage`, `Activity`, and `Label` from the feature set
- Normalizes features with `MinMaxScaler`
- Splits data 80/20 (`random_state=42`)
- Trains `RandomForestClassifier` with `max_depth=15`, `n_estimators=75`
- Runs 5-fold stratified cross-validation
- Reports accuracy, precision, recall, and F1-score
- Plots train/test/CV accuracy heatmaps and confusion matrices

## Dependencies

Pinned in `code/requirements.txt`, including:

- `pandas`, `numpy`
- `scikit-learn`
- `matplotlib`, `seaborn`
