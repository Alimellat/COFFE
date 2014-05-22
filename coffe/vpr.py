import sys
import os

def print_vpr_file(vpr_file, fpga_inst):


# get delay values
Tdel = fpga_inst.sb_mux.delay
T_ipin_cblock = fpga_inst.cb_mux.delay
local_CLB_routing = fpga_inst.logic_cluster.local_mux.delay
local_feedback = fpga_inst.logic_cluster.ble.local_output.delay
logic_block_output = fpga_inst.logic_cluster.ble.general_output.delay

# get lut delays
lut_input_names = fpga_inst.logic_cluster.ble.lut.input_drivers.keys()
lut_input_names.sort()
lut_delays = {}
for input_name in lut_input_names:
	lut_input = fpga_inst.logic_cluster.ble.lut.input_drivers[input_name]
	driver_delay = max(lut_input.driver.delay, lut_input.not_driver.delay)
	path_delay = lut_input.delay
	lut_delays[input_name] = driver_delay+path_delay
	
# get areas
grid_logic_tile_area = fpga_inst.area_dict["logic_cluster"]/fpga_inst.specs.min_width_tran_area
ipin_mux_trans_size = fpga_inst.area_dict["ipin_mux_trans_size"]/fpga_inst.specs.min_width_tran_area
mux_trans_size = fpga_inst.area_dict["switch_mux_trans_size"]/fpga_inst.specs.min_width_tran_area
buf_size = fpga_inst.area_dict["switch_buf_size"]/fpga_inst.specs.min_width_tran_area

#   <architecture>
  
#   <!-- ODIN II specific config -->
#   <models>
#     <model name="multiply">
#       <input_ports>
#       <port name="a"/>
#       <port name="b"/>
#       </input_ports>
#       <output_ports>
#       <port name="out"/>
#       </output_ports>
#     </model>
    
#     <model name="single_port_ram">
#       <input_ports>
#       <port name="we"/>     <!-- control -->
#       <port name="addr"/>  <!-- address lines -->
#       <port name="data"/>  <!-- data lines can be broken down into smaller bit widths minimum size 1 -->
#       <port name="clk" is_clock="1"/>  <!-- memories are often clocked -->
#       </input_ports>
#       <output_ports>
#       <port name="out"/>   <!-- output can be broken down into smaller bit widths minimum size 1 -->
#       </output_ports>
#     </model>

#     <model name="dual_port_ram">
#       <input_ports>
#       <port name="we1"/>     <!-- write enable -->
#       <port name="we2"/>     <!-- write enable -->
#       <port name="addr1"/>  <!-- address lines -->
#       <port name="addr2"/>  <!-- address lines -->
#       <port name="data1"/>  <!-- data lines can be broken down into smaller bit widths minimum size 1 -->
#       <port name="data2"/>  <!-- data lines can be broken down into smaller bit widths minimum size 1 -->
#       <port name="clk" is_clock="1"/>  <!-- memories are often clocked -->
#       </input_ports>
#       <output_ports>
#       <port name="out1"/>   <!-- output can be broken down into smaller bit widths minimum size 1 -->
#       <port name="out2"/>   <!-- output can be broken down into smaller bit widths minimum size 1 -->
#       </output_ports>
#     </model>

#   </models>
#   <!-- ODIN II specific config ends -->
 
#   <!-- Physical descriptions begin -->
#   <layout auto="1.0"/>

# 		<device>
#       ***************************************************
# 			<sizing R_minW_nmos="13090.000000" R_minW_pmos="19086.831111" ipin_mux_trans_size="ipin_mux_trans_size"/>
#       ***************************************************
#       ***************************************************
# 			<timing C_ipin_cblock="0.000000e+00" T_ipin_cblock="T_ipin_cblock"/>
#       ***************************************************
#       ***************************************************
# 			<area grid_logic_tile_area="grid_logic_tile_area"/>
#       ***************************************************
# 			<chan_width_distr>
# 				<io width="1.000000"/>
# 				<x distr="uniform" peak="1.000000"/>
# 				<y distr="uniform" peak="1.000000"/>
# 			</chan_width_distr>
# 			<switch_block type="wilton" fs="3"/>
# 		</device>
# 		<switchlist>
#       ***************************************************
# 			<switch type="mux" name="0" R="0.000000" Cin="0.000000e+00" Cout="0.000000e+00" Tdel="Tdel" mux_trans_size="mux_trans_size" buf_size="buf_size"/>
#       ***************************************************
# 		</switchlist>
# 		<segmentlist>
# 			<segment freq="1.000000" length="4" type="unidir" Rmetal="0.000000" Cmetal="0.000000e+00">
# 			<mux name="0"/>
# 			<sb type="pattern">1 1 1 1 1</sb>
# 			<cb type="pattern">1 1 1 1</cb>
# 			</segment>
# 		</segmentlist>

