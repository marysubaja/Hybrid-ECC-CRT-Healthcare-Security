import numpy as np
import matplotlib.pyplot as plt

# Bit size values
bit_size = [80, 112, 128, 192, 256]

# Sample values from graph
rsa = [1024, 2048, 3072, 7680, 15360]
ecc = [160, 224, 256, 384, 521]
ecc_crt = [128, 160, 192, 224, 256]
security_ratio = [8, 10, 12, 15, 18]

# Bar positions
x = np.arange(len(bit_size))
width = 0.2

plt.figure(figsize=(10,6))

plt.bar(
    x - 1.5*width,
    rsa,
    width,
    label='RSA'
)

plt.bar(
    x - 0.5*width,
    ecc,
    width,
    label='ECC'
)

plt.bar(
    x + 0.5*width,
    ecc_crt,
    width,
    label='ECC-CRT Improved scalar arithmetic (Invalid-Curve Defense)'
)

plt.bar(
    x + 1.5*width,
    security_ratio,
    width,
    label='Security Ratio'
)

plt.xticks(x, bit_size)

plt.xlabel(
    'Bit Size',
    fontsize=12
)

plt.ylabel(
    'Key Length',
    fontsize=12
)

plt.title(
    'Analysis of Public Key Algorithms',
    fontsize=16
)

plt.grid(
    axis='y',
    linestyle='--',
    alpha=0.6
)

plt.legend()
plt.tight_layout()

plt.savefig(
    "Analysis_Public_Key_Algorithms.png",
    dpi=300
)

plt.show()
