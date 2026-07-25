# APT Stage Detection with Random Forest

Identification of Advanced Persistent Threat (APT) attack stages using a Random Forest classifier on the DAPT 2020 benchmark dataset.

This repository contains the code and results of a research project that:
- Preprocesses the multi-day DAPT 2020 network traffic data
- Labels traffic according to APT stages (Reconnaissance, Establish Foothold, Lateral Movement, Data Exfiltration, Benign)
- Trains and tunes a Random Forest model
- Evaluates performance with accuracy (~99%), precision, recall, F1-score and confusion matrices