# 	  <complexblocklist>
#        <!-- Capacity is a unique property of I/Os, it is the maximum number of I/Os that can be placed at the same (X,Y) location on the FPGA -->
#       <pb_type name="io" capacity="8">
#         <input name="outpad" num_pins="1"/>
#         <output name="inpad" num_pins="1"/>
#         <clock name="clock" num_pins="1"/>

#         <!-- IOs can operate as either inputs or outputs -->
#         <mode name="inpad">
#           <pb_type name="inpad" blif_model=".input" num_pb="1">
#             <output name="inpad" num_pins="1"/>
#           </pb_type>
#           <interconnect>
#             <direct name="inpad" input="inpad.inpad" output="io.inpad">
#             <delay_constant max="4.243e-11" in_port="inpad.inpad" out_port="io.inpad"/>
#             </direct>
#           </interconnect>
      
#         </mode>
#         <mode name="outpad">
#           <pb_type name="outpad" blif_model=".output" num_pb="1">
#             <input name="outpad" num_pins="1"/>
#           </pb_type>
#           <interconnect>
#             <direct name="outpad" input="io.outpad" output="outpad.outpad">
#             <delay_constant max="1.394e-11" in_port="io.outpad" out_port="outpad.outpad"/>
#             </direct>
#           </interconnect>
#         </mode>

#         <fc default_in_type="frac" default_in_val="0.15" default_out_type="frac" default_out_val="0.10"/>

#         <!-- IOs go on the periphery of the FPGA, for consistency, 
#           make it physically equivalent on all sides so that only one definition of I/Os is needed.
#           If I do not make a physically equivalent definition, then I need to define 4 different I/Os, one for each side of the FPGA
#         -->
#         <pinlocations pattern="custom">
#           <loc side="left">io.outpad io.inpad io.clock</loc>
#           <loc side="top">io.outpad io.inpad io.clock</loc>
#           <loc side="right">io.outpad io.inpad io.clock</loc>
#           <loc side="bottom">io.outpad io.inpad io.clock</loc>
#         </pinlocations>

#         <gridlocations>
#           <loc type="perimeter" priority="10"/>
#         </gridlocations>

#       </pb_type>

#       <!-- Logic cluster definition -->
#       <pb_type name="clb">
#         <input name="I1" num_pins="10" equivalent="true"/>
#         <input name="I2" num_pins="10" equivalent="true"/>
#         <input name="I3" num_pins="10" equivalent="true"/>
#         <input name="I4" num_pins="10" equivalent="true"/>
#         <output name="O1" num_pins="2" equivalent="true"/>
#         <output name="O2" num_pins="2" equivalent="true"/>
#         <output name="O3" num_pins="2" equivalent="true"/>
#         <output name="O4" num_pins="2" equivalent="true"/>
#         <output name="O5" num_pins="2" equivalent="true"/>
#         <output name="O6" num_pins="2" equivalent="true"/>
#         <output name="O7" num_pins="2" equivalent="true"/>
#         <output name="O8" num_pins="2" equivalent="true"/>
#         <output name="O9" num_pins="2" equivalent="true"/>
#         <output name="O10" num_pins="2" equivalent="true"/>
#         <clock name="clk" num_pins="1"/>

