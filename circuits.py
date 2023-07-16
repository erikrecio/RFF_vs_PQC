import pennylane as qml
import numpy as np

class Simple_circuit_marked:

    name = "simple_circuit_marked"

    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = 1
        self.dim_w = 2
        self.n_qubits = 2
        self.layers_x = 0
        self.layers_p = 0

    def circuit(self, w, x):
        qml.RX(x[0], wires=0, id="x0")
        qml.RY(x[0], wires=1, id="x0")
        qml.Rot(w[0], w[1], 0, wires=0)
        qml.CNOT(wires=[1, 0])
        return qml.expval(qml.PauliZ(0))


class Circuit_with_weights:

    name = "circuit_with_weights"

    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = 3
        self.dim_w = 6
        self.n_qubits = 2
        self.layers_x = 0
        self.layers_p = 0

    def circuit(self, w, x):
        qml.RX(x[0], wires=0, id="x0")
        qml.RY(x[1], wires=1, id="x1")
        qml.CNOT(wires=[1, 0])

        qml.Rot(w[0], w[1], w[2], wires=0)
        qml.Rot(w[3], w[4], w[5], wires=1)
        qml.CNOT(wires=[1, 0])

        qml.RX(x[0], wires=0, id="x0")
        # qml.RY(x[1], wires=1, id="x1")
        qml.RX(x[2], wires=0, id="x2")
        qml.CNOT(wires=[1, 0])

        return qml.expval(qml.PauliZ(0))


class Circuit_1:

    name = "circuit_1"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 3*n_qubits
        self.n_qubits = n_qubits
        self.layers_x = n_qubits//dim_x
        self.layers_p = 1

    def circuit(self, w, x):

        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")

        for i in range(self.n_qubits):
            qml.Rot(w[3*i], w[3*i+1], w[3*i+2], wires=i)

        for i in range(self.n_qubits):
            if self.n_qubits-i-1 != 0:
                qml.CNOT(wires=[i,i+1])
            else:
                qml.CNOT(wires=[i,0])

        return qml.expval(qml.PauliZ(0))


class Circuit_2:

    name = "circuit_2"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 6*n_qubits
        self.n_qubits = n_qubits
        self.layers_x = n_qubits//dim_x
        self.layers_p = 1

    def circuit(self, w, x):
        
        for i in range(self.n_qubits):
            qml.Rot(w[3*i], w[3*i+1], w[3*i+2], wires=i)

        for i in range(self.n_qubits):
            if self.n_qubits-i-1 != 0:
                qml.CNOT(wires=[i,i+1])
            else:
                qml.CNOT(wires=[i,0])


        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")


        for i in range(self.n_qubits):
            qml.Rot(w[3*self.n_qubits+3*i], w[3*self.n_qubits+3*i+1], w[3*self.n_qubits+3*i+2], wires=i)

        for i in range(self.n_qubits):
            if self.n_qubits-i-1 != 0:
                qml.CNOT(wires=[i,i+1])
            else:
                qml.CNOT(wires=[i,0])

        return qml.expval(qml.PauliZ(0))



class Circuit_3:

    name = "circuit_3"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 3*n_qubits
        self.n_qubits = n_qubits
        self.layers_x = layers_x
        self.layers_p = 1

    def circuit(self, w, x):
        
        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")
            if i+1 == self.layers_x*self.dim_x:
                break


        for i in range(self.n_qubits):
            qml.Rot(w[3*i], w[3*i+1], w[3*i+2], wires=i)

        for i in range(self.n_qubits):
            if self.n_qubits-i-1 != 0:
                qml.CNOT(wires=[i,i+1])
            else:
                qml.CNOT(wires=[i,0])


        return qml.expval(qml.PauliZ(0))
    

class Circuit_1qubit:

    name = "circuit_1qubit"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 3*(layers_x*dim_x + 1)
        self.n_qubits = 1
        self.layers_x = layers_x
        self.layers_p = 1

    def circuit(self, w, x):
        
        qml.Rot(w[0], w[1], w[2], wires=0)
        pos = 3
        for l in range(self.layers_x):
            for d in range(self.dim_x):
                qml.RX(x[d], wires=0, id=f"x{d}")
                qml.Rot(w[pos], w[pos+1], w[pos+2], wires=0)
                pos += 3

        return qml.expval(qml.PauliZ(0))


class Circuit_big:

    name = "circuit_big"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 6*n_qubits*layers_p
        self.n_qubits = n_qubits
        self.layers_x = layers_x
        self.layers_p = layers_p

    def circuit(self, w, x):
        
        for j in range(self.layers_p):

            for i in range(self.n_qubits):
                qml.Rot(w[3*i+3*j*self.n_qubits], w[3*i+1+3*j*self.n_qubits], w[3*i+2+3*j*self.n_qubits], wires=i)

            for i in range(self.n_qubits):
                if self.n_qubits-i-1 != 0:
                    qml.CNOT(wires=[i,i+1])
                else:
                    qml.CNOT(wires=[i,0])


        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")
            if i+1 == self.layers_x*self.dim_x:
                break

        
        for j in range(self.layers_p):

            for i in range(self.n_qubits):
                qml.Rot(w[3*self.n_qubits*self.layers_p+3*i+3*j*self.n_qubits], w[3*self.n_qubits*self.layers_p+3*i+1+3*j*self.n_qubits], w[3*self.n_qubits*self.layers_p+3*i+2+3*j*self.n_qubits], wires=i)

            for i in range(self.n_qubits):
                if self.n_qubits-i-1 != 0:
                    qml.CNOT(wires=[i,i+1])
                else:
                    qml.CNOT(wires=[i,0])

        return qml.expval(qml.PauliZ(0))
    
    

class Circuit_one_p:

    name = "circuit_one_p"
    
    def __init__(self, n_qubits, dim_x, layers_x, layers_p):
        self.dim_x = dim_x
        self.dim_w = 1
        self.n_qubits = n_qubits
        self.layers_x = layers_x
        self.layers_p = 1

    def circuit(self, w, x):

        qml.RY(w[0], wires=0)
        
        for i in range(self.n_qubits):
            qml.RX(x[i % self.dim_x], wires=i, id=f"x{i % self.dim_x}")
            if i+1 == self.layers_x*self.dim_x:
                break

        
        return qml.expval(qml.PauliZ(0))