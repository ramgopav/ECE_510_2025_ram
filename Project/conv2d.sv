// Code your design here
`timescale 1ns/1ps

module conv2d (
    input  logic clk,
    input  logic rst,
    input  logic start,
    input  logic [7:0] in_data,
    input  logic [7:0] kernel [0:8],
    output logic [15:0] out_data,
    output logic done
);

    logic [7:0] input_buffer [0:24];
    logic [5:0] index;
    logic compute;
    integer sum;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            index   <= 0;
            compute <= 0;
            done    <= 0;
        end else if (start && !compute) begin
            if (index < 25) begin
                input_buffer[index] <= in_data;
                index <= index + 1;
            end 
            if (index == 24) begin  // Wait until last pixel is loaded
                compute <= 1;
            end
        end else if (compute && !done) begin
            sum = 0;
            sum += input_buffer[6]  * kernel[0];
            sum += input_buffer[7]  * kernel[1];
            sum += input_buffer[8]  * kernel[2];
            sum += input_buffer[11] * kernel[3];
            sum += input_buffer[12] * kernel[4];
            sum += input_buffer[13] * kernel[5];
            sum += input_buffer[16] * kernel[6];
            sum += input_buffer[17] * kernel[7];
            sum += input_buffer[18] * kernel[8];

            out_data <= sum[15:0];
            done <= 1;
            compute <= 0;
        end
    end
endmodule
