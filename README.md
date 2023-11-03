### Calibrated Solar Models

inlist_pre-MS

	-- Pre-main sequence Solar model --
 
 	create_pre_main_sequence_model = .true.
	save_model_when_terminate = .true.
    	save_model_filename = 'pre-MS.mod'
  	initial_mass = 1.0, initial_z = 0.018, initial_y = 0.27, mixing_length_alpha = 1.83
   	log_directory = 'LOGS_pre-MS'
    	
     	Lnuc_div_L_zams_limit = 0.99d0
     	stop_near_zams = .true.

inlist_diffusion

	-- Calibrated Solar model considering diffusion -- 	
 
	load_model_filename = 'pre-MS.mod'
 	create_pre_main_sequence_model = .false.
  	save_model_when_terminate = .true.
    	save_model_filename = '1M_at_Solar_Age_Diff.mod'
	relax_initial_Z = .true.
    	new_Z = 0.018
     	relax_initial_Y = .true.
    	new_Y = 0.27
	
 	log_directory = 'SolarModel_Diff_X' X = {0.0165, 0.018, 0.023, 0.0245}
	do_element_diffusion = .true.

	max_age = 4.57d9

inlist_no_diffusion

	-- Same as inlist_diffusion --
 	but, 
  	do_element_diffusion = .false.