#         <!-- Basic logic element definition -->
# 		<pb_type name="ble6" num_pb="10">
# 		  <input name="in_A" num_pins="1" equivalent="false"/>
# 		  <input name="in_B" num_pins="1" equivalent="false"/>
# 		  <input name="in_C" num_pins="1" equivalent="false"/>
# 		  <input name="in_D" num_pins="1" equivalent="false"/>
# 		  <input name="in_E" num_pins="1" equivalent="false"/>
# 		  <input name="in_F" num_pins="1" equivalent="false"/>
# 		  <output name="out_local" num_pins="1" equivalent="false"/>
# 		  <output name="out_routing" num_pins="2" equivalent="true"/>
# 		  <clock name="clk" num_pins="1"/> 
# 		  <pb_type name="lut6" blif_model=".names" num_pb="1" class="lut">
# 			<input name="in" num_pins="6" port_class="lut_in"/>
# 			<output name="out" num_pins="1" port_class="lut_out"/>
# 			<!-- We define the LUT delays on the LUT pins instead of through the LUT -->
# 			<delay_matrix type="max" in_port="lut6.in" out_port="lut6.out">
# 			   0
# 			   0
# 			   0
# 			   0
# 			   0
# 			   0
# 			</delay_matrix>
# 		  </pb_type>
# 		  <pb_type name="ff" blif_model=".latch" num_pb="1" class="flipflop">
# 			<input name="D" num_pins="1" port_class="D"/>
# 			<output name="Q" num_pins="1" port_class="Q"/>
# 			<clock name="clk" num_pins="1" port_class="clock"/>
# 			<T_setup value="1.891e-11" port="ff.D" clock="clk"/>
# 			<T_clock_to_Q max="6.032e-11" port="ff.Q" clock="clk"/>
# 		  </pb_type>

# 		  <interconnect>
# 			<!-- BLE input to LUT input direct connections and delays -->
# 			<direct name="direct1" input="ble6.in_A" output="lut6.in[0:0]">
#       ***************************************************
# 			  <delay_constant max="***lut_a" in_port="ble6.in_A" out_port="lut6.in[0:0]" />
#       ***************************************************
# 			</direct>
# 			<direct name="direct2" input="ble6.in_B" output="lut6.in[1:1]">
#       ***************************************************
# 			  <delay_constant max="***lut_b" in_port="ble6.in_B" out_port="lut6.in[1:1]" />
#       ***************************************************
# 			</direct>
# 			<direct name="direct3" input="ble6.in_D" output="lut6.in[3:3]">
#       ***************************************************
# 			  <delay_constant max="***lut_d" in_port="ble6.in_D" out_port="lut6.in[3:3]" />
#       ***************************************************
# 			</direct>
# 			<direct name="direct4" input="ble6.in_E" output="lut6.in[4:4]">
#       ***************************************************
# 			  <delay_constant max="***lut_e" in_port="ble6.in_E" out_port="lut6.in[4:4]" />
#       ***************************************************
# 			</direct>
# 			<direct name="direct5" input="ble6.in_F" output="lut6.in[5:5]">
#       ***************************************************
# 			  <delay_constant max="***lut_f" in_port="ble6.in_F" out_port="lut6.in[5:5]" />
#       ***************************************************
# 			</direct>
# 			<!--Clock -->  
# 			<direct name="direct6" input="ble6.clk" output="ff.clk"/>			
# 	        <!-- Register feedback mux -->   
# 	        <mux name="mux1" input="ble6.in_C ff.Q" output="lut6.in[2:2]">
#       ***************************************************
# 			  <delay_constant max="***lut_c" in_port="ble6.in_C" out_port="lut6.in[2:2]" />
#       ***************************************************
# 			  <delay_constant max="?????" in_port="ff.Q" out_port="lut6.in[2:2]" />  
# 			</mux>
# 	        <!-- FF input selection mux -->
# 	        <mux name="mux2" input="lut6.out ble6.in_C" output="ff.D">
# 			  <delay_constant max="?????" in_port="lut6.out" out_port="ff.D" />
# 			  <delay_constant max="?????" in_port="ble6.in_C" out_port="ff.D" />
# 			</mux>
# 	        <!-- BLE output (local) -->                  
# 			<mux name="mux3" input="ff.Q lut6.out" output="ble6.out_local">
# 			  <delay_constant max="?????" in_port="ff.Q" out_port="ble6.out_local" />
#       ***************************************************
# 	          <delay_constant max="***local feedback" in_port="lut6.out" out_port="ble6.out_local" />
#       ***************************************************
# 			</mux>
# 	        <!-- BLE output (routing 1) --> 
# 	        <mux name="mux4" input="ff.Q lut6.out" output="ble6.out_routing[0:0]">
#       ***************************************************
# 	          <delay_constant max="***local CLB routing" in_port="ff.Q" out_port="ble6.out_routing[0:0]" />
#       ***************************************************
#       ***************************************************
# 			  <delay_constant max="***logic block output" in_port="lut6.out" out_port="ble6.out_routing[0:0]" />
#       ***************************************************
# 			</mux>
# 	        <!-- BLE output (routing 2) --> 
# 			<mux name="mux5" input="ff.Q lut6.out" output="ble6.out_routing[1:1]">
#       ***************************************************
# 	          <delay_constant max="***local CLB routing" in_port="ff.Q" out_port="ble6.out_routing[1:1]" />
#       ***************************************************
#       ***************************************************
# 			  <delay_constant max="***logic block output" in_port="lut6.out" out_port="ble6.out_routing[1:1]" />
#       ***************************************************
# 			</mux>
# 		  </interconnect>
# 		</pb_type>

        
#         <interconnect>
#           <!-- 50% sparsely populated local routing -->
#           <complete name="lutA" input="clb.I4 clb.I3 ble6[1:0].out_local ble6[3:2].out_local ble6[8:8].out_local" output="ble6[9:0].in_A">
# 			<delay_constant max="6.07717e-11" in_port="clb.I4" out_port="ble6.in_A" />
# 			<delay_constant max="6.07717e-11" in_port="clb.I3" out_port="ble6.in_A" />
#           </complete>
# 	      <complete name="lutB" input="clb.I3 clb.I2 ble6[3:2].out_local ble6[5:4].out_local ble6[9:9].out_local" output="ble6[9:0].in_B">
# 	        <delay_constant max="6.07717e-11" in_port="clb.I3" out_port="ble6.in_B" />
# 	        <delay_constant max="6.07717e-11" in_port="clb.I2" out_port="ble6.in_B" />
#           </complete>
# 	      <complete name="lutC" input="clb.I2 clb.I1 ble6[5:4].out_local ble6[7:6].out_local ble6[8:8].out_local" output="ble6[9:0].in_C">
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I2" out_port="ble6.in_C" />
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I1" out_port="ble6.in_C" />
#           </complete>
# 	      <complete name="lutD" input="clb.I4 clb.I2 ble6[1:0].out_local ble6[5:4].out_local ble6[9:9].out_local" output="ble6[9:0].in_D">
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I4" out_port="ble6.in_D" />
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I2" out_port="ble6.in_D" />
#           </complete>
# 	      <complete name="lutE" input="clb.I3 clb.I1 ble6[3:2].out_local ble6[7:6].out_local ble6[8:8].out_local" output="ble6[9:0].in_E">
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I3" out_port="ble6.in_E" />
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I1" out_port="ble6.in_E" />
#           </complete>
# 	      <complete name="lutF" input="clb.I4 clb.I1 ble6[1:0].out_local ble6[7:6].out_local ble6[9:9].out_local" output="ble6[9:0].in_F">
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I4" out_port="ble6.in_F" />
# 	      	<delay_constant max="6.07717e-11" in_port="clb.I1" out_port="ble6.in_F" />
#           </complete>
#           <complete name="clks" input="clb.clk" output="ble6[9:0].clk">
#           </complete>
          
