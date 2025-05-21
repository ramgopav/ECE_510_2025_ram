// Code your testbench here
// or browse Examples
// ===========================
// DESIGN: Binary LIF Neuron
// ===========================

module binary_lif_neuron (
    input wire clk,
    input wire rst,
    input wire binary_input,
    output reg spike,
    output reg [7:0] potential
);
    parameter lambda = 8'd250;       // ~0.98 leak factor (Q8)
    parameter threshold = 8'd15;     // Threshold for spiking
    parameter reset_val = 8'd0;      // Reset potential after spike

    reg [23:0] mult_result;
    reg [7:0] next_potential;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            potential <= 0;
            spike <= 0;
        end else begin
            mult_result = (potential << 8) * lambda;       // Scale potential to Q8.8, multiply by lambda
            next_potential = (mult_result >> 16) + binary_input; // Scale result back to 8-bit, add input

            if (next_potential >= threshold) begin
                spike <= 1;
                potential <= reset_val;
            end else begin
                spike <= 0;
                potential <= next_potential;
            end
        end
    end
endmodule


// ===========================
// TESTBENCH
// ===========================

`timescale 1ns/1ps
module binary_lif_neuron_tb;
    reg clk, rst;
    reg binary_input;
    wire spike;
    wire [7:0] potential;

    binary_lif_neuron #(
        .lambda(8'd250),
        .threshold(8'd20),
        .reset_val(8'd0)
    ) uut (
        .clk(clk),
        .rst(rst),
        .binary_input(binary_input),
        .spike(spike),
        .potential(potential)
    );

    // Clock generation
    initial clk = 0;
    always #5 clk = ~clk;  // 100MHz clock

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, binary_lif_neuron_tb);
        $display("Time\tInput\tPotential\tSpike");
        $monitor("%0t\t%b\t%d\t\t%b", $time, binary_input, potential, spike);

        rst = 1; binary_input = 0;
        #10 rst = 0;

        // === Scenario 1: Constant input below threshold ===
        $display("\n--- Scenario 1: Constant input = 0 (no spike expected) ---");
        repeat (10) begin
            @(posedge clk);
            binary_input = 0;
        end

        // === Scenario 2: Input accumulates until reaching threshold ===
        $display("\n--- Scenario 2: Accumulating input to spike ---");
        repeat (50) begin
            @(posedge clk);
            binary_input = 1;
        end

        // === Scenario 3: Leakage with no input ===
        $display("\n--- Scenario 3: Leakage after stopping input ---");
        repeat (10) begin
            @(posedge clk);
            binary_input = 0;
        end

        // === Scenario 4: Strong input causing immediate spike ===
        $display("\n--- Scenario 4: Short burst of inputs to trigger spike ---");
        repeat (5) begin
            @(posedge clk);
            binary_input = 1;
        end

        repeat (5) begin
            @(posedge clk);
            binary_input = 0;
        end

        $finish;
    end
endmodule
