# Hybrid ECC + CRT Healthcare Security Framework

## Overview
This project implements a Hybrid ECC + CRT cryptographic framework for healthcare data security. The framework compares the performance of RSA, ECC, ECC-ElGamal, and Hybrid ECC+CRT algorithms using healthcare datasets.

## Features

- RSA encryption and decryption
- ECC encryption and decryption
- ECC-ElGamal encryption
- Hybrid ECC + CRT encryption
- Performance evaluation metrics:
  - Encryption Time
  - Decryption Time
  - Throughput
  - Entropy
  - Accuracy
  - Ciphertext Size
  - Memory Usage

## Dataset
Dataset used:

hda.csv

The dataset contains healthcare information used for encryption performance analysis.

## Project Structure

Hybrid-ECC-CRT-Healthcare-Security/

├── Hybrid_ECC_CRT.py  
├── hda.csv  
├── requirements.txt  
├── README.md  

├── Results/  
│   ├── Encryption_Time.png  
│   ├── Decryption_Time.png  
│   ├── Throughput.png  
│   ├── Entropy.png  
│   ├── Accuracy.png  
│   ├── Ciphertext_Size.png  
│   ├── Memory_Usage.png  
│   └── ECC_CRT_Final_Results.csv  

## Installation

Install required packages:
pip install -r requirements.txt
## Run Project
python Hybrid_ECC_CRT.py
## Output
The system generates:
Performance comparison graphs
CSV result table
Encryption and decryption analysis
## Algorithms Compared
1. RSA
2. ECC
3. ECC-ElGamal
4. Hybrid ECC+CRT
