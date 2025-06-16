@echo off
setlocal
set PORT=COM3

py -m scripts.export_weights || exit /b 1
yosys -p "read -sv rtl/*.sv; synth_ice40 -top conv2d_top_uart -json build/c.json" || exit /b 1
nextpnr-ice40 --hx8k --json build/c.json --asc build/c.asc || exit /b 1
icepack build/c.asc build/c.bin   || exit /b 1
openFPGALoader -b icebreaker build/c.bin || exit /b 1
set FPGA_PORT=%PORT%
py plate_reader.py real_car_images\Cars10.jpg --hw
endlocal