#           <!-- Direct connections to CLB outputs -->
#           <direct name="clbouts1" input="ble6[0:0].out_routing" output="clb.O1"/>
#           <direct name="clbouts2" input="ble6[1:1].out_routing" output="clb.O2"/>
#           <direct name="clbouts3" input="ble6[2:2].out_routing" output="clb.O3"/>
#           <direct name="clbouts4" input="ble6[3:3].out_routing" output="clb.O4"/>
#           <direct name="clbouts5" input="ble6[4:4].out_routing" output="clb.O5"/>
#           <direct name="clbouts6" input="ble6[5:5].out_routing" output="clb.O6"/>
#           <direct name="clbouts7" input="ble6[6:6].out_routing" output="clb.O7"/>
#           <direct name="clbouts8" input="ble6[7:7].out_routing" output="clb.O8"/>
#           <direct name="clbouts9" input="ble6[8:8].out_routing" output="clb.O9"/>
#           <direct name="clbouts10" input="ble6[9:9].out_routing" output="clb.O10"/>
#         </interconnect>

#         <fc default_in_type="frac" default_in_val="0.2" default_out_type="frac" default_out_val="0.025"/>

#         <!-- Two sided connectivity CLB architecture--> 
#         <pinlocations pattern="custom">
# 		  <loc side="right">clb.O1 clb.O2 clb.O3 clb.O4 clb.O5 clb.I1 clb.I3 clb.clk</loc> 
#           <loc side="bottom">clb.O6 clb.O7 clb.O8 clb.O9 clb.O10 clb.I2 clb.I4 clb.clk</loc>      
#         </pinlocations>
#         <gridlocations>
#           <loc type="fill" priority="1"/>
#         </gridlocations>
#       </pb_type>

