import sys
sys.path.append("../src")
from cryspy.fromstr import fromstr as fs
import cryspy.geo as geo
import cryspy.crystal as cr
import cryspy.niceprint


def test_print_atomtable():
    atomset = \
        cr.Atomset({cr.Atom("Dy1", "Dy", fs("p 0.982(0)    0.082(0)  1/4        ")),
                cr.Atom("Mn1", "Mn", fs("p 1/2         0         0          ")),
                cr.Atom("O1", "O", fs("p 0.108(2)    0.471(2)  1/4        ")),
                cr.Atom("O2", "O", fs("p 0.707(1)    0.328(1)  0.052(1)   "))})

    liste = ["Dy1", "Mn1", "O1", "O2"]
    assert cryspy_niceprint.atomtable(liste, atomset) == \
        "  name  type          x           y           z \n" \
        "  ----  ----         ---         ---         ---\n" \
        "   Dy1    Dy    0.982(0)    0.082(0)         1/4\n" \
        "   Mn1    Mn         1/2           0           0\n" \
        "    O1     O  0.1080(20)  0.4710(20)         1/4\n" \
        "    O2     O  0.7070(10)  0.3280(10)  0.0520(10)"


def test_print_cif():
    atomset = \
        cr.Atomset({cr.Atom("Dy1", "Dy", fs("p 0.982(0)    0.082(0)  1/4        ")),
                cr.Atom("Mn1", "Mn", fs("p 1/2         0         0          ")),
                cr.Atom("O1", "O", fs("p 0.108(2)    0.471(2)  1/4        ")),
                cr.Atom("O2", "O", fs("p 0.707(1)    0.328(1)  0.052(1)   "))})

    sg = geo.Spacegroup(geo.canonical, [fs("{x,y,z}"), fs("{-x,-y,-z}")])
    liste = ["Dy1", "Mn1", "O1", "O2"]

    atomset_all = (sg ** atomset) % geo.canonical

    assert cryspy_niceprint.print_cif_without_symmetries(liste, atomset_all) == "hallo"
