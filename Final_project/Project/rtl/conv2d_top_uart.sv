module conv2d_top_uart (
    input  logic clk, rst_n,
    input  logic rx,
    output logic tx
);
    logic [7:0] px_in;  logic vin;
    uart_rx RX(.clk(clk), .rx(rx), .data(px_in), .valid(vin));

    logic [7:0] px_out; logic vout;
    conv2d_sliding core (.*);                // your existing multi-filter core

    uart_tx TX(.clk(clk), .data(px_out), .valid(vout), .tx(tx));
endmodule
