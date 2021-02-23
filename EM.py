import math
import numpy as np

global c
c = 3E8
global e0
e0 = 8.854187817E-12
global pi
pi = math.pi
global u0
u0 = 4 * pi * 1E-7


class magnetism:

    def __init__(self, Q=None, V=[0, 0, 0], L=0, I=None, R=None):
        self.charge = Q
        self.velocity = V
        if L > 0:
            self.isWire = True
        else:
            self.isWire = False
        self.current = I
        self.length = L
        self.radius = R

    @staticmethod
    def crossProduct(A, B):
        return list(np.cross(A, B))

    def field(self, r, rHat):
        VxR = self.crossProduct(self.velocity, rHat)
        i = (u0 * self.charge * VxR[0]) / (4 * math.pi * pow(r, 2))
        j = (u0 * self.charge * VxR[1]) / (4 * math.pi * pow(r, 2))
        k = (u0 * self.charge * VxR[2]) / (4 * math.pi * pow(r, 2))
        return [i, j, k]

    def force(self, particle, r, rHat):
        if self.isWire:
            return self.wireForce(particle, r)
        temp = magnetism.crossProduct(particle.velocity, self.field(r, rHat))
        force = [particle.charge * x for x in temp]
        return force

    # negative = repel; positive = attract
    def wireForce(self, wire, r):
        return (u0 * self.current * wire.current * self.length) / (2 * math.pi * r)

    def loopField(self, angle):
        constants = (u0*self.current)/(4*pi*self.radius)
        return constants*math.radians(angle)

if __name__ == '__main__':
    proton = magnetism(Q=6 * 1.602E-19, V=[2E8, 0, 0])
    proton2 = magnetism(Q=1.602E-19, V=[0, -2.5E8, 0])
    print(proton.field(2E-6, [math.cos(math.radians(30)), -math.sin(math.radians(30)), 0]))
    print(proton.force(proton2, 2E-6, [math.cos(math.radians(30)), -math.sin(math.radians(30)), 0]))
    wire = magnetism(L=1.5, I=-4)
    wire2 = magnetism(L=1.5, I=3)
    print(wire.wireForce(wire2, 2))
    curve = magnetism(I=4, R=.08)
    # doesn't work print(curve.loopField(360))
