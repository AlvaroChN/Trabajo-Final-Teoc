from qiskit import QuantumCircuit, execute, Aer

class QuantumFiniteAutomaton:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.circuito = QuantumCircuit(num_qubits, num_qubits)

    def crear_qfa(self, cadena_binaria):
        # Check if the input string is a valid binary string
        if not set(cadena_binaria).issubset('01'):
            raise ValueError("La cadena debe ser binaria")

        # Check if the length of the binary string matches the number of qubits
        if len(cadena_binaria) != self.num_qubits:
            raise ValueError("La longitud de la cadena debe ser igual al número de qubits")

        # Aplica una puerta X a cada qubit si el bit correspondiente es 1 y
        # Aplica una puerta Hadamard a cada qubit para ponerlos en superposición
        for i, bit in enumerate(cadena_binaria):
            if bit == '1':
                self.circuito.x(i)
            self.circuito.h(i)

        # Aplica una puerta CNOT a pares de qubits para entrelazarlos
        for i in range(self.num_qubits - 1):
            self.circuito.cx(i, i + 1)

        # Mide los qubits
        self.circuito.measure(range(self.num_qubits), range(self.num_qubits))

    def ejecutar_qfa(self):
        # Ejecuta el circuito en un simulador
        resultado = execute(self.circuito, Aer.get_backend('qasm_simulator')).result()

        # Obtiene los conteos de los resultados de la medición
        conteos = resultado.get_counts()

        # El QFA acepta la cadena si la mayoría de las mediciones dan 0
        return conteos.get('0' * self.num_qubits, 0) > sum(conteos.values()) / 2

# Solicita al usuario que ingrese las cadenas binarias
cadenas_binarias = input("Por favor, ingresa las cadenas binarias separadas por comas: ").split(',')

# Prueba el QFA con las cadenas binarias ingresadas por el usuario
qfa = QuantumFiniteAutomaton(len(cadenas_binarias[0].strip()))
for cadena_binaria in cadenas_binarias:
    qfa.crear_qfa(cadena_binaria.strip())
    print(f"La cadena {cadena_binaria.strip()} es aceptada: {qfa.ejecutar_qfa()}")
