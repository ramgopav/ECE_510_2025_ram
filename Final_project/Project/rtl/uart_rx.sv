module uart_rx #(parameter CLK_HZ=50_000_000, BAUD=115200) (
    input  logic clk, rx,
    output logic [7:0] data,
    output logic       valid
);
    localparam DIV = CLK_HZ / BAUD;
    logic [$clog2(DIV)-1:0] cnt; logic [3:0] bitp; logic [7:0] sh; enum {IDLE,SRT,DATA,STP} st;
    always_ff @(posedge clk) begin
        valid <= 0;
        case (st)
        IDLE: if (!rx) begin cnt<=DIV/2; st<=SRT; end
        SRT : if (!cnt--) begin cnt<=DIV-1; bitp<=0; st<=DATA; end
        DATA: if (!cnt--) begin cnt<=DIV-1; sh<= {rx,sh[7:1]};
                       if (bitp==7) st<=STP; else bitp++; end
        STP : if (!cnt--) begin data<=sh; valid<=1; st<=IDLE; end
        endcase
    end
endmodule