#       <!-- This is the 36*36 uniform mult -->
#       <pb_type name="mult_36" height="4">
#           <input name="a" num_pins="36"/>
#           <input name="b" num_pins="36"/>
#           <output name="out" num_pins="72"/>

#           <mode name="two_divisible_mult_18x18">
#             <pb_type name="divisible_mult_18x18" num_pb="2">
#               <input name="a" num_pins="18"/>
#               <input name="b" num_pins="18"/>
#               <output name="out" num_pins="36"/>

#               <mode name="two_mult_9x9">
#                 <pb_type name="mult_9x9_slice" num_pb="2">
#                   <input name="A_cfg" num_pins="9"/>
#                   <input name="B_cfg" num_pins="9"/>
#                   <output name="OUT_cfg" num_pins="18"/>

#                   <pb_type name="mult_9x9" blif_model=".subckt multiply" num_pb="1">
#                     <input name="a" num_pins="9"/>
#                     <input name="b" num_pins="9"/>
#                     <output name="out" num_pins="18"/>
#                     <delay_constant max="1.667e-9" in_port="mult_9x9.a" out_port="mult_9x9.out"/>
#                     <delay_constant max="1.667e-9" in_port="mult_9x9.b" out_port="mult_9x9.out"/>
#                   </pb_type>

#                   <interconnect>
#                     <direct name="a2a" input="mult_9x9_slice.A_cfg" output="mult_9x9.a">
#                     </direct>
#                     <direct name="b2b" input="mult_9x9_slice.B_cfg" output="mult_9x9.b">
#                     </direct>
#                     <direct name="out2out" input="mult_9x9.out" output="mult_9x9_slice.OUT_cfg">
#                     </direct>
#                   </interconnect>
#                 </pb_type>
#                 <interconnect>
#                   <direct name="a2a" input="divisible_mult_18x18.a" output="mult_9x9_slice[1:0].A_cfg">
#                   </direct>
#                   <direct name="b2b" input="divisible_mult_18x18.b" output="mult_9x9_slice[1:0].B_cfg">
#                   </direct>
#                   <direct name="out2out" input="mult_9x9_slice[1:0].OUT_cfg" output="divisible_mult_18x18.out">
#                   </direct>
#                 </interconnect>
#               </mode>

#               <mode name="mult_18x18">
#                 <pb_type name="mult_18x18_slice" num_pb="1">
#                   <input name="A_cfg" num_pins="18"/>
#                   <input name="B_cfg" num_pins="18"/>
#                   <output name="OUT_cfg" num_pins="36"/>

#                   <pb_type name="mult_18x18" blif_model=".subckt multiply" num_pb="1" >
#                     <input name="a" num_pins="18"/>
#                     <input name="b" num_pins="18"/>
#                     <output name="out" num_pins="36"/>
#                     <delay_constant max="1.667e-9" in_port="mult_18x18.a" out_port="mult_18x18.out"/>
#                     <delay_constant max="1.667e-9" in_port="mult_18x18.b" out_port="mult_18x18.out"/>
#                   </pb_type>

#                   <interconnect>
#                     <direct name="a2a" input="mult_18x18_slice.A_cfg" output="mult_18x18.a">
#                     </direct>
#                     <direct name="b2b" input="mult_18x18_slice.B_cfg" output="mult_18x18.b">
#                     </direct>
#                     <direct name="out2out" input="mult_18x18.out" output="mult_18x18_slice.OUT_cfg">
#                     </direct>
#                   </interconnect>
#                 </pb_type>
#                 <interconnect>
#                   <direct name="a2a" input="divisible_mult_18x18.a" output="mult_18x18_slice.A_cfg">
#                   </direct>
#                   <direct name="b2b" input="divisible_mult_18x18.b" output="mult_18x18_slice.B_cfg">
#                   </direct>
#                   <direct name="out2out" input="mult_18x18_slice.OUT_cfg" output="divisible_mult_18x18.out">
#                   </direct>
#                 </interconnect>
#               </mode>
#             </pb_type>
#             <interconnect>
#               <direct name="a2a" input="mult_36.a" output="divisible_mult_18x18[1:0].a">
#               </direct>
#               <direct name="b2b" input="mult_36.b" output="divisible_mult_18x18[1:0].b">
#               </direct>
#               <direct name="out2out" input="divisible_mult_18x18[1:0].out" output="mult_36.out">
#               </direct>
#             </interconnect>
#           </mode>

