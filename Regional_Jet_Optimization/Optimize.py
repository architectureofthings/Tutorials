# Optimize.py
# Created:  Feb 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
import Vehicles
import Analyses
import Missions
import Procedure
import Plot_Mission
import matplotlib.pyplot as plt
from SUAVE.Optimization import Nexus, carpet_plot
import SUAVE.Optimization.Package_Setups.scipy_setup as scipy_setup
import VyPy
import pyOpt
# ----------------------------------------------------------------------        
#   Run the whole thing
# ----------------------------------------------------------------------  
def main():
    problem = setup()
    output = problem.objective()
    #uncomment these lines when you want to start an optimization problem from a different initial guess
    '''
    inputs                                   = [1.28, 1.38]
    scaling                                  = problem.optimization_problem.inputs[:,3] #have to rescale inputs to start problem from here
    scaled_inputs                            = np.multiply(inputs,scaling)
    problem.optimization_problem.inputs[:,1] = scaled_inputs
    '''
    
    #optimize
    #output = scipy_setup.SciPy_Solve(problem,solver='SLSQP')
    #print output
  
    
    #variable_sweep(problem)  #uncomment this to view some contours of the problem
    print 'fuel burn=', problem.summary.base_mission_fuelburn
    print 'fuel margin=', problem.all_constraints()
    
    #Plot_Mission.plot_mission(problem)
    
    return



# ----------------------------------------------------------------------        
#   Inputs, Objective, & Constraints
# ----------------------------------------------------------------------  

def setup():

    nexus = Nexus()
    problem = Data()
    nexus.optimization_problem = problem

    # -------------------------------------------------------------------
    # Inputs
    # -------------------------------------------------------------------

    #   [ tag                            , initial, (lb,ub)             , scaling , units ]
    problem.inputs = np.array([
        [ 'wing_area'                    ,  95    , (   90. ,   130.   ) ,   100. , Units.meter**2],
        [ 'cruise_altitude'              ,  11    , (   9   ,    14.   ) ,   10.  , Units.km],
    ])
    
   
    
    # -------------------------------------------------------------------
    # Objective
    # -------------------------------------------------------------------

    # throw an error if the user isn't specific about wildcards
    # [ tag, scaling, units ]
    problem.objective = np.array([
        [ 'fuel_burn', 10000, Units.kg ]
    ])
    
    
    # -------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------
    
    # [ tag, sense, edge, scaling, units ]
    problem.constraints = np.array([
        [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less], #fuel margin defined here as fuel 
    ])
    
    # -------------------------------------------------------------------
    #  Aliases
    # -------------------------------------------------------------------
    
    # [ 'alias' , ['data.path1.name','data.path2.name'] ]

    problem.aliases = [
        [ 'wing_area'                        ,   ['vehicle_configurations.*.wings.main_wing.areas.reference',
                                                  'vehicle_configurations.*.reference_area'                    ]],
        [ 'cruise_altitude'                  , 'missions.base.segments.climb_5.altitude_end'                    ],
        [ 'fuel_burn'                        ,    'summary.base_mission_fuelburn'                               ],
        [ 'design_range_fuel_margin'         ,    'summary.max_zero_fuel_margin'                                ],
    ]    
    '''
    #TASOPT imports
    from  mission_B737_TASOPT import full_setup, mission_setup

    configs, analyses = full_setup()
    nexus.vehicle_configurations = configs
    nexus.analyses = analyses
    nexus.mission  = analyses.mission
    #nexus.mission  = mission_setup(nexus.analyses)
    '''
    
    
    # -------------------------------------------------------------------
    #  Vehicles
    # -------------------------------------------------------------------
   
    #import Vehicle_TASOPT
    #nexus.vehicle_configurations = Vehicle_TASOPT.setup()
    nexus.vehicle_configurations = Vehicles.setup()
    
    
    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    nexus.analyses = Analyses.setup(nexus.vehicle_configurations)
    
    
    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
    nexus.missions = Missions.setup(nexus.analyses)
    
   
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.procedure = Procedure.setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary = Data()    
    nexus.total_number_of_iterations = 0
    return nexus
    
