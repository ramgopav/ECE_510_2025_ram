import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock

@cocotb.test()
async def spi_benchmark(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    PACKET_SIZES = [1, 8, 16, 32, 64, 128, 256, 512, 1024]
    spi_clock_ns = 10
    sclk_half = spi_clock_ns // 2

    results = []

    for packet_size in PACKET_SIZES:
        num_bits = packet_size * 8
        data_pattern = [0xA5 for _ in range(packet_size)]

        dut.cs.value = 1
        dut.sclk.value = 0
        dut.mosi.value = 0
        await Timer(100, units="ns")

        dut.cs.value = 0
        sim_time_start = cocotb.utils.get_sim_time(units="ns")

        for byte in data_pattern:
            for i in range(8):
                bit_val = (byte >> (7 - i)) & 1
                dut.mosi.value = bit_val
                await Timer(sclk_half, units="ns")
                dut.sclk.value = 1
                await Timer(sclk_half, units="ns")
                dut.sclk.value = 0

        dut.cs.value = 1
        await Timer(50, units="ns")

        sim_time_end = cocotb.utils.get_sim_time(units="ns")
        elapsed_ns = sim_time_end - sim_time_start
        elapsed_s = elapsed_ns / 1e9
        throughput_kbps = (packet_size * 8) / elapsed_s / 1000
        latency_us = elapsed_ns / 1000
        ideal_time = num_bits * spi_clock_ns
        efficiency = (ideal_time / elapsed_ns) * 100

        results.append((packet_size, throughput_kbps, efficiency))

    spi_clk_freq = 1e9 / spi_clock_ns
    overhead_ns = elapsed_ns - (PACKET_SIZES[-1] * 8 * spi_clock_ns)
    overhead_us = overhead_ns / 1000

    print("\nSPI BENCHMARK SUMMARY (Simulation Time Based)")
    print("============================================================")
    print(f"Average Latency:     {latency_us:.2f} µs")
    print(f"Maximum Throughput:  {max(r[1] for r in results):.2f} kbps")
    print(f"SPI Clock Frequency: {spi_clk_freq/1e6:.2f} MHz")
    print(f"Protocol Overhead:   {overhead_us:.2f} µs")
    print("============================================================")
    print("Performance by Packet Size:")
    print(f"{'Size (bytes)':<15} {'Throughput (kbps)':<22} {'Efficiency (%)'}")
    print("-" * 60)

    for size, tput, eff in results:
        print(f"{size:<15} {tput:<22.2f} {eff:.2f}")
