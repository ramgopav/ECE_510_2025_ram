//======================================================================
//  rtl_main.v   –  ONE–MODULE RTL  (no sub-instances)
//
//  • clk       : system clock  (param CLK_HZ)
//  • rst_n     : async, active-low reset
//  • uart_rx_i : serial in   (115 200-8-N-1)
//  • uart_tx_o : serial out
//
//  Host ?   784 bytes (28×28 glyph)
//  FPGA ?   676 bytes (26×26 conv feature map, LSB each)
//
//  !!  Place   weights.mem   in the same directory.
//======================================================================
`timescale 1ns/1ps
module plate_cnn_fpga #(
    parameter integer CLK_HZ = 12_000_000,
    parameter integer BAUD   = 115_200
)(
    input  wire clk,
    input  wire rst_n,
    input  wire uart_rx_i,
    output wire uart_tx_o
);

    // ---------------------------------------------------------------
    //  UART constants
    // ---------------------------------------------------------------
    localparam integer UART_DIV    = CLK_HZ / BAUD;      // clocks / bit
    localparam integer UART_DIV_W  = $clog2(UART_DIV);

    // ---------------------------------------------------------------
    //  --- Tiny UART-RX (no sub-module) ---
    // ---------------------------------------------------------------
    reg  [UART_DIV_W-1:0] rx_cnt   = 0;
    reg  [3:0]            rx_bitp  = 0;
    reg  [7:0]            rx_shift = 0;
    reg                   rx_valid = 0;
    reg                   rx_busy  = 0;
	wire tx_done_all;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_busy  <= 1'b0;
            rx_valid <= 1'b0;
        end else begin
            rx_valid <= 1'b0;
            if (!rx_busy) begin
                if (!uart_rx_i) begin                 // start bit detect
                    rx_busy <= 1'b1;
                    rx_cnt  <= UART_DIV + (UART_DIV>>1);  // half-bit
                    rx_bitp <= 4'd0;
                end
            end
            else if (rx_cnt == 0) begin               // sample
                rx_cnt   <= UART_DIV-1;
                rx_shift <= {uart_rx_i, rx_shift[7:1]};
                if (rx_bitp == 4'd7) begin
                    rx_busy  <= 1'b0;
                    rx_valid <= 1'b1;
                end
                else
                    rx_bitp <= rx_bitp + 1'b1;
            end
            else
                rx_cnt <= rx_cnt - 1'b1;
        end
    end
    wire [7:0] rx_byte = rx_shift;

    // ---------------------------------------------------------------
    //  Weight ROM (32 × 9)   –  synthesises into flop-array
    // ---------------------------------------------------------------
    reg [7:0] wmem [0:31][0:8];
    initial $readmemh("weights.mem", wmem);

    // Use filter-0 for demo
    wire [7:0] k0 = wmem[0][0], k1 = wmem[0][1], k2 = wmem[0][2],
               k3 = wmem[0][3], k4 = wmem[0][4], k5 = wmem[0][5],
               k6 = wmem[0][6], k7 = wmem[0][7], k8 = wmem[0][8];

    // ---------------------------------------------------------------
    //  Store entire 28×28 glyph (simple but large)
    // ---------------------------------------------------------------
    reg [7:0] img [0:27][0:27];
    reg [9:0] rx_cnt_bytes = 0;
    reg       img_full     = 0;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_cnt_bytes <= 10'd0;
            img_full     <= 1'b0;
        end else if (rx_valid) begin
            img[rx_cnt_bytes/28][rx_cnt_bytes%28] <= rx_byte;
            rx_cnt_bytes <= rx_cnt_bytes + 1'b1;
            if (rx_cnt_bytes == 10'd783)
                img_full <= 1'b1;
        end else if (tx_done_all) begin
            rx_cnt_bytes <= 10'd0;
            img_full     <= 1'b0;
        end
    end

    // ---------------------------------------------------------------
    //  Convolution 3×3  ? 26×26
    // ---------------------------------------------------------------
    reg [15:0] feat [0:25][0:25];
    reg [5:0]  row = 0, col = 0;
    reg        calc = 0, calc_done = 0;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            row<=0; col<=0; calc<=0; calc_done<=0;
        end
        else if (img_full && !calc && !calc_done) begin
            calc <= 1'b1;
            row  <= 6'd0;
            col  <= 6'd0;
        end
        else if (calc) begin
            integer s;
            s = +$signed({1'b0,img[row  ][col  ]}) * $signed(k0)
              + $signed({1'b0,img[row  ][col+1]}) * $signed(k1)
              + $signed({1'b0,img[row  ][col+2]}) * $signed(k2)
              + $signed({1'b0,img[row+1][col  ]}) * $signed(k3)
              + $signed({1'b0,img[row+1][col+1]}) * $signed(k4)
              + $signed({1'b0,img[row+1][col+2]}) * $signed(k5)
              + $signed({1'b0,img[row+2][col  ]}) * $signed(k6)
              + $signed({1'b0,img[row+2][col+1]}) * $signed(k7)
              + $signed({1'b0,img[row+2][col+2]}) * $signed(k8);
            feat[row][col] <= s[15:0];

            if (col == 6'd25) begin
                col <= 6'd0;
                if (row == 6'd25) begin
                    calc      <= 1'b0;
                    calc_done <= 1'b1;
                end
                else
                    row <= row + 1'b1;
            end
            else
                col <= col + 1'b1;
        end
        else if (tx_done_all)
            calc_done <= 1'b0;
    end

    // ---------------------------------------------------------------
    //  In-lined UART-TX  (LSB of feat[row][col])
    // ---------------------------------------------------------------
    reg [UART_DIV_W-1:0] tx_cnt  = 0;
    reg [3:0]            tx_bitp = 0;
    reg [9:0]            tx_sh   = 10'b1111111111; // idle high
    reg                  tx_busy = 0;

    reg [5:0] tx_r = 0, tx_c = 0;
    wire      have_lsb = calc_done && !tx_busy;
    wire [7:0] tx_payload = feat[tx_r][tx_c][7:0];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx_busy <= 1'b0;
            tx_sh   <= 10'h3FF;
            tx_cnt  <= 0;
            tx_bitp <= 0;
            tx_r    <= 0;
            tx_c    <= 0;
        end
        else begin
            // --- load new byte when ready ---
            if (have_lsb) begin
                tx_sh   <= {1'b1, tx_payload, 1'b0}; // stop | data | start
                tx_busy <= 1'b1;
                tx_cnt  <= UART_DIV-1;
                tx_bitp <= 0;
            end
            // --- shift out if busy ---
            else if (tx_busy) begin
                if (tx_cnt == 0) begin
                    tx_sh   <= {1'b1, tx_sh[9:1]};
                    tx_cnt  <= UART_DIV-1;
                    tx_bitp <= tx_bitp + 1'b1;
                    if (tx_bitp == 4'd9)
                        tx_busy <= 1'b0;
                end
                else
                    tx_cnt <= tx_cnt - 1'b1;
            end

            // --- advance pixel pointers after byte accepted ---
            if (have_lsb) begin
                if (tx_c == 6'd25) begin
                    tx_c <= 6'd0;
                    if (tx_r == 6'd25)
                        tx_r <= 6'd0;
                    else
                        tx_r <= tx_r + 1'b1;
                end
                else
                    tx_c <= tx_c + 1'b1;
            end
        end
    end

    assign uart_tx_o  = tx_busy ? tx_sh[0] : 1'b1;  // idle high
    assign tx_done_all = (tx_r==6'd25) && (tx_c==6'd25) && have_lsb;

endmodule