#           <mode name="mult_36x36">
#             <pb_type name="mult_36x36_slice" num_pb="1">
#               <input name="A_cfg" num_pins="36"/>
#               <input name="B_cfg" num_pins="36"/>
#               <output name="OUT_cfg" num_pins="72"/>

#               <pb_type name="mult_36x36" blif_model=".subckt multiply" num_pb="1">
#                 <input name="a" num_pins="36"/>
#                 <input name="b" num_pins="36"/>
#                 <output name="out" num_pins="72"/>
#                 <delay_constant max="1.667e-9" in_port="mult_36x36.a" out_port="mult_36x36.out"/>
#                 <delay_constant max="1.667e-9" in_port="mult_36x36.b" out_port="mult_36x36.out"/>
#               </pb_type>

#               <interconnect>
#                 <direct name="a2a" input="mult_36x36_slice.A_cfg" output="mult_36x36.a">
#                 </direct>
#                 <direct name="b2b" input="mult_36x36_slice.B_cfg" output="mult_36x36.b">
#                 </direct>
#                 <direct name="out2out" input="mult_36x36.out" output="mult_36x36_slice.OUT_cfg">
#                 </direct>
#               </interconnect>
#             </pb_type>
#             <interconnect>
#               <direct name="a2a" input="mult_36.a" output="mult_36x36_slice.A_cfg">
#               </direct>
#               <direct name="b2b" input="mult_36.b" output="mult_36x36_slice.B_cfg">
#               </direct>
#               <direct name="out2out" input="mult_36x36_slice.OUT_cfg" output="mult_36.out">
#               </direct>
#             </interconnect>
#           </mode>

#         <fc default_in_type="frac" default_in_val="0.15" default_out_type="frac" default_out_val="0.10"/>
#         <pinlocations pattern="spread"/>

#         <gridlocations>
#           <loc type="col" start="4" repeat="8" priority="2"/>
#         </gridlocations>
#       </pb_type>


# <!-- 32 Kb Memory based off Stratix IV 9K memory and Virtex V 36 Kb.  Setup time set to match flip-flop setup time at 40 nm. Clock to q based off Stratix IV 600 max MHz  -->
#       <pb_type name="memory" height="6">
#           <input name="addr1" num_pins="15"/>
#           <input name="addr2" num_pins="15"/>
#           <input name="data" num_pins="64"/>
#           <input name="we1" num_pins="1"/>
#           <input name="we2" num_pins="1"/>
#           <output name="out" num_pins="64"/>
#           <clock name="clk" num_pins="1"/>

#           <mode name="mem_512x64_sp">
#             <pb_type name="mem_512x64_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="9" port_class="address"/>
#               <input name="data" num_pins="64" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="64" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_512x64_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_512x64_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_512x64_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_512x64_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[8:0]" output="mem_512x64_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[63:0]" output="mem_512x64_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_512x64_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_512x64_sp.out" output="memory.out[63:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_512x64_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>
          
#           <mode name="mem_1024x32_sp">
#             <pb_type name="mem_1024x32_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="10" port_class="address"/>
#               <input name="data" num_pins="32" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="32" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_1024x32_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[9:0]" output="mem_1024x32_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[31:0]" output="mem_1024x32_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_1024x32_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_1024x32_sp.out" output="memory.out[31:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_1024x32_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>

          
#           <mode name="mem_2048x16_sp">
#             <pb_type name="mem_2048x16_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="11" port_class="address"/>
#               <input name="data" num_pins="16" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="16" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_2048x16_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[10:0]" output="mem_2048x16_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[15:0]" output="mem_2048x16_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_2048x16_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_2048x16_sp.out" output="memory.out[15:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_2048x16_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>

#           <mode name="mem_4096x8_sp">
#             <pb_type name="mem_4096x8_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="12" port_class="address"/>
#               <input name="data" num_pins="8" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="8" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_4096x8_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_4096x8_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_4096x8_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_4096x8_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[11:0]" output="mem_4096x8_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[7:0]" output="mem_4096x8_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_4096x8_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_4096x8_sp.out" output="memory.out[7:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_4096x8_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>
 
