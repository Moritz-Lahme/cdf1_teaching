"""
Geometry basics -- reusable Rhino.Geometry functions for Grasshopper.

Adding a new function with Copilot
-----------------------------------
1. Open this file and select this chat model, then ask Copilot something like:
   "Add a function here, all in Rhino geometry, that builds a <your shape/idea>.
   Follow the same style as create_cone / create_fractal_tree (defaults for
   optional inputs, a docstring listing params, return a Rhino.Geometry object)."
2. Once the function is added, ask Copilot:
   "Give me the Python code to use this function in a Grasshopper GHPython 3
   component, importing it from computational_design_and_fabrication."
3. Copy the snippet Copilot gives you into a GHPython component, wire up the
   inputs as sliders/panels, and set the output variable (e.g. `a`).
"""

import math
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs

def create_cone(base_point=None, height=10.0, radius=5.0, cap_bottom=True):
    """
    Build a cone as a Brep.

    base_point : Rhino.Geometry.Point3d -- center of the cone's base circle
    height     : float -- cone height along the base plane's normal (Z by default)
    radius     : float -- base circle radius
    cap_bottom : bool  -- whether to cap the base circle (closed vs open cone)

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    cone = rg.Cone(plane, height, radius)
    return cone.ToBrep(cap_bottom)

def create_cylinder(base_point=None, height=10.0, radius=5.0, cap=True):
    """
    Build a cylinder as a Brep.

    base_point : Rhino.Geometry.Point3d -- center of the cylinder base
    height     : float -- cylinder height along the Z axis
    radius     : float -- cylinder radius
    cap        : bool -- whether to cap both ends of the cylinder

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if height is None:
        height = 10.0
    if radius is None:
        radius = 5.0
    if height <= 0:
        raise ValueError("height must be greater than zero.")
    if radius <= 0:
        raise ValueError("radius must be greater than zero.")

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    cylinder = rg.Cylinder(rg.Circle(plane, radius), height)
    return cylinder.ToBrep(cap, cap)

def create_sphere(base_point=None, radius=5.0):
    """
    Build a sphere as a Brep.

    base_point : Rhino.Geometry.Point3d -- center of the sphere
    radius     : float -- sphere radius

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    sphere = rg.Sphere(base_point, radius)
    return sphere.ToBrep()

def create_cube(base_point=None, x_size=5.0, y_size=5.0, z_size=5.0):
    """
    Build a rectangular cube-like box as a Brep.

    base_point : Rhino.Geometry.Point3d -- lower corner of the box
    x_size     : float -- box size in the X direction
    y_size     : float -- box size in the Y direction
    z_size     : float -- box size in the Z direction

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if x_size is None:
        x_size = 5.0
    if y_size is None:
        y_size = 5.0
    if z_size is None:
        z_size = 5.0
    if x_size <= 0 or y_size <= 0 or z_size <= 0:
        raise ValueError("x_size, y_size, and z_size must be greater than zero.")

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    box = rg.Box(
        plane,
        rg.Interval(0, x_size),
        rg.Interval(0, y_size),
        rg.Interval(0, z_size)
    )
    return box.ToBrep()

def move_brep(brep, move_x=0.0, move_y=0.0, move_z=0.0):
    """
    Return a translated copy of a Brep.

    brep   : Rhino.Geometry.Brep -- the Brep to move
    move_x : float -- translation distance along the X axis
    move_y : float -- translation distance along the Y axis
    move_z : float -- translation distance along the Z axis

    Returns a translated copy of the Rhino.Geometry.Brep.
    """
    if brep is None:
        raise ValueError("brep must be provided.")

    brep = rs.coercebrep(brep)
    if brep is None:
        raise TypeError("brep must be a Rhino Brep or a Brep object reference.")

    if move_x is None:
        move_x = 0.0
    if move_y is None:
        move_y = 0.0
    if move_z is None:
        move_z = 0.0

    moved_brep = brep.DuplicateBrep()
    moved_brep.Transform(
        rg.Transform.Translation(
            rg.Vector3d(move_x, move_y, move_z)
        )
    )
    return moved_brep

def mirror_brep(brep, mirror_plane=None):
    """
    Return a mirrored copy of a Brep.

    brep         : Rhino.Geometry.Brep -- the Brep to mirror
    mirror_plane : Rhino.Geometry.Plane -- plane used for mirroring;
                   the world XY plane by default

    Returns a mirrored copy of the Rhino.Geometry.Brep.
    """
    if brep is None:
        raise ValueError("brep must be provided.")

    brep = rs.coercebrep(brep)
    if brep is None:
        raise TypeError("brep must be a Rhino Brep or a Brep object reference.")

    if mirror_plane is None:
        mirror_plane = rg.Plane.WorldXY
    else:
        mirror_plane = rs.coerceplane(mirror_plane)
        if mirror_plane is None:
            raise TypeError("mirror_plane must be a Rhino Plane or a plane object reference.")

    mirrored_brep = brep.DuplicateBrep()
    mirrored_brep.Transform(rg.Transform.Mirror(mirror_plane))
    return mirrored_brep

