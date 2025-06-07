# ⬇︎ RUN THIS AS A NEW PYTHON CELL ⬇︎
import re, matplotlib.pyplot as plt

sizes, gbps = [], []
for line in open("timings.txt"):
    m = re.search(r"N=(\d+).*?kernel=([0-9.]+)", line)
    if not m:
        continue
    N  = int(m.group(1))
    ms = float(m.group(2))
    if N == 32768:           # skip the very first (warm-up) launch
        continue
    bytes_moved = 3 * 4 * N   # 1 read of x, 1 read + 1 write of y  (float32 → 4 B)
    gbps.append(bytes_moved / (ms / 1e3) / 1e9)   # GB / s
    sizes.append(N)

labels = [f"2^{n.bit_length()-1}" for n in sizes]
plt.bar(labels, gbps)
plt.ylabel("Effective GB/s")
plt.xlabel("Problem size (elements)")
plt.title("SAXPY kernel – effective memory bandwidth (Tesla K80)")
plt.tight_layout()
plt.savefig("plot_bandwidth.png", dpi=200)
plt.show()

print(f"Average bandwidth across sizes: {sum(gbps)/len(gbps):.2f} GB/s")
