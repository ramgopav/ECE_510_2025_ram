module spi_slave (
    input  wire clk,
    input  wire sclk,
    input  wire mosi,
    input  wire cs,
    output wire miso,
    output reg  [7:0] data_out
);

    reg [7:0] shift_reg;
    reg [2:0] bit_cnt = 0;

    assign miso = shift_reg[7];

    always @(posedge sclk or posedge cs) begin
        if (cs) begin
            bit_cnt <= 0;
        end else begin
            shift_reg <= {shift_reg[6:0], mosi};
            bit_cnt <= bit_cnt + 1;
            if (bit_cnt == 7)
                data_out <= {shift_reg[6:0], mosi};
        end
    end
endmodule
