`timescale 1ns/1ps

module conv2d_sliding (
    input  logic clk,
    input  logic rst,
    input  logic start,
    input  logic [7:0] in_data,
    input  logic [7:0] kernel [0:8],
    output logic [15:0] out_data,
    output logic done
);

    logic [7:0] input_buffer [0:24];  // 5x5 image
    logic [5:0] in_idx;
    logic [3:0] out_idx;
    logic load_done, compute;

    integer sum;
    integer row, col, i, j;
    integer index;

    // FSM and convolution logic
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            in_idx <= 0;
            out_idx <= 0;
            load_done <= 0;
            compute <= 0;
            done <= 0;
        end else if (start && !load_done) begin
            input_buffer[in_idx] <= in_data;
            in_idx <= in_idx + 1;
            if (in_idx == 24) begin
                load_done <= 1;
                compute <= 1;
                out_idx <= 0;
            end
        end else if (compute && out_idx < 9) begin
            row = out_idx / 3;
            col = out_idx % 3;
            sum = 0;

            for (i = 0; i < 3; i++) begin
                for (j = 0; j < 3; j++) begin
                    index = (row + i) * 5 + (col + j);
                    sum += input_buffer[index] * kernel[i * 3 + j];
                end
            end

            out_data <= sum[15:0];
            out_idx <= out_idx + 1;

            if (out_idx == 8)
                done <= 1;
        end
    end

endmodule
