import numpy as np
import sys

class CoilGenerator:
    def __init__(self, h, g, w, d):
        self.h = h
        self.g = g
        self.w = w
        self.d = d

    def gen_nodes_2d(self):
        r = 0.1
        g_ = self.g + self.w
        l = 0.5 * (np.pi * self.d - g_)

        # Calculate nodes for one coil
        assert self.w < g_ and 2 * self.w < l and self.w < self.h

        nodes = [
            [g_, r * self.h],
            [g_, 0],
            [l, 0],
            [l, self.h],
            [0, self.h],
            [0, 0],
            [-l, 0],
            [-l, self.h],
            [-g_, self.h],
            [-g_, r * self.h]
        ]

        # Add extra horizontal nodes to replicate curves in 3D space
        n = 20  # Number of segments
        atbi = []

        for i, [x, y] in enumerate(nodes[:-1]):
            if i % 2 == 1:
                dx = (nodes[i + 1][0] - x) / n
                atbi.append([[x + (num) * dx, y] for num in np.arange(1, n)])

        atbi = [x for _ in atbi for x in _]
        q = len(atbi) // 4

        prod = [
            nodes[0:2], atbi[0:q],
            nodes[2:4], atbi[q:2 * q],
            nodes[4:6], atbi[2 * q:3 * q],
            nodes[6:8], atbi[3 * q:],
            nodes[8:10]
        ]
        prod = [x for _ in prod for x in _]
        return prod

    def proj2dto3d(self, nodes):
        r = self.d / 2
        return [[r * np.cos(x / r), r * np.sin(x / r), y] for [x, y] in nodes]

    def generate_script(self):
        nodes_2d = self.gen_nodes_2d()
        nodes_3d = self.proj2dto3d(nodes_2d)

        # Convert nodes to script
        script = "\n".join([f"N{i + 1} x={x} y={y} z={z}" for i, [x, y, z] in enumerate(nodes_3d)])

        # Break up the string
        script += "\n\n"

        # Generate segments
        script += "\n".join([f"E{i + 1} N{i + 1} N{i + 2} w=0.038 h=1 wx={x} wy={y} wz=0" for i, [x, y, z] in enumerate(nodes_3d[:-1])])

        script = """
.units mm
.Default sigma=5.80e4 \n
""" + script + """\n
.external N1 N{:}
.freq fmin=10e6 fmax=20e6 ndec=0.05

.end""".format(len(nodes_3d))

        return script

    def write_script_to_file(self, filename):
        script = self.generate_script()
        with open(filename, 'w') as f:
            f.write(script)


# Parameters /mm
h = 5  # Height
g = 1  # Actual gap between coils
w = 1  # Width of coil
d = 5  # Diameter of epr tube, i.e., diameter of coil

coil_generator = CoilGenerator(h, g, w, d)
coil_generator.write_script_to_file('test.inp')

