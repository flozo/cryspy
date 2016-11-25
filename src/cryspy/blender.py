from cryspy import geo
from cryspy import crystal
from cryspy.fromstr import fromstr as fs

def make_blender_script(atomset, metric, outfilename):
    assert isinstance(atomset, crystal.Atomset), \
        "atomset must be of type crystal.Atomset."
    assert isinstance(metric, geo.Metric), \
        "metric must be of type geo.Metric."
    assert isinstance(outfilename, str), \
        "outfilename must be of type str."

    outstr = "import bpy \n" \
             "\n"


    b = 0.02 # half axes-width in Angstroem
    t = metric.schmidttransformation
   
    pos = fs("p 1 0 0")
    x = float((t**pos).x())
    y = float((t**pos).y())
    z = float((t**pos).z())
    outstr += "bpy.ops.mesh.primitive_cube_add(location = (0,0,0))\n"
    outstr += "myaxis = bpy.context.object\n"
    outstr += "myaxis.data.vertices[0].co = (0.0, -%f, -%f)\n"%(b, b)
    outstr += "myaxis.data.vertices[1].co = (0.0, -%f,  %f)\n"%(b, b)
    outstr += "myaxis.data.vertices[2].co = (0.0,  %f, -%f)\n"%(b, b)
    outstr += "myaxis.data.vertices[3].co = (0.0,  %f,  %f)\n"%(b, b)
    outstr += "myaxis.data.vertices[4].co = (%f, %f, %f)\n"%(x, y - b, z - b)
    outstr += "myaxis.data.vertices[5].co = (%f, %f, %f)\n"%(x, y - b, z + b)
    outstr += "myaxis.data.vertices[6].co = (%f, %f, %f)\n"%(x, y + b, z - b)
    outstr += "myaxis.data.vertices[7].co = (%f, %f, %f)\n"%(x, y + b, z + b)

    pos = fs("p 0 1 0")
    x = float((t**pos).x())
    y = float((t**pos).y())
    z = float((t**pos).z())
    outstr += "bpy.ops.mesh.primitive_cube_add(location = (0,0,0))\n"
    outstr += "myaxis = bpy.context.object\n"
    outstr += "myaxis.data.vertices[0].co = (-%f, 0.0, -%f)\n"%(b, b)
    outstr += "myaxis.data.vertices[1].co = ( %f, 0.0, -%f)\n"%(b, b)
    outstr += "myaxis.data.vertices[2].co = (-%f, 0.0,  %f)\n"%(b, b)
    outstr += "myaxis.data.vertices[3].co = ( %f, 0.0,  %f)\n"%(b, b)
    outstr += "myaxis.data.vertices[4].co = (%f, %f, %f)\n"%(x - b, y, z - b)
    outstr += "myaxis.data.vertices[5].co = (%f, %f, %f)\n"%(x + b, y, z - b)
    outstr += "myaxis.data.vertices[6].co = (%f, %f, %f)\n"%(x - b, y, z + b)
    outstr += "myaxis.data.vertices[7].co = (%f, %f, %f)\n"%(x + b, y, z + b)

    pos = fs("p 0 0 1")
    x = float((t**pos).x())
    y = float((t**pos).y())
    z = float((t**pos).z())
    outstr += "bpy.ops.mesh.primitive_cube_add(location = (0,0,0))\n"
    outstr += "myaxis = bpy.context.object\n"
    outstr += "myaxis.data.vertices[0].co = (-%f, -%f, 0.0)\n"%(b, b)
    outstr += "myaxis.data.vertices[1].co = (-%f,  %f, 0.0)\n"%(b, b)
    outstr += "myaxis.data.vertices[2].co = ( %f, -%f, 0.0)\n"%(b, b)
    outstr += "myaxis.data.vertices[3].co = ( %f,  %f, 0.0)\n"%(b, b)
    outstr += "myaxis.data.vertices[4].co = (%f, %f, %f)\n"%(x - b, y - b, z)
    outstr += "myaxis.data.vertices[5].co = (%f, %f, %f)\n"%(x - b, y + b, z)
    outstr += "myaxis.data.vertices[6].co = (%f, %f, %f)\n"%(x + b, y - b, z)
    outstr += "myaxis.data.vertices[7].co = (%f, %f, %f)\n"%(x + b, y + b, z)


    outstr += "bpy.ops.mesh.primitive_cube_add(location=(0,0,0))\n"
    outstr += "bpy.ops.object.mode_set(mode='EDIT')\n"
    outstr += "bpy.ops.mesh.delete(type='VERT')\n"
    outstr += "bpy.ops.object.mode_set(mode='OBJECT')\n"
    outstr += "posobject = bpy.context.object\n"
    outstr += "posobject.name = 'Positions'\n"


    materialnumber = 0
    atomnumber = 0
    for atom in atomset.menge:
        atomnumber += 1
        materialnumber += 1
        x = float((t**atom.pos).x())
        y = float((t**atom.pos).y())
        z = float((t**atom.pos).z())
        outstr += "posobject.data.vertices.add(1)\n"
        outstr += "posobject.data.vertices[-1].co = (%f, %f, %f)\n"%(x, y, z)
        (spheresize, color) = size_and_color(atom.typ)
        outstr += "bpy.ops.mesh.primitive_ico_sphere_add(location=(%f, %f, %f), size=%f)\n"%(x, y, z, spheresize)
        outstr += "bpy.context.object.name = 'Atom%03i(%s)'\n"%(atomnumber, atom.name)
        outstr += "mat = bpy.data.materials.new('material.%03i')\n"%(materialnumber)
        outstr += "mat.diffuse_color = %s\n"%(color.__str__())
        outstr += "bpy.context.object.data.materials.append(mat)\n"

    outfile = open(outfilename, "w")
    outfile.write(outstr)
    outfile.close()

def size_and_color(atomtype):
    assert isinstance(atomtype, str), \
        "atomtype must be of type str."
    if atomtype == "Li":
        spheresize = 0.1
        color = (1.0, 1.0, 0.7)
    elif atomtype == "O":
        spheresize = 0.3
        color = (1.0, 0.0, 0.0)
    elif atomtype == "Ca":
        spheresize = 0.4
        color = (0.0, 0.0, 0.8)
    elif atomtype == "Mn":
        spheresize = 0.5
        color = (0.6, 0.0, 0.8)
    elif atomtype == "Fe":
        spheresize = 0.5
        color = (0.6, 0.4, 0.0)
    else:
        spheresize = 0.2
        color = (0.5, 0.5, 0.5)
    return (spheresize, color)