#           <mode name="mem_8192x4_sp">
#             <pb_type name="mem_8192x4_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="13" port_class="address"/>
#               <input name="data" num_pins="4" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="4" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_8192x4_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[12:0]" output="mem_8192x4_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[3:0]" output="mem_8192x4_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_8192x4_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_8192x4_sp.out" output="memory.out[3:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_8192x4_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>

#           <mode name="mem_16384x2_sp">
#             <pb_type name="mem_16384x2_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="14" port_class="address"/>
#               <input name="data" num_pins="2" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="2" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_16384x2_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[13:0]" output="mem_16384x2_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[1:0]" output="mem_16384x2_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_16384x2_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_16384x2_sp.out" output="memory.out[1:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_16384x2_sp.clk">
#               </direct>
#             </interconnect>
#           </mode>  
          
#           <mode name="mem_32768x1_sp">
#             <pb_type name="mem_32768x1_sp" blif_model=".subckt single_port_ram" class="memory" num_pb="1">
#               <input name="addr" num_pins="15" port_class="address"/>
#               <input name="data" num_pins="1" port_class="data_in"/>
#               <input name="we" num_pins="1" port_class="write_en"/>
#               <output name="out" num_pins="1" port_class="data_out"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_sp.addr" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_sp.data" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_sp.we" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_32768x1_sp.out" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[14:0]" output="mem_32768x1_sp.addr">
#               </direct>
#               <direct name="data1" input="memory.data[0:0]" output="mem_32768x1_sp.data">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_32768x1_sp.we">
#               </direct>
#               <direct name="dataout1" input="mem_32768x1_sp.out" output="memory.out[0:0]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_32768x1_sp.clk">
#               </direct>
#             </interconnect>
#           </mode> 
                   
#           <mode name="mem_1024x32_dp">
#             <pb_type name="mem_1024x32_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="10" port_class="address1"/>
#               <input name="addr2" num_pins="10" port_class="address2"/>
#               <input name="data1" num_pins="32" port_class="data_in1"/>
#               <input name="data2" num_pins="32" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="32" port_class="data_out1"/>
#               <output name="out2" num_pins="32" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_1024x32_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_1024x32_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_1024x32_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[9:0]" output="mem_1024x32_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[9:0]" output="mem_1024x32_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[31:0]" output="mem_1024x32_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[63:32]" output="mem_1024x32_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_1024x32_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_1024x32_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_1024x32_dp.out1" output="memory.out[31:0]">
#               </direct>
#               <direct name="dataout2" input="mem_1024x32_dp.out2" output="memory.out[63:32]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_1024x32_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>
          
#           <mode name="mem_2048x16_dp">
#             <pb_type name="mem_2048x16_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="11" port_class="address1"/>
#               <input name="addr2" num_pins="11" port_class="address2"/>
#               <input name="data1" num_pins="16" port_class="data_in1"/>
#               <input name="data2" num_pins="16" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="16" port_class="data_out1"/>
#               <output name="out2" num_pins="16" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x16_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_2048x16_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_2048x16_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[10:0]" output="mem_2048x16_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[10:0]" output="mem_2048x16_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[15:0]" output="mem_2048x16_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[31:16]" output="mem_2048x16_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_2048x16_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_2048x16_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_2048x16_dp.out1" output="memory.out[15:0]">
#               </direct>
#               <direct name="dataout2" input="mem_2048x16_dp.out2" output="memory.out[31:16]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_2048x16_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>
          
