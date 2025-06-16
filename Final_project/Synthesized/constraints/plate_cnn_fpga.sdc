
set clk_period 2.0  

create_clock -name "clk" -period $clk_period [get_ports clk]


# Input constraints
set_input_delay [expr $clk_period * 0.1] -clock clk [all_inputs]
set_input_delay 0.0 -clock clk [get_ports clk]
set_input_delay 0.0 -clock clk [get_ports rst_n]

# Output constraints  
set_output_delay [expr $clk_period * 0.1] -clock clk [all_outputs]

# Drive strength for inputs (except clocks)
set_driving_cell -lib_cell NBUFFX2_HVT [remove_from_collection [all_inputs] [get_ports {clk rst_n}]]

# Load on outputs
set_load 0.05 [all_outputs]

# Clock uncertainty
set_clock_uncertainty 0.1 [get_clocks clk]

