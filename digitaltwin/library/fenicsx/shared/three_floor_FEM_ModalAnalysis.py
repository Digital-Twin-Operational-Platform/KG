# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:40:01 2024

@author: xshen
"""



import sys

from mpi4py import MPI

import numpy as np
# from analytical_modes import verify_mode

import ufl
# from basix.ufl import element, mixed_element
from dolfinx import mesh, fem, plot,default_scalar_type   #, XDMFFile
from dolfinx.fem import locate_dofs_geometrical, Constant, FunctionSpace, form, locate_dofs_topological, dirichletbc
from dolfinx.fem.petsc import assemble_matrix
from dolfinx.mesh import CellType, create_rectangle, exterior_facet_indices, locate_entities, create_box, locate_entities_boundary
from dolfinx.plot import vtk_mesh
from dolfinx.io import XDMFFile

from dolfinx.fem import Function, functionspace #, VectorFunctionSpace

try:
    import pyvista
    have_pyvista = True
except ModuleNotFoundError:
    print("pyvista and pyvistaqt are required to visualise the solution")
    have_pyvista = False

try:
    from slepc4py import SLEPc
except ModuleNotFoundError:
    print("slepc4py is required for this demo")
    sys.exit(0)


from petsc4py import PETSc

import time


import os

# Get the current working directory
current_directory = os.getcwd()

# Print the current working directory
print("Current working directory:", current_directory)



#def FEM_output():
    # Specify the path to your .xdmf mesh file
#xdmf_file_path = './digitaltwin/Data/XDMF/Three_Floor_structure.xdmf'
xdmf_file_path = './shared/Three_Floor_structure.xdmf'

# Read the mesh in FEniCSx
with XDMFFile(MPI.COMM_WORLD, xdmf_file_path, "r") as xdmf:
    mesh_ = xdmf.read_mesh(name="Grid")
    mesh_.topology.create_connectivity(mesh_.topology.dim, mesh_.topology.dim-1)


print("mesh dimention:", mesh_.topology.dim)


E, nu = 70 *1e9, 0.3
rho = 2700
# Lame coefficient for constitutive relation
mu = E/2./(1+nu)
lambda_ = E*nu/(1+nu)/(1-2*nu)

domain = mesh_
# V = fem.VectorFunctionSpace(domain, ("Lagrange", 1))
#V = fem.functionspace(domain, ("CG", 2))
V = fem.functionspace(domain, ("Lagrange", 2, (mesh_.geometry.dim,)))
#####################################################################
#   Variational formulation
# Strain function
def epsilon(u):
    return ufl.sym(ufl.grad(u))  # Equivalent to 0.5*(ufl.nabla_grad(u) + ufl.nabla_grad(u).T)

#  Stress function
def sigma(u):
    print("1", ufl.div(u))
    print("2", ufl.Identity(len(u)))
    print("3", epsilon(u))
    return lambda_ * ufl.div(u) * ufl.Identity(len(u)) + 2 * mu * epsilon(u)


# Boundary condition

coordinates = mesh_.geometry.x
# Find the minimum z-coordinate
min_z = np.min(coordinates[:, 2])

# Mark the bottom boundary
x = ufl.SpatialCoordinate(mesh_)
fdim = mesh_.topology.dim - 1
bottom_facets = locate_entities_boundary(mesh_, fdim, marker=lambda y: np.isclose(y[2], min_z)) # min_z

dtype = PETSc.ScalarType  # type: ignore

################
# 1 BC
bc = dirichletbc(
    np.zeros(3, dtype=dtype), locate_dofs_topological(V, entity_dim=fdim, entities=bottom_facets), V=V
)

# As we want the traction over the remaining boundary to be 0
# T = fem.Constant(domain, default_scalar_type((0, 0, 0)))
#### 
# 2 BC
# def clamped_boundary(x):
#     return np.isclose(x[2], min_z)

# bc = dirichletbc(
#     np.zeros(3, dtype=dtype), locate_dofs_geometrical(V, clamped_boundary), V=V
# )
# u_D = Function(V)
# u_D.interpolate(lambda x: np.zeros_like(x))
# bc = dirichletbc(u_D, locate_dofs_topological(V, fdim, bottom_facets))

#### Constructing the K, and M matrix
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
a = ufl.inner(sigma(u), epsilon(v)) * ufl.dx
m = rho * ufl.inner(u, v) * ufl.dx

# A = assemble_matrix(fem.form(a), [])
# M = assemble_matrix(fem.form(m), [])
A = assemble_matrix(fem.form(a), bcs=[bc])
M = assemble_matrix(fem.form(m), bcs=[bc])
A.assemble()
M.assemble()
#####################################################################
#   Solve the linear variational problem
# Solve the eigenvalue problem
eps = SLEPc.EPS().create(MPI.COMM_WORLD)
eps.setOperators(A, M)
eps.setProblemType(SLEPc.EPS.ProblemType.GNHEP)
eps.setTolerances(tol=1e-9)
eps.setDimensions(nev=12)
eps.setTarget(-30)
st = eps.getST()
st.setType(SLEPc.ST.Type.SINVERT)
st.setShift(10)
eps.setWhichEigenpairs(SLEPc.EPS.Which.TARGET_REAL)
eps.setFromOptions()
eps.solve()

num_eigenvalues = eps.getConverged()
print(f"Number of converged eigenvalues: {num_eigenvalues}")

f_ = []
for i in range(num_eigenvalues):
    lambda_i = eps.getEigenvalue(i)
    freq_3D = np.sqrt(lambda_i)/2./np.pi
    #print(f"Eigenfreq {i}: {freq_3D}")
    f_.append(freq_3D)


# Identify the index of the first mode
index_ = []
for i, value in enumerate(f_):
    if value > 1.0:
        index_.append(i)
    
start_mode = index_[0]

for i in range(start_mode, num_eigenvalues):
    lambda_i = eps.getEigenvalue(i)
    freq_3D = np.sqrt(lambda_i)/2./np.pi
    print(f"Eigenfreq {i-start_mode+1}: {freq_3D}")

# eps.view()
# eps.errorView()
#####################################################################
#   visualisation
# pyvista.start_xvfb()
# pyvista.global_theme.cmap = 'jet'

# eh = fem.Function(V)  # Function to store eigenvectors
# kz_list = []        # List to store valid kz values


"""

