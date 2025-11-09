import numpy as np
import random
from pathlib import Path
import yaml
from typing import List, Tuple

class Blackjack:
    def __init__(self, objetivo=21):
        """Clase que define el juego de Blackjack."""
        self.objetivo = objetivo
        self.reset()

    def reset(self):
        """Reinicia el juego."""
        self.total = 0
        self.jugando = True

    def pedir_carta(self) -> int:
        """Devuelve una carta aleatoria entre 1 y 10."""
        return random.randint(1, 10)

    def actualizar_estado(self, accion: int) -> Tuple[int, float, bool]:
        """
        Aplica la acción (1: pedir, 0: plantarse) y devuelve el nuevo estado y recompensa.
        :param accion: Acción tomada por el jugador.
        :return: Nuevo total, recompensa y estado del juego (jugando o no).
        """
        if accion == 1:  # Pedir carta
            carta = self.pedir_carta()
            self.total += carta
            if self.total > self.objetivo:
                self.jugando = False
                return self.total, -1, False  # Pierde
            return self.total, 0, True  # Continúa
        else:  # Plantarse
            self.jugando = False
            return self.total, None, False

class Maquina:
    def __init__(self, exploracion=0.2):
        """Inicializa al agente con una tabla de valores Q."""
        self.q_table = {}  # Tabla Q
        self.visitas = {}  # Contador de visitas
        self.exploracion = exploracion  # Probabilidad de explorar

    def _init_estado(self, estado: int):
        """Inicializa un estado en la Q-Table."""
        if estado not in self.q_table:
            self.q_table[estado] = {0: 0, 1: 0}  # 0: plantarse, 1: pedir
            self.visitas[estado] = {0: 0, 1: 0}

    def decidir_accion(self, estado: int) -> int:
        """Decide una acción basada en la política entrenada."""
        self._init_estado(estado)
        if estado < 15:  # No tiene sentido plantarse si el total es menor a 15
            return 1  # Forzar a pedir
        if np.random.rand() < self.exploracion:
            return random.choice([0, 1])  # Exploración
        return max(self.q_table[estado], key=self.q_table[estado].get)  # Explotación


    def actualizar_politica(self, episodio: List[Tuple[int, int, float]]):
        """Actualiza la Q-Table al final del episodio usando Monte Carlo."""
        retornos = 0
        visitados = set()

        for estado, accion, recompensa in reversed(episodio):
            retornos += recompensa
            if (estado, accion) not in visitados:
                self.visitas[estado][accion] += 1
                self.q_table[estado][accion] += (retornos - self.q_table[estado][accion]) / self.visitas[estado][accion]
                visitados.add((estado, accion))

    def guardar_politica(self, ruta: Path):
        """Guarda la política en un archivo YAML."""
        with open(ruta, "w") as archivo:
            yaml.dump(self.q_table, archivo)
        print(f"Política guardada en {ruta}")

    def cargar_politica(self, ruta: Path):
        """Carga la política desde un archivo YAML."""
        with open(ruta, "r") as archivo:
            self.q_table = yaml.load(archivo, Loader=yaml.FullLoader)
        print(f"Política cargada desde {ruta}")

class JuegoBlackjack:
    def __init__(self, agente: Maquina):
        """Clase para gestionar el entrenamiento y juego."""
        self.juego = Blackjack()
        self.agente = agente

    def entrenar(self, episodios: int = 1000):
        """Entrena al agente jugando múltiples episodios."""
        for i in range(episodios):
            self.juego.reset()
            historial = []
            estado = self.juego.total

            while self.juego.jugando:
                accion = self.agente.decidir_accion(estado)
                nuevo_estado, recompensa, jugando = self.juego.actualizar_estado(accion)
                recompensa = recompensa if recompensa is not None else 1 if nuevo_estado <= 21 else -1
                historial.append((estado, accion, recompensa))
                estado = nuevo_estado

            self.agente.actualizar_politica(historial)
            if i % 100 == 0:
                print(f"Episodio {i} completado.")

    def jugar_con_humano(self):
        """Permite que un humano juegue contra el agente entrenado."""
        self.juego.reset()
        print("¡Inicia la partida de Blackjack: Jugador Humano vs Máquina entrenada!\n")

        # Inicializamos los totales de los jugadores
        total_humano = 0
        total_maquina = 0

        # --- Turno del Jugador Humano ---
        print("--- Turno del Jugador Humano ---")
        jugando_humano = True
        while jugando_humano:
            print(f"Tu total actual: {total_humano}")
            accion = input("¿Pedir (1) o Plantarse (0)? ").strip()

            if accion == "1":
                carta = self.juego.pedir_carta()
                total_humano += carta
                print(f"Has recibido un {carta}. Total: {total_humano}")
                if total_humano > 21:
                    print("¡Te has pasado! La máquina gana.")
                    return
            elif accion == "0":
                print(f"Te plantas con un total de {total_humano}.")
                jugando_humano = False
            else:
                print("Opción inválida. Elige 1 (pedir) o 0 (plantarse).")

        # --- Turno de la Máquina ---
        print("\n--- Turno de la Máquina ---")
        while True:
            print(f"Total actual de la máquina: {total_maquina}")
            if total_maquina < 14:  # Regla básica: si el total es bajo, pedir siempre
                accion_maquina = 1
            else:
                accion_maquina = self.agente.decidir_accion(total_maquina)
        
            if accion_maquina == 1:  # Pedir carta
                carta = self.juego.pedir_carta()
                total_maquina += carta
                print(f"La máquina pide y recibe un {carta}. Total de la máquina: {total_maquina}")
                if total_maquina > 21:
                    print("¡La máquina se ha pasado! Tú ganas.")
                    return
            else:  # Plantarse
                print(f"La máquina se planta con un total de {total_maquina}.")
                break


        # --- Comparar resultados ---
        print("\n--- Resultado Final ---")
        print(f"Tu total: {total_humano}")
        print(f"Total de la máquina: {total_maquina}")

        if total_humano > total_maquina:
            print("¡Felicidades! Tú ganas.")
        elif total_maquina > total_humano:
            print("La máquina gana. Mejor suerte la próxima vez.")
        else:
            print("¡Es un empate!")
        
    def evaluacion(self, episodios: 1000) -> float:
        """
        Evalúa al agente jugando múltiples partidas.
        :param juego: Instancia del juego Blackjack con el agente entrenado.
        :param episodios: Número de partidas de evaluación.
        :return: Porcentaje de victorias y número total de partidas.
        """
        victorias = 0
        for _ in range(episodios):
            self.juego.reset()  # Reinicia el juego
            total_agente = 0
            
            while True:
                accion = self.agente.decidir_accion(total_agente)  # Acción del agente
                if accion == 1:  # Pedir carta
                    carta = self.juego.pedir_carta()
                    total_agente += carta
                    if total_agente > self.juego.objetivo:  # Se pasó del objetivo
                        break
                else:  # Plantarse
                    break
                
            # Cuenta como victoria si no se pasa
            if total_agente <= self.juego.objetivo:
                victorias += 1
    
        porcentaje_victorias = (victorias / episodios) * 100
        return porcentaje_victorias
    