#           <mode name="mem_2048x8_dp">
#             <pb_type name="mem_2048x8_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="12" port_class="address1"/>
#               <input name="addr2" num_pins="12" port_class="address2"/>
#               <input name="data1" num_pins="8" port_class="data_in1"/>
#               <input name="data2" num_pins="8" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="8" port_class="data_out1"/>
#               <output name="out2" num_pins="8" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_2048x8_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_2048x8_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_2048x8_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[11:0]" output="mem_2048x8_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[11:0]" output="mem_2048x8_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[7:0]" output="mem_2048x8_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[15:8]" output="mem_2048x8_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_2048x8_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_2048x8_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_2048x8_dp.out1" output="memory.out[7:0]">
#               </direct>
#               <direct name="dataout2" input="mem_2048x8_dp.out2" output="memory.out[15:8]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_2048x8_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>
#           <mode name="mem_8192x4_dp">
#             <pb_type name="mem_8192x4_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="13" port_class="address1"/>
#               <input name="addr2" num_pins="13" port_class="address2"/>
#               <input name="data1" num_pins="4" port_class="data_in1"/>
#               <input name="data2" num_pins="4" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="4" port_class="data_out1"/>
#               <output name="out2" num_pins="4" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_8192x4_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_8192x4_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_8192x4_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[12:0]" output="mem_8192x4_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[12:0]" output="mem_8192x4_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[3:0]" output="mem_8192x4_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[7:4]" output="mem_8192x4_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_8192x4_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_8192x4_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_8192x4_dp.out1" output="memory.out[3:0]">
#               </direct>
#               <direct name="dataout2" input="mem_8192x4_dp.out2" output="memory.out[7:4]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_8192x4_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>
#           <mode name="mem_16384x2_dp">
#             <pb_type name="mem_16384x2_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="14" port_class="address1"/>
#               <input name="addr2" num_pins="14" port_class="address2"/>
#               <input name="data1" num_pins="2" port_class="data_in1"/>
#               <input name="data2" num_pins="2" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="2" port_class="data_out1"/>
#               <output name="out2" num_pins="2" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_16384x2_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_16384x2_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_16384x2_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[13:0]" output="mem_16384x2_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[13:0]" output="mem_16384x2_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[1:0]" output="mem_16384x2_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[3:2]" output="mem_16384x2_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_16384x2_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_16384x2_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_16384x2_dp.out1" output="memory.out[1:0]">
#               </direct>
#               <direct name="dataout2" input="mem_16384x2_dp.out2" output="memory.out[3:2]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_16384x2_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>
          
#           <mode name="mem_32768x1_dp">
#             <pb_type name="mem_32768x1_dp" blif_model=".subckt dual_port_ram" class="memory" num_pb="1">
#               <input name="addr1" num_pins="15" port_class="address1"/>
#               <input name="addr2" num_pins="15" port_class="address2"/>
#               <input name="data1" num_pins="1" port_class="data_in1"/>
#               <input name="data2" num_pins="1" port_class="data_in2"/>
#               <input name="we1" num_pins="1" port_class="write_en1"/>
#               <input name="we2" num_pins="1" port_class="write_en2"/>
#               <output name="out1" num_pins="1" port_class="data_out1"/>
#               <output name="out2" num_pins="1" port_class="data_out2"/>
#               <clock name="clk" num_pins="1" port_class="clock"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.addr1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.data1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.we1" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.addr2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.data2" clock="clk"/>
#               <T_setup value="2.448e-10" port="mem_32768x1_dp.we2" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_32768x1_dp.out1" clock="clk"/>
#               <T_clock_to_Q max="1.667e-9" port="mem_32768x1_dp.out2" clock="clk"/>
#             </pb_type>
#             <interconnect>
#               <direct name="address1" input="memory.addr1[14:0]" output="mem_32768x1_dp.addr1">
#               </direct>
#               <direct name="address2" input="memory.addr2[14:0]" output="mem_32768x1_dp.addr2">
#               </direct>
#               <direct name="data1" input="memory.data[0:0]" output="mem_32768x1_dp.data1">
#               </direct>
#               <direct name="data2" input="memory.data[1:1]" output="mem_32768x1_dp.data2">
#               </direct>
#               <direct name="writeen1" input="memory.we1" output="mem_32768x1_dp.we1">
#               </direct>
#               <direct name="writeen2" input="memory.we2" output="mem_32768x1_dp.we2">
#               </direct>
#               <direct name="dataout1" input="mem_32768x1_dp.out1" output="memory.out[0:0]">
#               </direct>
#               <direct name="dataout2" input="mem_32768x1_dp.out2" output="memory.out[1:1]">
#               </direct>
#               <direct name="clk" input="memory.clk" output="mem_32768x1_dp.clk">
#               </direct>
#             </interconnect>
#           </mode>

#         <fc default_in_type="frac" default_in_val="0.15" default_out_type="frac" default_out_val="0.10"/>
#         <pinlocations pattern="spread"/>
#         <gridlocations>
#           <loc type="col" start="2" repeat="8" priority="2"/>
#         </gridlocations>
#       </pb_type>


#     </complexblocklist>
#   </architecture>