# for i in range(6, num_eigenvalues):    # num_eigenvalues
#     vr, _ = A.createVecs()
#     # Extract the real part of the first eigenvector
#     eps.getEigenvector(i, vr)
#     # Create a DOLFINx function to represent the mode shape
#     mode_shape = fem.Function(V)
#     mode_shape.vector.ghostUpdate(addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD)
#     mode_shape.vector.setArray(vr.getArray())
    
#     error = eps.computeError(i, SLEPc.EPS.ErrorType.RELATIVE)
    
#     eigenfrequency = np.sqrt(np.abs(eps.getEigenvalue(i).real))/2./np.pi
#     # Verify, save and visualize solution
#     plotter = pyvista.Plotter()
    
#     topology, cell_types, geometry = vtk_mesh(V)
#     grid = pyvista.UnstructuredGrid(topology, cell_types, geometry)
#     # Attach the mode shape values to the grid. Since we directly work with the DOF values, there's no need for `compute_point_values`.
#     dof_coordinates = V.tabulate_dof_coordinates()
#     grid.point_data["mode_shape"] = mode_shape.vector.getArray()[2::3].real
#     # grid.point_data["mode_shape"] = mode_shape.vector.getArray().real
#     warped = grid.warp_by_scalar("mode_shape", factor=30)
#     grid.set_active_scalars("mode_shape")
#     plotter.add_mesh(warped,  scalars="mode_shape", show_edges=True)  #show_edges=True,
#     plotter.add_text(f"Mode {i+1}, Frequency: {eigenfrequency:.2f} Hz, Error: {error:.2e}", position='upper_left', font_size=10)
#     plotter.show()
    #######################################

