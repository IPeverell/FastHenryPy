import argparse
import numpy as np
import matplotlib.pyplot as plt
from os import getcwd

class CoilGenerator:
    def __init__(self, h, g, w, d, turns):
        self.h = h
        self.g = g
        self.w = w
        self.d = d
        self.turns = turns

    def gen_nodes_2d(self):
        r = 0.5
        g_ = self.g + self.w
        l = 0.5 * (np.pi * self.d - g_)

        
        assert self.w < g_ and 2*self.w*self.turns < l and self.w*self.turns < self.h
        
        # Calculate vertices for n turns
        nodes=[]
        for t in range(1,self.turns+1):
            nodes.append( [ (t-1)*g_, self.h/2-(t-1)*g_ ])
            nodes.append( [ l-(t-1)*g_, self.h/2-(t-1)*g_ ])
            nodes.append( [ l-(t-1)*g_, -self.h/2+(t-1)*g_ ])
            nodes.append( [ t*g_, -self.h/2 +(t-1)*g_ ])
        nodes.append([self.turns*g_,0])

        # Add extra horizontal nodes to replicate curves once projected to 3D space
        s = 30  # Number of segments per horizontal
        
        #create nested list of extra nodes
        atbi =[]
        for i,[x,y] in enumerate(nodes):
            if i %2==0 and i +1 != len(nodes):
                dx =(nodes[i+1][0] -x) /s
                dy = y - nodes[i+1][1]
                assert dy ==0,print("Error - not horizontal")
                atbi.append([[x+k*dx,y] for k in range(1,s)])

        #add in the extra nodes
        for index, atb in reversed(list(enumerate(atbi))):
            nodes.insert(2*index+1,atb)

        #flatten nested list:
        prod=[]
        for item in nodes:
            if isinstance(item[0],list):
                for subitem in item:
                    prod.append(subitem)
            else:
                prod.append(item)

        
        #invert through origin (symmetry)
        prod = [[-x,-y] for [x,y] in prod][::-1] +prod
        return prod

    def proj2dto3d(self, nodes):
        r = self.d / 2
        return [[r  * np.cos(x / r), r * np.sin(x / r), y] for [x, y] in nodes]

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
.freq fmin=1e6 fmax=30e6 ndec=30

.end""".format(len(nodes_3d))

        return script

    def write_script_to_file(self, filename):
        script = self.generate_script()
        with open(getcwd() +'/'+filename, 'w') as f:
            f.write(script)
    
    def plot_nodes(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        nodes_2d = self.gen_nodes_2d()
        nodes_3d = self.proj2dto3d(nodes_2d)

        x_vals = [x for x, _, _ in nodes_3d]
        y_vals = [y for _, y, _ in nodes_3d]
        z_vals = [z for _, _, z in nodes_3d]

        ax.plot(x_vals, y_vals, z_vals)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()




def main():
    parser = argparse.ArgumentParser(description='Generate coil script')
    parser.add_argument('h', type=float, help='height of coil')
    parser.add_argument('g', type=float, help='actual gap between coils')
    parser.add_argument('w', type=float, help='width of coil')
    parser.add_argument('d', type=float, help='diameter of epr tube (coil diameter)')
    parser.add_argument('turns', type=int, help='number of coil turns')

    parser.add_argument('filename', help='output filename')

    args = parser.parse_args()

    h = args.h
    g = args.g
    w = args.w
    d = args.d
    turns = args.turns
    filename = args.filename

    coil_generator = CoilGenerator(h, g, w, d, turns)
    coil_generator.write_script_to_file(filename)
    coil_generator.plot_nodes()

if __name__ == '__main__':
    main()

