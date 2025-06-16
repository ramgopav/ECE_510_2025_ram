module weight_rom #(parameter FILTS=32) (
    input  logic [4:0] addr,
    output logic [8*9-1:0] data
);
    logic [7:0] rom [0:FILTS-1][0:8];
    initial $readmemh("weights.mem", rom);
    always_comb data = {
        rom[addr][0], rom[addr][1], rom[addr][2],
        rom[addr][3], rom[addr][4], rom[addr][5],
        rom[addr][6], rom[addr][7], rom[addr][8]
    };
endmodule
