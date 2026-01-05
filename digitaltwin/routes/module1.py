"""
These module python scripts should be designed to:
    1) Add additional URL routes for various computations
    2) Take the Input from the user and convert them to appropriate variables (string to float, etc.)
    3) Call upon the library folder "..library" to perform a function call
    4) Take the output of the library call and render it to the user

For development purposes, all the calculations can be done here, but that will make debugging and unit testing much more difficult.
"""
from ..digitaltwin import bp,kg_ # the ..digitaltwin tells the directory to look at the parent folder

import time
from flask import render_template

@bp.route("/help")
def help():
    return render_template("help.html")

@bp.route("/Start")
def start():
    return render_template("Start.html")

@bp.route("/ode")
def init():
    from ..library.ODE import three_dof
    parameters_ODE = ["m1", "m2", "m3", "k1", "k2", "k3", "c1", "c2", "c3"]
    ode_input = three_dof.ODE_input(parameters_ODE)
    print('\n' * 5)
    print("Received ODE parameters, run the ODE agent..")
    time.sleep(5)
    ode_output = three_dof.ODE_output(Mi=ode_input[0:3], Ki=ode_input[3:6], Ci=ode_input[6:9])

    print('\n' * 5)
    print("ODE agent task finished.")
    time.sleep(5)
    # ODE_output
    kg_.ODE()
    return render_template("Geo.html")

@bp.route("/geo")
def geo():
    components_ = ["floor", "pillar", "block", "V", "H"]
    directions_ = ["Len_", "Wid_", "Hei_"]
    parameters_Geometric = []    #  Get input
    # parameters all about length, width and height. The coordinates can be calculated by these.
    for i in range(0, 5):
        for j in range(0, 3):
            parameters_Geometric.append(directions_[j] + components_[i])

    print('\n' * 5)
    print("Received geometric parameters, run the Blender agent..")
    time.sleep(5)

    print('\n' * 5)
    print("Blender agent task finished.")
    return render_template("GMSH2XDMF.html")

@bp.route("/mesh")
def mesher():
    from ..library.Gmsh import three_floor_gmsh
    from ..library.Gmsh2XDMF import Gmsh2XDMF
    parameters_Gmsh = ["angle_surface_dection", "mesh_size", "Geometry_tolerance_boolean", "curve_angle"]
    Gmsh_input_ = three_floor_gmsh.Gmsh_input(parameters_Gmsh)
    print(parameters_Gmsh, Gmsh_input_)

    print('\n' * 5)
    print("Received meshing parameters, run the Gmsh agent..")

    print('\n' * 5)
    print("Gmsh agent task finished.")

    # Python XDMF
    print('\n' * 5)
    print("Run the Gmsh_to_XDMF agent..")
    time.sleep(5)

    Gmsh2XDMF.Gmsh2XDMF()

    print('\n' * 5)
    print("Gmsh2XDMF agent task finished.")
    time.sleep(5)
    return render_template("Bayes.html")
    
@bp.route("/bayes")
def bayes():
    from .. import reasoning
    # Bayesian inference
    print('\n' * 5)
    print("Run the Bayesian agent..")
    #three_floor_Bayesian.Bayesian_output()    # currently commented for testing

    print('\n' * 5)
    print("Wait for the initialisation..")
    time.sleep(30)

    def conditional_function():
        #print("test_1")
        #user_input = input("Please enter 'yes' to run the query or 'no' to stop: ")
        user_input = "no"  #user_input.strip().lower()
        #print("test_2")
        if user_input == "yes":
            print("Query is running...")
            # Place the code you want to run here
            reasoning.run()
        elif user_input == "no":
            print("Query has been stopped.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Run the function
    conditional_function()
    return render_template("Done.html")