#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author : Moise Rousseau (2021), email at rousseau.moise@gmail.com


import time
from .ui import UI
import SMESH
import subprocess
import salome
import os


def export_mesh(mesh, f_out):
  out = open(f_out, 'w')
  #write node coordinates
  out.write("MeshVersionFormatted 2\n")
  out.write("Dimension 3\n\n")
  out.write("Vertices\n")
  n_nodes = mesh.NbNodes()
  out.write(f"{n_nodes}\n")
  for i in range(1,n_nodes+1):
    X,Y,Z = mesh.GetNodeXYZ(i)
    out.write("{} {} {} 1\n".format(X,Y,Z))
  #triangle
  n_tri = mesh.NbTriangles()
  if n_tri:
    out.write("\nTriangles\n")
    out.write(f"{n_tri}\n")
    for i in mesh.GetElementsByType(SMESH.FACE):
      if mesh.GetElementGeomType(i) == SMESH.Entity_Triangle:
        nodes = mesh.GetElemNodes(i)
        for node in nodes:
          out.write(f"{node} ")
        out.write("1\n")
  #quad
  n_quad = mesh.NbQuadrangles()
  if n_quad:
    out.write("\nQuadrilaterals\n")
    out.write(f"{n_quad}\n")
    for i in mesh.GetElementsByType(SMESH.FACE):
      if mesh.GetElementGeomType(i) == SMESH.Entity_Quadrangle:
        nodes = mesh.GetElemNodes(i)
        for node in nodes:
          out.write(f"{node} ")
        out.write("1\n")
  out.close()  
  return 0 #success

def import_mesh(mesh, f_in):
  #add vertices
  src = open(f_in, 'r')
  line = src.readline()
  while "Vertices" not in line:
    line = src.readline()
  n_vertices = int(src.readline())
  for i in range(n_vertices):
    X,Y,Z,j = [float(x) for x in src.readline().split()]
    mesh.AddNode(X,Y,Z)
  src.close()
  #add element
  src = open(f_in, 'r')
  line = src.readline()
  func = {"Triangles":mesh.AddFace, "Quadrilaterals":mesh.AddFace, "Tetrahedra":mesh.AddVolume}
  while line != "End\n":
    for elem in func.keys():
      if elem in line:
        n_elem = int(src.readline())
        for i in range(n_elem):
          nodes = [int(x) for x in src.readline().split()[:-1]]
          func[elem](nodes)
    line = src.readline()
  src.close()
  return 0
  


def Var_Tet_Mesher(context):

  window = UI(context)
  
  result = window.show()
  
  if result:
    t = time.time()
    smesh = salome.smesh.smeshBuilder.New()
    path = '/home/%s/.config/salome/Plugins/salome_var_tet_mesher/' %(os.getlogin())
  
    #get the mesh and export it
    print("\tExport boundary mesh")
    mesh = smesh.Mesh(window.mesh)
    export_mesh(mesh, path+'in.mesh')
    
    #get parameters
    n = window.le_penalization.text()
    it = window.le_it.text()
    command = ["./Var-Tet-Mesher", "in.mesh", "out.mesh", f"nb_pts={n}"]
    if it != "-1": 
      command.append(f"max_thread={it}")
    
    #optimize
    print("\tCall the mesher\n")
    res = subprocess.call(command, cwd=path)
    
    #import mesh
    print("\Import back the mesh\n")
    new_mesh = smesh.Mesh()
    import_mesh(new_mesh, path+"out.mesh")
    if salome.sg.hasDesktop():
      salome.sg.updateObjBrowser()
      
    print ("\n\tTotal time elapsed {} s".format(time.time() - t))
      
    print ("    END \n")
    print ("####################\n\n")

  return

