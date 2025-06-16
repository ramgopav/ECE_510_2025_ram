module uart_tx #(parameter CLK_HZ=50_000_000, BAUD=115200) (
    input  logic clk,
    input  logic [7:0] data,
    input  logic       valid,
    output logic       tx,
    output logic       busy
);
    localparam DIV = CLK_HZ / BAUD;
    logic [$clog2(DIV)-1:0] cnt; logic [3:0] bitp; logic [9:0] sh;
    always_ff @(posedge clk) begin
        if (!busy && valid) begin sh<={1'b1,data,1'b0}; cnt<=DIV-1; bitp<=0; busy<=1; end
        else if (busy && !cnt--) begin cnt<=DIV-1; bitp++; if(bitp==9) busy<=0; end
        if (busy) sh <= {1'b1, sh[9:1]};
    end
    assign tx = busy ? sh[0] : 1'b1;
endmodule