def variable_sweep(problem):    
    number_of_points = 5
    outputs=carpet_plot(problem, number_of_points, 0, 0)  #run carpet plot, suppressing default plots
    inputs =outputs.inputs
    objective=outputs.objective
    constraints=outputs.constraint_val
    plt.figure(0)
    CS = plt.contourf(inputs[0,:],inputs[1,:], objective, 20, linewidths=2)
    cbar = plt.colorbar(CS)
    
    cbar.ax.set_ylabel('fuel burn (kg)')
    CS_const=plt.contour(inputs[0,:],inputs[1,:], constraints[0,:,:])
    plt.clabel(CS_const, inline=1, fontsize=10)
    cbar = plt.colorbar(CS_const)
    cbar.ax.set_ylabel('fuel margin')
    
    
    
    plt.xlabel('wing area (m^2)')
    plt.ylabel('cruise_altitude (km)')
    
    
    wing_1 = np.array([ 0.95,	0.9500000149011611,	0.95,	0.95,	0.9500000149011611,	0.95,	0.95,	0.9500000149011611,	0.95,	1.0830895945429801,	1.0830896094441413,	1.0830895945429801,	1.0830895945429801,	1.0830896094441413,	1.0830895945429801,	1.0830895945429801,	1.0830896094441413,	1.0830895945429801,	1.021757391325076,	1.0217574062262371,	1.021757391325076,	1.021757391325076,	1.0217574062262371,	1.021757391325076,	1.021757391325076,	1.0217574062262371,	1.021757391325076,	0.923430766276824,	0.9234307811779852,	0.923430766276824,	0.923430766276824,	0.9234307811779852,	0.923430766276824,	0.923430766276824,	0.9234307811779852,	0.923430766276824,	0.9458241453484385,	0.9458241602495997,	0.9458241453484385,	0.9458241453484385,	0.9458241602495997,	0.9458241453484385,	0.9458241453484385,	0.9458241602495997,	0.9458241453484385,	0.943053052966747,	0.9430530678679082,	0.943053052966747,	0.943053052966747,	0.9430530678679082,	0.943053052966747,	0.943053052966747,	0.9430530678679082,	0.943053052966747,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	1.0,	1.0,	1.0,	1.0,	1.0,	1.1000000000000001,	1.1000000000000001,	1.1000000000000001,	1.1000000000000001,	1.1000000000000001,	1.2,	1.2,	1.2,	1.2,	1.2,	1.3,	1.3,	1.3,	1.3,	1.3, 0.94305305 ])*100.
    alt_1  = [11.        ,	11.        ,	11.00000015,	11.        ,	11.        ,	11.00000015,	11.        ,	11.        ,	11.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015, 	9.        ,	9.       ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	9.        ,	9.00000015,	9.        ,	10.25      ,	11.5       ,	12.75      ,	14.        ,	9.        ,	10.25      ,	11.5       ,	12.75      ,	14.        ,	9.        ,	10.25      ,	11.5       ,	12.75      ,	14.        ,	9.        ,	10.25      ,	11.5       ,	12.75      ,	14.        ,	9.        ,	10.25      ,	11.5       ,	12.75      ,	14. , 9.       ]  
    
    wing_2 = np.array([1.28,	1.2800000149011612,	1.28,	1.28,	1.2800000149011612,	1.28,	1.28,	1.2800000149011612,	1.28,	1.3,	1.3000000149011612,	1.3,	1.3,	1.3000000149011612,	1.3,	1.3,	1.3000000149011612,	1.3,	1.2512983213829585,	1.2512983362841197,	1.2512983213829585,	1.2512983213829585,	1.2512983362841197,	1.2512983213829585,	1.2512983213829585,	1.2512983362841197,	1.2512983213829585,	1.2027018036450188,	1.20270181854618,	1.2027018036450188,	1.2027018036450188,	1.20270181854618,	1.2027018036450188,	1.2027018036450188,	1.20270181854618,	1.2027018036450188,	0.9696195074510734,	0.9696195223522346,	0.9696195074510734,	0.9696195074510734,	0.9696195223522346,	0.9696195074510734,	0.9696195074510734,	0.9696195223522346,	0.9696195074510734,	0.9356100057984995,	0.9356100206996607,	0.9356100057984995,	0.9356100057984995,	0.9356100206996607,	0.9356100057984995,	0.9356100057984995,	0.9356100206996607,	0.9356100057984995,	0.9442290521247874,	0.9442290670259486,	0.9442290521247874,	0.9442290521247874,	0.9442290670259486,	0.9442290521247874,	0.9442290521247874,	0.9442290670259486,	0.9442290521247874,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	0.90000000000000002,	1.0,	1.0,	1.0,	1.0,	1.0,	1.1000000000000001,	1.1000000000000001, 0.94422905 ])* 100.
    
    alt_2  = [ 13.8 , 13.8 ,  13.80000015 , 13.8 , 13.8 , 13.80000015 , 13.8 , 13.8, 13.80000015 , 10.86578142 , 10.86578142,  10.86578157 , 10.86578142 , 10.86578142 , 10.86578157 , 10.86578142,  10.86578142 , 10.86578157 ,  9.  ,  9. ,  9.00000015 ,  9., 9.,     9.00000015 ,  9. ,  9. ,  9.00000015 ,  9.26299784  , 9.26299784 ,  9.26299799 ,  9.26299784 ,  9.26299784 ,  9.26299799 ,  9.26299784 ,  9.26299784 ,  9.26299799 ,  9.21358943 ,  9.21358943  , 9.21358957 ,  9.21358943 ,  9.21358943 ,  9.21358957 ,  9.21358943 ,  9.21358943 ,  9.21358957 ,  9. ,  9.,  9.00000015 ,  9., 9. , 9.00000015 ,  9.,  9.  ,  9.00000015 ,  9.  ,  9., 9.00000015 ,  9.  ,  9. ,  9.00000015 ,  9. ,     9.,  9.00000015 ,  9. , 10.25 , 11.5 , 12.75, 14., 9.,10.25 , 11.5 , 12.75 , 14. ,  9.  , 10.25 , 9.     ]
   
    
    
    #now plot optimization path (note that these data points were post-processed into a plottable format)
    #wing_1  = [95          ,	95.00000149 ,	95          ,	95          ,	95.00000149 ,	95          ,	95          ,	95.00000149 ,	95          ,	106.674165  ,	106.6741665 ,	106.674165  ,	106.674165  ,	106.6741665 ,	106.674165  ,	106.674165  ,	106.6741665 ,	106.674165  ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	110.520489  ,	110.5204905 ,	110.520489  ,	110.520489  ,	110.5204905 ,	110.520489  ,	110.520489  ,	110.5204905 ,	110.520489  ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.2149828]
    #alt_1   = [11.0              ,	11.0              ,	11.000000149011612,	11.0              ,	11.0              ,	11.000000149011612,	11.0              ,	11.0              ,	11.000000149011612,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.52829047]
    #wing_2  = [128        ,	128.0000015,	128        ,	128        ,	128.0000015,	128        ,	128        ,	128.0000015,	128        ,	130        ,	130.0000015,	130        ,	130        ,	130.0000015,	130        ,	130        ,	130.0000015,	130        ,	122.9564124,	122.9564139,	122.9564124,	122.9564124,	122.9564139,	122.9564124,	122.9564124,	122.9564139,	122.9564124,	116.5744347,	116.5744362,	116.5744347,	116.5744347,	116.5744362,	116.5744347,	116.5744347,	116.5744362,	116.5744347,	116.3530891,	116.3530906,	116.3530891,	116.3530891,	116.3530906,	116.3530891,	116.3530891,	116.3530906,	116.3530891]
    #alt_2   = [13.8,	13.799999999999999,	13.80000014901161,	13.799999999999999,	13.799999999999999,	13.80000014901161,	13.799999999999999,	13.799999999999999,	13.80000014901161,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.402627869388722,	11.402627869388722,	11.402628018400334,	11.402627869388722,	11.402627869388722,	11.402628018400334,	11.402627869388722,	11.402627869388722,	11.402628018400334]

    '''
    opt_1   = plt.plot(wing_1, alt_1, label='optimization path 1')
    init_1  = plt.plot(wing_1[0], alt_1[0], 'ko')
    final_1 = plt.plot(wing_1[-1], alt_1[-1], 'kx')
    
    opt_2   = plt.plot(wing_2, alt_2, 'k--', label='optimization path 2')
    init_2  = plt.plot(wing_2[0], alt_2[0], 'ko', label= 'initial points')
    final_2 = plt.plot(wing_2[-1], alt_2[-1], 'kx', label= 'final points')
    '''
    plt.legend(loc='upper left')  
    plt.show(block=True)    
    
      

    return
    
    
if __name__ == '__main__':
    main()
    
    