for i in range(6, 7): #num_eigenvalues):    # num_eigenvalues
    vr, _ = A.createVecs()
    # Extract the real part of the first eigenvector
    eps.getEigenvector(i, vr)
    # Create a DOLFINx function to represent the mode shape
    mode_shape = fem.Function(V)
    mode_shape.vector.ghostUpdate(addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD)
    mode_shape.vector.setArray(vr.getArray())
    
    error = eps.computeError(i, SLEPc.EPS.ErrorType.RELATIVE)
    
    eigenfrequency = np.sqrt(np.abs(eps.getEigenvalue(i).real))/2./np.pi
    # Verify, save and visualize solution
    # plotter = pyvista.Plotter(window_size=(1200, 1500))
    plotter = pyvista.Plotter(window_size=(600, 900))
    
    topology, cell_types, geometry = vtk_mesh(V)
    grid = pyvista.UnstructuredGrid(topology, cell_types, geometry)
    num_dofs = geometry.shape[0]
    values = np.zeros((num_dofs, 3), dtype=np.float64)
    values[:, : mesh_.geometry.dim] = mode_shape.vector.getArray().reshape(num_dofs, V.dofmap.index_map_bs)
    grid["vectors"] = values
    warped = grid.warp_by_vector("vectors", factor=2)
    grid.set_active_vectors("vectors")
    sargs = dict(height=0.1, width=0.8, vertical=False, position_x=0.1, position_y=0, color="black")
    plotter.add_mesh(warped, show_edges=True, scalar_bar_args=sargs,)  #show_edges=True,
    
    # Attach the mode shape values to the grid. Since we directly work with the DOF values, there's no need for `compute_point_values`.
    # dof_coordinates = V.tabulate_dof_coordinates()
    # grid.point_data["mode_shape"] = mode_shape.vector.getArray()[2::3].real
    # grid.point_data["mode_shape"] = mode_shape.vector.getArray().real
    # warped = grid.warp_by_scalar("mode_shape", factor=30)
    # grid.set_active_scalars("mode_shape")
    # plotter.add_mesh(warped,  scalars="mode_shape", show_edges=True)  #show_edges=True,
    plotter.add_text(f"Mode {i+1}, Frequency: {eigenfrequency:.2f} Hz, Error: {error:.2e}", position='upper_left', font_size=10)
    plotter.show()



import os
# # import imageio
for i in range(15, 20):# num_eigenvalues):    # num_eigenvalues
    print(i)
    vr, _ = A.createVecs()
    # Extract the real part of the first eigenvector
    eps.getEigenvector(i, vr)
    # Create a DOLFINx function to represent the mode shape
    mode_shape = fem.Function(V)
    mode_shape.vector.ghostUpdate(addv=PETSc.InsertMode.INSERT, mode=PETSc.ScatterMode.FORWARD)
    mode_shape.vector.setArray(vr.getArray())
    
    error = eps.computeError(i, SLEPc.EPS.ErrorType.RELATIVE)
    num_time_steps = 30
    t = np.linspace(0, 2*np.pi, num_time_steps)
    eigenfrequency = np.sqrt(np.abs(eps.getEigenvalue(i).real))/2./np.pi
    
    topology, cell_types, geometry = vtk_mesh(V)
    grid = pyvista.UnstructuredGrid(topology, cell_types, geometry)
    num_dofs = geometry.shape[0]
    values = np.zeros((num_dofs, 3), dtype=np.float64)
    base_vector = mode_shape.vector.getArray()
    for time_step in range(num_time_steps):
        plotter = pyvista.Plotter(window_size=(1200, 1500))
        oscillating_vector = base_vector * np.sin(eigenfrequency * t[time_step])
        values[:, : mesh_.geometry.dim] = oscillating_vector.reshape(num_dofs, V.dofmap.index_map_bs)
        grid["vectors"] = values
        warped = grid.warp_by_vector("vectors", factor=2)
        grid.set_active_vectors("vectors")
        sargs = dict(height=0.1, width=0.8, vertical=False, position_x=0.1, position_y=0, color="black")
        plotter.add_mesh(warped, show_edges=True, scalar_bar_args=sargs)  #show_edges=True,
        plotter.add_text(f"Mode {i+1}, Frequency: {eigenfrequency:.2f} Hz, Error: {error:.2e}", position='upper_left', font_size=10)
        # plotter.write_frame()
        frame_filename = os.path.join(f"frame_{i:03d}_{time_step:03d}.png")  
        # frames.append(imageio.imread(frame_filename))
        plotter.screenshot(frame_filename)
        plotter.close()


# plotter.close()

# animation_filename = os.path.join(f"mode_{i+1}_animation.gif")
# imageio.mimsave(animation_filename, frames, fps=10)  # Adjust fps as needed
"""
