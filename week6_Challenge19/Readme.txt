Binary LIF Neuron – Code Design and Simulation (Step-by-Step Explanation)

1. What This Project Does
   The goal is to design a Binary Leaky Integrate-and-Fire (LIF) neuron in Verilog, and simulate how it behaves over time with different inputs. We want to see when (or if) the neuron "fires" (spikes) based on how its internal value (potential) grows.

2. Understanding the Neuron Design
   Every clock cycle, the neuron:

* Stores a value called potential
* Multiplies this value by a leak factor lambda (λ), making it decay slowly over time
* Adds a new binary input (0 or 1)
* If the potential crosses a threshold, it spikes (sets spike = 1)
* If it spikes, the potential resets to zero

3. Writing the Verilog Code
   The main Verilog module uses fixed-point math to implement the decay:

* lambda is set to 250 (in Q8.8 fixed-point, representing 0.98)
* To multiply fixed-point correctly, the potential is scaled before multiplication and scaled down after

Example core logic:

```
mult_result = (potential << 8) * lambda;
next_potential = (mult_result >> 16) + binary_input;
```

If next\_potential >= threshold, spike is set to 1, and potential is reset to 0.

4. Writing the Testbench
   The testbench:

* Generates a clock
* Applies reset at the beginning
* Sends a constant input of binary\_input = 1 for many cycles
* Observes the output (potential and spike)

Example testbench snippet:

```
repeat (100) begin
    @(posedge clk);
    binary_input = 1;
end
```

5. How to Simulate It
   You can run this in EDA Playground or any Verilog simulator (like ModelSim):

* Paste both the module and testbench
* Add:

```
$dumpfile("dump.vcd");
$dumpvars(0, binary_lif_neuron_tb);
```

* Run the simulation and open EPWave to view waveforms

6. What Happened in My Case
   In my simulation:

* I used lambda = 250 (≈0.98) and threshold = 100
* The potential increased slowly but never reached 100
* Therefore, spike stayed 0 throughout

7. Why This Is Correct Behavior
   According to the formula:

```
P_inf = input / (1 - lambda)
```

With input = 1 and lambda = 0.98, the potential will converge to 50 over time.
So if the threshold is set to 100, it will never be reached. This is not a bug—it's expected.

8. Conclusion

* The neuron was designed and implemented correctly
* The simulation was set up properly
* The parameters chosen caused the neuron to never spike
* This confirms the theoretical model of the Binary LIF neuron