def rotate_brep(brep, angle_x=0.0, angle_y=0.0, center=None):
    """
    Return a rotated copy of a Brep around the X and Y axes.

    brep    : Rhino.Geometry.Brep -- the Brep to copy and rotate
    angle_x : float -- rotation angle around the X axis in degrees
    angle_y : float -- rotation angle around the Y axis in degrees
    center  : Rhino.Geometry.Point3d -- rotation center; Brep center by default

    Returns a rotated copy of the input Brep. The input Brep is unchanged.
    """
    if brep is None:
        raise ValueError("brep must be provided.")
    brep = rs.coercebrep(brep)
    if brep is None:
        raise TypeError("brep must be a Rhino Brep or a Brep object reference.")

    if center is None:
        center = brep.GetBoundingBox(True).Center
    else:
        center = rs.coerce3dpoint(center)
        if center is None:
            raise TypeError("center must be a Rhino Point3d or a point object reference.")

    rotated_brep = brep.DuplicateBrep()
    if angle_x:
        rotated_brep.Transform(
            rg.Transform.Rotation(
                math.radians(angle_x), rg.Vector3d.XAxis, center
            )
        )
    if angle_y:
        rotated_brep.Transform(
            rg.Transform.Rotation(
                math.radians(angle_y), rg.Vector3d.YAxis, center
            )
        )
    return rotated_brep


def create_torus(base_point=None, major_radius=8.0, minor_radius=2.0):
    """
    Build a torus as a Brep, centered on the same point as a sphere.

    base_point   : Rhino.Geometry.Point3d -- center of the torus
    major_radius : float -- distance from the torus center to the tube center
    minor_radius : float -- radius of the torus tube

    Returns a Rhino.Geometry.Brep.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if major_radius is None:
        major_radius = 2.0
    if minor_radius is None:
        minor_radius = 1.0

    if major_radius <= 0:
        raise ValueError("major_radius must be greater than zero.")
    if minor_radius <= 0:
        raise ValueError("minor_radius must be greater than zero.")
    if major_radius <= minor_radius:
        raise ValueError("major_radius must be greater than minor_radius.")

    plane = rg.Plane(base_point, rg.Vector3d.ZAxis)
    torus = rg.Torus(plane, major_radius, minor_radius)
    return torus.ToBrep()

def create_grid(base_point=None, x_count=10, y_count=10,
                x_spacing=1.0, y_spacing=1.0):
    """
    Build a rectangular grid of line curves in the XY plane.

    base_point : Rhino.Geometry.Point3d -- lower-left corner of the grid
    x_count    : int -- number of spaces in the X direction
    y_count    : int -- number of spaces in the Y direction
    x_spacing  : float -- distance between grid lines in the X direction
    y_spacing  : float -- distance between grid lines in the Y direction

    Returns a list of Rhino.Geometry.LineCurve objects.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if x_count is None:
        x_count = 10
    if y_count is None:
        y_count = 10
    if x_spacing is None:
        x_spacing = 1.0
    if y_spacing is None:
        y_spacing = 1.0

    x_count = int(x_count)
    y_count = int(y_count)
    if x_count < 1:
        raise ValueError("x_count must be at least 1.")
    if y_count < 1:
        raise ValueError("y_count must be at least 1.")
    if x_spacing <= 0:
        raise ValueError("x_spacing must be greater than zero.")
    if y_spacing <= 0:
        raise ValueError("y_spacing must be greater than zero.")

    grid = []
    x_length = x_count * x_spacing
    y_length = y_count * y_spacing

    for y in range(y_count + 1):
        y_position = base_point.Y + y * y_spacing
        start = rg.Point3d(base_point.X, y_position, base_point.Z)
        end = rg.Point3d(base_point.X + x_length, y_position, base_point.Z)
        grid.append(rg.LineCurve(start, end))

    for x in range(x_count + 1):
        x_position = base_point.X + x * x_spacing
        start = rg.Point3d(x_position, base_point.Y, base_point.Z)
        end = rg.Point3d(x_position, base_point.Y + y_length, base_point.Z)
        grid.append(rg.LineCurve(start, end))

    return grid

