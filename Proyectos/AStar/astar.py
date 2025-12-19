import pygame
import math
from queue import PriorityQueue

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("A* Pathfinding Visualizer")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 50,50)
AZUL = (0, 0, 255)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
TURQUESA = (64, 224, 208)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.vecinos = []
        self.ancho = ancho
        self.total_filas = total_filas

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self): return self.color == NEGRO
    def es_inicio(self): return self.color == NARANJA
    def es_fin(self): return self.color == PURPURA
    def restablecer(self): self.color = BLANCO
    def hacer_inicio(self): self.color = NARANJA
    def hacer_pared(self): self.color = NEGRO
    def hacer_fin(self): self.color = PURPURA
    def hacer_cerrado(self): self.color = ROJO
    def hacer_abierto(self): self.color = VERDE
    def hacer_camino(self): self.color = TURQUESA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        # ABAJO
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila + 1][self.col])
        # ARRIBA
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append(grid[self.fila - 1][self.col])
        # DERECHA
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col + 1])
        # IZQUIERDA
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append(grid[self.fila][self.col - 1])

        # --- MOVIMIENTOS DIAGONALES (Anti-Corte de Esquinas) ---
        # ABAJO-DERECHA
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1:
            if not grid[self.fila + 1][self.col + 1].es_pared():
                # No permite pasar si hay dos paredes bloqueando la esquina
                if not grid[self.fila + 1][self.col].es_pared() or not grid[self.fila][self.col + 1].es_pared():
                    self.vecinos.append(grid[self.fila + 1][self.col + 1])
        
        # ABAJO-IZQUIERDA
        if self.fila < self.total_filas - 1 and self.col > 0:
            if not grid[self.fila + 1][self.col - 1].es_pared():
                if not grid[self.fila + 1][self.col].es_pared() or not grid[self.fila][self.col - 1].es_pared():
                    self.vecinos.append(grid[self.fila + 1][self.col - 1])

        # ARRIBA-DERECHA
        if self.fila > 0 and self.col < self.total_filas - 1:
            if not grid[self.fila - 1][self.col + 1].es_pared():
                if not grid[self.fila - 1][self.col].es_pared() or not grid[self.fila][self.col + 1].es_pared():
                    self.vecinos.append(grid[self.fila - 1][self.col + 1])

        # ARRIBA-IZQUIERDA
        if self.fila > 0 and self.col > 0:
            if not grid[self.fila - 1][self.col - 1].es_pared():
                if not grid[self.fila - 1][self.col].es_pared() or not grid[self.fila][self.col - 1].es_pared():
                    self.vecinos.append(grid[self.fila - 1][self.col - 1])

    def limpiar_rastro(self):
        # Solo restablece si no es pared, inicio o fin
        if self.color not in [NEGRO, NARANJA, PURPURA]:
            self.color = BLANCO

# Función heurística (Distancia Manhattan)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruir_camino(vino_de, actual, dibujar):
    while actual in vino_de:
        actual = vino_de[actual]
        actual.hacer_camino()
        dibujar()

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    contador = 0
    open_set = PriorityQueue()
    open_set.put((0, contador, inicio))
    vino_de = {}
    
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = h(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        actual = open_set.get()[2]
        open_set_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(vino_de, fin, dibujar)
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True

        for vecino in actual.vecinos:
            temp_g_score = g_score[actual] + 1

            if temp_g_score < g_score[vecino]:
                vino_de[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + h(vecino.get_pos(), fin.get_pos())
                if vecino not in open_set_hash:
                    contador += 1
                    open_set.put((f_score[vecino], contador, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_abierto()

        dibujar()
        if actual != inicio:
            actual.hacer_cerrado()

    return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    FILAS = 12  # Aumentado para mejor visualización
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None
    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio: inicio = None
                elif nodo == fin: fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.limpiar_rastro()
                            nodo.actualizar_vecinos(grid)
                    
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

                if event.key == pygame.K_r: # Limpiar todo con la tecla R
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

                if event.key == pygame.K_c: # Limpiar todo con la tecla C
                    for fila in grid:
                        for nodo in fila:
                            nodo.limpiar_rastro()
                            nodo.actualizar_vecinos(grid)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)