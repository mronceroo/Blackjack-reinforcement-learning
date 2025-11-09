# Blackjack Reinforcement Learning

Un proyecto en Python que implementa técnicas de aprendizaje por refuerzo (reinforcement learning) para jugar al Blackjack.

## Descripción general

Este repositorio contiene código para:

* Simular partidas de Blackjack.
* Aplicar algoritmos de aprendizaje por refuerzo (Q-learning) para que un agente aprenda la mejor política de juego.
* Evaluar el desempeño del agente frente a estrategias básicas.
* Analizar resultados, rendimientos y comportamientos emergentes del agente.

## Estructura del repositorio

```
/
├── notebooks/            # Notebooks de experimentación e informes
├── src/                  # Código fuente del entorno, agente y algoritmos
└── artifacts/            # Resultados, gráficos, modelos entrenados
```

* notebooks/: Contiene documentos tipo Jupyter que muestran los experimentos, visualizaciones y análisis.
* src/: Módulos Python con la implementación del entorno de juego, la clase agente, los algoritmos de RL, scripts de entrenamiento y evaluación.
* artifacts/: Carpeta para guardar datos generados, como pesos del agente entrenado, logs de entrenamiento y gráficos de rendimiento.

## Requisitos

* Python 3.x
* Librerías comunes: numpy, pandas, matplotlib, torch o tensorflow (si se usan extensiones de RL).
* (Opcional) Jupyter Notebook para explorar los notebooks.

## Instalación

Clonar el repositorio:

```
git clone https://github.com/mronceroo/Blackjack-reinforcement-learning.git
cd Blackjack-reinforcement-learning
```

Instalar dependencias:

```
pip install -r requirements.txt
```

## Ejecución

1. Navegar a la carpeta src y ejecutar el script de entrenamiento:

   ```
   python train_agent.py
   ```

   Esto entrenará un agente para jugar al Blackjack.

2. Evaluar la política aprendida:

   ```
   python evaluate_agent.py
   ```

3. Abrir los notebooks en la carpeta notebooks para visualizar resultados y análisis.

## Algoritmos implementados

* Monte Carlo Exploring Starts
* Q-Learning (tabla)
* Posible extensión: función valor aproximada o Deep Q-Learning

Cada agente interactúa con el entorno del juego, actualiza su política o función valor, y tras suficientes episodios produce una estrategia que busca maximizar la ganancia esperada.

## Resultados esperados

* Gráficos de rendimiento (ganancia acumulada frente a número de episodios).
* Comparaciones de políticas (agente frente a estrategia básica).
* Tablas de valores de estado (por ejemplo, suma del jugador, carta visible del crupier, presencia de ás flexible).
* Discusión sobre convergencia, exploración/explotación e impacto de hiperparámetros.

## Posibles extensiones

* Convertir el entorno en un entorno compatible con OpenAI Gym.
* Implementar Deep Q-Learning para manejar mayores espacios de estado.
* Usar políticas basadas en redes neuronales.
* Modificar reglas del juego (por ejemplo, múltiples barajas, división de pares, doble tras separación).
* Exportar la política aprendida para usarla en una interfaz de juego en tiempo real.

## Problemas comunes

* Exploración insuficiente: usar políticas epsilon-greedy o similares.
* Problemas de convergencia: monitorizar la evolución de la política y función valor.
* Verificar la correcta implementación de las reglas del Blackjack (tratamiento del ás, pagos, etc.).
* Ajustar el tamaño de la tabla de valores o la arquitectura de la red si se usa Deep RL.
