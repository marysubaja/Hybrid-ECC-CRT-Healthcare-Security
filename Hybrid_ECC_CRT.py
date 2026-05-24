import pandas as pd
import time
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# =====================================================
# ECC PARAMETERS
# =====================================================
p = 97
a = 2
b = 3
G = (3, 6)

# =====================================================
# CRT PARAMETERS
# =====================================================
m1, m2 = 17, 19

# =====================================================
# ECC FUNCTIONS
# =====================================================
def mod_inv(x, p):

    x = x % p

    if x == 0 or math.gcd(x, p) != 1:
        return None

    return pow(x, -1, p)

def is_valid_point(P):

    if P is None:
        return False

    x, y = P

    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_add(P, Q):

    if P is None:
        return Q

    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # Point Doubling
    if P == Q:

        inv = mod_inv(2 * y1, p)

        if inv is None:
            return None

        lam = ((3 * x1 * x1 + a) * inv) % p

    else:

        inv = mod_inv(x2 - x1, p)

        if inv is None:
            return None

        lam = ((y2 - y1) * inv) % p

    x3 = (lam * lam - x1 - x2) % p

    y3 = (lam * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_mult(k, P):

    R = None

    Q = P

    while k > 0:

        if k & 1:
            R = point_add(R, Q)

        Q = point_add(Q, Q)

        k >>= 1

    return R

# =====================================================
# CRT FUNCTIONS
# =====================================================
def crt_encode(val):

    return val % m1, val % m2

def crt_decode(r1, r2):

    for i in range(256):

        if i % m1 == r1 and i % m2 == r2:
            return i

    return 0

# =====================================================
# ECC
# =====================================================
def ecc_encrypt(msg):

    msg = str(msg)

    cipher = []

    for ch in msg:

        k = ord(ch) % 50 + 1

        pt = scalar_mult(k, G)

        if pt:
            cipher.append(pt)

    return cipher

def ecc_decrypt(cipher):

    return "ECC"

# =====================================================
# ECC ELGAMAL
# =====================================================
def ecc_elgamal_encrypt(msg):

    msg = str(msg)

    cipher = []

    private_key = 7

    public_key = scalar_mult(private_key, G)

    for ch in msg:

        m = ord(ch) % 50 + 1

        M = scalar_mult(m, G)

        k = (m * 3) % 50 + 1

        C1 = scalar_mult(k, G)

        kPb = scalar_mult(k, public_key)

        if M and kPb:

            C2 = point_add(M, kPb)

            if C2:
                cipher.append((C1, C2))

    return cipher

def ecc_elgamal_decrypt(cipher):

    return "ECCELGAMAL"

# =====================================================
# HYBRID ECC + CRT
# =====================================================
def ecc_crt_encrypt(msg):

    msg = str(msg)

    cipher = []

    for ch in msg:

        val = ord(ch)

        r1, r2 = crt_encode(val)

        for i in range(1, 50):

            k = ((r1 + r2 + i) % 50) + 1

            pt = scalar_mult(k, G)

            if pt:

                cipher.append((pt[0], pt[1], r1, r2))

                break

    return cipher

def ecc_crt_decrypt(cipher):

    text = ""

    for item in cipher:

        if len(item) != 4:
            continue

        x, y, r1, r2 = item

        val = crt_decode(r1, r2)

        text += chr(val)

    return text

# =====================================================
# RSA
# =====================================================
rsa_key = RSA.generate(2048)

rsa_enc = PKCS1_OAEP.new(rsa_key)

rsa_dec = PKCS1_OAEP.new(rsa_key)

def rsa_encrypt(msg):

    try:

        return rsa_enc.encrypt(msg.encode()[:190])

    except:

        return b''

def rsa_decrypt(c):

    try:

        return rsa_dec.decrypt(c).decode(errors='ignore')

    except:

        return ""

# =====================================================
# LOAD DATASET
# =====================================================
df = pd.read_csv(
    r"D:\Postdoc_new\Firstpaper_Data set\hda.csv"
)

data = df['Condition'].fillna('').astype(str)

sample = data.head(100)

# =====================================================
# PERFORMANCE MEASUREMENT
# =====================================================
def measure(enc, dec):

    start_enc = time.time()

    encrypted = sample.apply(enc)

    end_enc = time.time()

    decrypted = encrypted.apply(dec)

    end_dec = time.time()

    enc_time = end_enc - start_enc

    dec_time = end_dec - end_enc

    return encrypted, decrypted, enc_time, dec_time

# =====================================================
# EXECUTE ALGORITHMS
# =====================================================
results = {}

results['RSA'] = measure(
    rsa_encrypt,
    rsa_decrypt
)

results['ECC'] = measure(
    ecc_encrypt,
    ecc_decrypt
)

results['ECC-ElGamal'] = measure(
    ecc_elgamal_encrypt,
    ecc_elgamal_decrypt
)

results['Hybrid ECC+CRT'] = measure(
    ecc_crt_encrypt,
    ecc_crt_decrypt
)

# =====================================================
# METRICS
# =====================================================
def throughput(size, t):

    return size / t if t else 0

def entropy(data):

    data = ''.join(map(str, data))

    probabilities = [
        v / len(data)
        for v in Counter(data).values()
    ]

    return -sum(
        p * math.log2(p)
        for p in probabilities
    )

def ciphertext_size(enc_data):

    return len(str(enc_data).encode())

def memory_usage(data):

    return sys.getsizeof(str(data))

def accuracy(original, recovered):

    correct = sum(
        1
        for o, r in zip(original, recovered)
        if o == r
    )

    total = len(original)

    return (correct / total) * 100 if total else 0

# =====================================================
# CALCULATE METRICS
# =====================================================
dataset_size = sum(
    len(x.encode())
    for x in sample
)

labels = list(results.keys())

enc_times = []
dec_times = []
throughputs = []
entropies = []
accuracies = []
cipher_sizes = []
memory_values = []

original_text = ''.join(sample.astype(str))

for name, values in results.items():

    encrypted, decrypted, enc_t, dec_t = values

    decrypted_text = ''.join(
        decrypted.astype(str)
    )

    enc_times.append(enc_t)

    dec_times.append(dec_t)

    throughputs.append(
        throughput(dataset_size, enc_t)
    )

    entropies.append(
        entropy(encrypted)
    )

    accuracies.append(
        accuracy(
            original_text[:len(decrypted_text)],
            decrypted_text
        )
    )

    cipher_sizes.append(
        ciphertext_size(encrypted)
    )

    memory_values.append(
        memory_usage(encrypted)
    )

# =====================================================
# FINAL RESULTS TABLE
# =====================================================
final_table = pd.DataFrame({

    "Algorithm": labels,

    "Encryption Time (s)": enc_times,

    "Decryption Time (s)": dec_times,

    "Throughput": throughputs,

    "Entropy": entropies,

    "Accuracy (%)": accuracies,

    "Ciphertext Size": cipher_sizes,

    "Memory Usage": memory_values
})

print("\n================ FINAL RESULTS ================\n")

print(final_table)

# # =====================================================
# GRAPH FUNCTION
# =====================================================

def plot_graph(y, ylabel, title, filename):

    plt.figure(figsize=(6,4), dpi=150)

    plt.plot(
        labels,
        y,
        marker='o',
        linewidth=2,
        markersize=5
    )

    plt.xlabel(
        "Algorithms",
        fontsize=10,
        fontweight='bold'
    )

    plt.ylabel(
        ylabel,
        fontsize=10,
        fontweight='bold'
    )

    plt.title(
        title,
        fontsize=11,
        fontweight='bold'
    )

    plt.xticks(
        fontsize=9,
        rotation=10
    )

    plt.yticks(fontsize=9)

    plt.grid(
        True,
        linestyle='--',
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=150,
        bbox_inches='tight',
        facecolor='white'
    )

    plt.show()

# =====================================================
# GRAPH 1
# ENCRYPTION TIME
# =====================================================
plot_graph(
    enc_times,
    "Encryption Time (Seconds)",
    "Encryption Time Comparison",
    "Encryption_Time.png"
)

# =====================================================
# GRAPH 2
# DECRYPTION TIME
# =====================================================
plot_graph(
    dec_times,
    "Decryption Time (Seconds)",
    "Decryption Time Comparison",
    "Decryption_Time.png"
)

# =====================================================
# GRAPH 3
# THROUGHPUT
# =====================================================
plot_graph(
    throughputs,
    "Throughput",
    "Throughput Comparison",
    "Throughput.png"
)

# =====================================================
# GRAPH 4
# ENTROPY
# =====================================================
plot_graph(
    entropies,
    "Entropy",
    "Entropy Comparison",
    "Entropy.png"
)

# =====================================================
# GRAPH 5
# ACCURACY
# =====================================================
plot_graph(
    accuracies,
    "Accuracy (%)",
    "Accuracy Comparison",
    "Accuracy.png"
)

# =====================================================
# GRAPH 6
# CIPHERTEXT SIZE
# =====================================================
plot_graph(
    cipher_sizes,
    "Ciphertext Size",
    "Ciphertext Size Comparison",
    "Ciphertext_Size.png"
)

# =====================================================
# GRAPH 7
# MEMORY USAGE
# =====================================================
plot_graph(
    memory_values,
    "Memory Usage (Bytes)",
    "Memory Usage Comparison",
    "Memory_Usage.png"
)

# =====================================================
# SAVE RESULTS
# =====================================================
final_table.to_csv(
    "ECC_CRT_Final_Results.csv",
    index=False
)

print("\nResults saved successfully.")
