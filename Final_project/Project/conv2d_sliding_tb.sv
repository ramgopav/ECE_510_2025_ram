// Code your testbench here
// or browse Examples
`timescale 1ns/1ps

module conv2d_sliding_tb;

    logic clk = 0;
    logic rst = 0;
    logic start = 0;
    logic [7:0] in_data;
    logic [7:0] kernel [0:8];
    logic [15:0] out_data;
    logic done;

    // Instantiate the design
    conv2d_sliding uut (
        .clk(clk),
        .rst(rst),
        .start(start),
        .in_data(in_data),
        .kernel(kernel),
        .out_data(out_data),
        .done(done)
    );

    // Clock: 100 MHz
    always #5 clk = ~clk;

    // Stimulus
    initial begin
        $display("🚀 Starting sliding conv2d testbench");
        rst = 1;
        #20 rst = 0;

        // Initialize kernel (all 1s)
        for (int i = 0; i < 9; i++) kernel[i] = 8'd1;

        // Feed 5×5 image: values 1 to 25
        start = 1;
        for (int i = 0; i < 25; i++) begin
            in_data = i + 1;
            #10;
        end
        start = 0;
      
      // Wait 1 cycle after compute starts
			@(posedge clk);

        // Print each output pixel
        $display("🧾 Sliding window output values:");
        repeat (9) begin
            @(posedge clk);
            $display("→ Output: %0d", out_data);
        end

        // Confirm final 'done'
        @(posedge clk);
        if (done)
            $display("✅ All outputs generated. Done.");
        else
            $display("❌ ERROR: Done flag not set.");

        $finish;
    end

endmodule
