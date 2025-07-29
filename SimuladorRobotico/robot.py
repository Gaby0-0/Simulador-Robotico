import sim
import time
import math

class Robot:
    def __init__(self, ip='127.0.0.1', port=19999):
        sim.simxFinish(-1)  # cerrar conexiones previas
        self.clientID = sim.simxStart(ip, port, True, True, 5000, 5)
        self.joints = []
        self.grippers = []

        if self.clientID != -1:
            print("✅ Conectado a CoppeliaSim")
            self.obtener_joints()
        else:
            print("❌ No se pudo conectar a CoppeliaSim")

    def obtener_joints(self):
        joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        for name in joint_names:
            res, handle = sim.simxGetObjectHandle(self.clientID, name, sim.simx_opmode_blocking)
            if res == 0:
                self.joints.append(handle)
            else:
                self.joints.append(None)
                print(f"❌ No se encontró {name}")

        # Garra
        joint_names_gripper = ['gripperClose','gripperCenter']
        for nameGrippers in joint_names_gripper:
            res, gripper = sim.simxGetObjectHandle(self.clientID, nameGrippers , sim.simx_opmode_blocking)
            if res == 0:
                self.grippers.append(gripper)
            else:
                print("⚠️ No se encontró la garra")
    
    def obtener_angulos(self):
        try:
            base = sim.simxGetJointPosition(self.clientID, self.joints[0], sim.simx_opmode_blocking)[1]
            brazo = sim.simxGetJointPosition(self.clientID, self.joints[1], sim.simx_opmode_blocking)[1]
            codo = sim.simxGetJointPosition(self.clientID, self.joints[2], sim.simx_opmode_blocking)[1]
            garra = sim.simxGetJointPosition(self.clientID, self.joints[3], sim.simx_opmode_blocking)[1]

            # Convertir radianes a grados redondeados
            return {
                'base': round(math.degrees(base), 1),
                'brazo': round(math.degrees(brazo), 1),
                'codo': round(math.degrees(codo), 1),
                'garra': round(math.degrees(garra), 1)
            }
        except Exception as e:
            print("Error al obtener ángulos:", e)
            return None


    def mueveBase(self, a, v):
        angulo = float(a)
        velocidad = float(v)
        sim.simxSetJointTargetPosition(self.clientID,self.joints[0],math.radians(angulo), sim.simx_opmode_oneshot)
        time.sleep(velocidad )

    def mueveBrazo(self, a, v):
        angulo = float(a)
        velocidad = float(v)
        sim.simxSetJointTargetPosition(self.clientID,self.joints[1],math.radians(angulo), sim.simx_opmode_oneshot)
        time.sleep(velocidad)

    def mueveCodo(self, a, v):
        angulo = float(a)
        velocidad = float(v)
        sim.simxSetJointTargetPosition(self.clientID,self.joints[2],math.radians(angulo), sim.simx_opmode_oneshot)
        time.sleep(velocidad)
    
    def mueveGarra(self, a, v):
        angulo = float(a)
        velocidad = float(v)
        sim.simxSetJointTargetPosition(self.clientID,self.joints[3],math.radians(angulo), sim.simx_opmode_oneshot)
        time.sleep(velocidad)

     
        
    def ejecutar_ciclo(self, instrucciones, ciclos):

        for i in range(int(ciclos)):
            for instruccion in instrucciones:
                partes = instruccion.split(",")
                print(f"{partes[0]} {partes[1]} {partes[2]}")
                if partes[0] == "garra":
                    self.mueveGarra(partes[1], partes[2])
                if partes[0] == "brazo":
                    self.mueveBrazo(partes[1], partes[2])
                if partes[0] == "codo":
                    self.mueveCodo(partes[1], partes[2])
                if partes[0] == "base":
                    self.mueveBase(partes[1], partes[2])

    def cerrar(self):
        time.sleep(4)
        sim.simxFinish(self.clientID)
        print("🔚 Conexión cerrada")  