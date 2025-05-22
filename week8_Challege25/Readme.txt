# SPI Benchmark Challenge 🧪

This project simulates and benchmarks an SPI interface using:
- ✅ Verilog (SPI Slave)
- 🐍 Python Cocotb (SPI Master + Testbench)
- 📊 Performance metrics like latency, throughput, and efficiency

---

## 📁 Files in This Project

- `spi_slave.v` — Verilog SPI slave module
- `test_spi_benchmark.py` — Cocotb Python testbench that sends SPI data and benchmarks it
- `Makefile` — Used to run the simulation with Cocotb

---

## 🚀 How to Run

1. ✅ Make sure you have:
   - Python (3.8+)
   - Cocotb installed (`pip install cocotb`)
   - Icarus Verilog (`sudo apt install iverilog`)
   - Make utility (`sudo apt install make`)
   - GTKWave (optional, for waveforms)

2. 📦 Extract the zip file:
unzip spi_benchmark_project.zip
cd spi_benchmark

3. ▶️ Run the test: make

4. 🧾 You will see a **SPI BENCHMARK SUMMARY** printed like: can see the picture "output" 


---

## 📊 What I Learn from this

✅ **How SPI works** — You simulate bit-by-bit transfer using SCLK, MOSI, CS, and get the response on MISO.

✅ **How to drive hardware (Verilog) from software (Python)** — using Cocotb testbench to simulate SPI master.

✅ **How to measure real SPI performance** — by calculating:
- **Latency** — how long a transfer takes
- **Throughput** — how fast data moves
- **Efficiency** — how close you are to the ideal SPI clock speed

✅ **How simulation timing works** — you compare simulation time (ideal) vs real-world time (slow).

---

## 📌 Notes

- This benchmark uses simulated time for accuracy.
- You can edit the SPI clock speed by changing `spi_clock_ns` in the Python script.
- Efficiency improves as packet size increases (due to less overhead).

---

## ✅ Next Steps

- Add MISO handling for full-duplex SPI
- Dump waveforms using VCD and view with GTKWave
- Test different SPI clock rates and packet patterns

---

