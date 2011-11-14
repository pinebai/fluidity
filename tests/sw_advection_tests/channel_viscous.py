import os
import numpy
meshtemplate='''
Point(1) = {0, 0, 0, <dx>};
Extrude {0, 1, 0} {
  Point{1};Layers{<layers>};
}
Point(3) = {1, 0, 0, <dx>};
Extrude {0, 1, 0} {
  Point{3};Layers{<layers>};
}
Line(3)={1,3};
Line(4)={2,4};
Line Loop(5) = {4, -2, -3, 1};
Plane Surface(6) = {5};

Physical Line(1) = {1};
Physical Line(2) = {2};
Physical Line(3) = {4, 3};
Physical Surface(1) = {6};
Mesh.Optimize=1;
'''

meshtemplate_rot='''
Point(1) = {0, 0, 0, <dx>};
Extrude {0, 0, 1} {
  Point{1};Layers{<layers>};
}
Point(3) = {1, 0, 0, <dx>};
Extrude {0, 0, 1} {
  Point{3};Layers{<layers>};
}
Line(3)={1,3};
Line(4)={2,4};
Line Loop(5) = {4, -2, -3, 1};
Plane Surface(6) = {5};

Physical Line(1) = {1};
Physical Line(2) = {2};
Physical Line(3) = {4, 3};
Physical Surface(1) = {6};
Mesh.Optimize=1;
'''

def generate_meshfile(name,layers):


    file(name+".geo",'w').write(
        meshtemplate.replace('<dx>',str(1./layers)
                 ).replace('<layers>',str(layers)))

    os.system("gmsh -3 "+name+".geo")
    os.system("../../scripts/gmsh2triangle "+name+".msh")

def generate_meshfile_rot(name,layers):


    file(name+".geo",'w').write(
        meshtemplate_rot.replace('<dx>',str(1./layers)
                 ).replace('<layers>',str(layers)))

    os.system("gmsh -3 "+name+".geo")
    os.system("../../scripts/gmsh2triangle "+name+".msh")

def meshfile2tube(name):
    #same connectivity as flat mesh file
    os.system("cp "+name+".ele "+name+"_tube.ele")
    os.system("cp "+name+".edge "+name+"_tube.edge")

    inputfile = file(name+'.node', 'r')
    line = inputfile.readline().strip()
    assert('3 0 0' in line)
    columns = numpy.double(line.split())
    assert(all(columns[1:]==numpy.array([3,0,0])))
    nnodes = int(columns[0])
    print "Mesh has "+str(nnodes)+" nodes."

    outputfile = file(name+'_tube.node', 'w')
    outputfile.write(str(nnodes)+' 3 0 0'+'\n')
    for node in range(nnodes):
        line = numpy.double(inputfile.readline().strip().split())
        assert(line[0]==node+1)
        Xin = line[1:]
        z = 2*(Xin[1]-0.5)
        Xout = numpy.array([numpy.pi*
                            numpy.cos(2*numpy.pi*Xin[0])/numpy.pi,
                            numpy.pi*
                            numpy.sin(2*numpy.pi*Xin[0])/numpy.pi,z])
        outputfile.write(str(node+1)+' '+str(Xout[0])+
                         ' '+str(Xout[1])+' '+str(Xout[2])+'\n')
    outputfile.write('#Generated by meshfile2tube('+name+').\n')
    outputfile.close()
    inputfile.close()
    
