// Code your testbench here
// or browse Examples
`timescale 1ns/1ps

module conv2d_tb;

    logic clk = 0;
    logic rst = 0;
    logic start = 0;
    logic [7:0] in_data;
    logic [7:0] kernel [0:8];
    logic [15:0] out_data;
    logic done;

    // DUT
    conv2d uut (
        .clk(clk),
        .rst(rst),
        .start(start),
        .in_data(in_data),
        .kernel(kernel),
        .out_data(out_data),
        .done(done)
    );

    // 100 MHz clock
    always #5 clk = ~clk;

    initial begin
        $display("🚀 Starting conv2d testbench");
        rst = 1;
        #20 rst = 0;

        // Fill 3x3 kernel with 1s
        for (int i = 0; i < 9; i++) kernel[i] = 8'd1;

        // Feed 5x5 image: values 1 to 25
        start = 1;
        for (int i = 0; i < 25; i++) begin
            in_data = i + 1;
            #10;
        end
        start = 0;

        // Wait for result (with timeout)
        repeat (50) begin
            #10;
            if (done) begin
                $display("✅ Convolution Output: %0d", out_data);
                $finish;
            end
        end

        $display("❌ ERROR: Timeout, 'done' not triggered.");
        $finish;
    end

endmodule