def create_grid_centers(base_point=None, x_count=10, y_count=10,
                        x_spacing=1.0, y_spacing=1.0):
    """
    Build center points for every rectangular field in an XY grid.

    base_point : Rhino.Geometry.Point3d -- lower-left corner of the grid
    x_count    : int -- number of fields in the X direction
    y_count    : int -- number of fields in the Y direction
    x_spacing  : float -- width of each field in the X direction
    y_spacing  : float -- height of each field in the Y direction

    Returns a list of Rhino.Geometry.Point3d objects.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if x_count is None:
        x_count = 10
    if y_count is None:
        y_count = 10
    if x_spacing is None:
        x_spacing = 1.0
    if y_spacing is None:
        y_spacing = 1.0

    x_count = int(x_count)
    y_count = int(y_count)
    if x_count < 1:
        raise ValueError("x_count must be at least 1.")
    if y_count < 1:
        raise ValueError("y_count must be at least 1.")
    if x_spacing <= 0:
        raise ValueError("x_spacing must be greater than zero.")
    if y_spacing <= 0:
        raise ValueError("y_spacing must be greater than zero.")

    centers = []
    for y in range(y_count):
        for x in range(x_count):
            centers.append(
                rg.Point3d(
                    base_point.X + (x + 0.5) * x_spacing,
                    base_point.Y + (y + 0.5) * y_spacing,
                    base_point.Z
                )
            )

    return centers

def select_grid_center(base_point=None, x_count=10, y_count=10,
                       x_spacing=1.0, y_spacing=1.0,
                       x_index=0, y_index=0):
    """
    Select one center point from a rectangular XY grid.

    base_point : Rhino.Geometry.Point3d -- lower-left corner of the grid
    x_count    : int -- number of fields in the X direction
    y_count    : int -- number of fields in the Y direction
    x_spacing  : float -- width of each field in the X direction
    y_spacing  : float -- height of each field in the Y direction
    x_index    : int -- zero-based field index in the X direction
    y_index    : int -- zero-based field index in the Y direction

    Returns a Rhino.Geometry.Point3d.
    """
    if base_point is None:
        base_point = rg.Point3d(0, 0, 0)
    else:
        base_point = rs.coerce3dpoint(base_point)
        if base_point is None:
            raise TypeError("base_point must be a Rhino Point3d or a point object reference.")

    if x_count is None:
        x_count = 10
    if y_count is None:
        y_count = 10
    if x_spacing is None:
        x_spacing = 1.0
    if y_spacing is None:
        y_spacing = 1.0
    if x_index is None:
        x_index = 0
    if y_index is None:
        y_index = 0

    x_count = int(x_count)
    y_count = int(y_count)
    x_index = int(x_index)
    y_index = int(y_index)

    if x_count < 1:
        raise ValueError("x_count must be at least 1.")
    if y_count < 1:
        raise ValueError("y_count must be at least 1.")
    if x_spacing <= 0:
        raise ValueError("x_spacing must be greater than zero.")
    if y_spacing <= 0:
        raise ValueError("y_spacing must be greater than zero.")
    if not 0 <= x_index < x_count:
        raise IndexError("x_index must be between 0 and x_count - 1.")
    if not 0 <= y_index < y_count:
        raise IndexError("y_index must be between 0 and y_count - 1.")

    return rg.Point3d(
        base_point.X + (x_index + 0.5) * x_spacing,
        base_point.Y + (y_index + 0.5) * y_spacing,
        base_point.Z
    )

def boolean_difference(brep_a, brep_b):
    """
    Perform a boolean difference operation between two Breps.

    brep_a : Rhino.Geometry.Brep -- the first Brep
    brep_b : Rhino.Geometry.Brep -- the second Brep to subtract from the first

    Returns a list of Rhino.Geometry.Brep resulting from the difference.
    """
    if brep_a is None or brep_b is None:
        raise ValueError("Both brep_a and brep_b must be provided.")

    brep_a = rs.coercebrep(brep_a)
    if brep_a is None:
        raise TypeError("brep_a must be a Rhino Brep or a Brep object reference.")

    brep_b = rs.coercebrep(brep_b)
    if brep_b is None:
        raise TypeError("brep_b must be a Rhino Brep or a Brep object reference.")

    result = rg.Brep.CreateBooleanDifference([brep_a], [brep_b], 0.001)
    return result


def copy_brep_along_z(brep, distance, copy_count):
    """
    Create copies of a Brep, each offset in the +Z direction.

    brep : Rhino.Geometry.Brep -- the Brep to copy
    distance : float -- the Z spacing between consecutive copies
    copy_count : int -- the number of copies to create

    Returns a list of Rhino.Geometry.Brep copies; copy i is moved by distance * (i + 1).
    """
    if brep is None:
        raise ValueError("brep must be provided.")
    if copy_count < 0:
        raise ValueError("copy_count must not be negative.")

    copies = []
    for i in range(1, int(copy_count) + 1):
        copy = brep.DuplicateBrep()
        copy.Transform(rg.Transform.Translation(rg.Vector3d(0, 0, distance * i)))
        copies.append(copy)
    return copies


