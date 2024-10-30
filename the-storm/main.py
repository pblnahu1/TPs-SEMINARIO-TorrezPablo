import random
import pygame
import config
from menu import menu
from menu import font_text
from clases import Jugador, Piedra, Obstaculo

# inicio pygame
pygame.init()

#creo la ventana
pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
pygame.display.set_caption("The storm")

# cargar imágenes y fuentes
jugador_img = pygame.image.load("img/persona-corriendo-adelante.png")
jugador_img = pygame.transform.scale(jugador_img, (config.ANCHO_JUGADOR, config.ALTO_JUGADOR))
fondo_img = pygame.image.load("img/fondo-tormenta.png")
fondo_img = pygame.transform.scale(fondo_img, (config.ANCHO, config.ALTO))
fondo_menus_img = pygame.image.load("img/fondo-tormenta-menus.png")
fondo_menus_img = pygame.transform.scale(fondo_menus_img, (config.ANCHO, config.ALTO))
granizo_img = pygame.image.load("img/piedra.png")
granizo_img = pygame.transform.scale(granizo_img, (10,10))
obs_tronco_img = pygame.image.load("img/troncos.png")
obs_tronco_img = pygame.transform.scale(obs_tronco_img, (65,65))

#Defino musica
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("music.mp3")
volumen = 0.09
sonido_fondo.set_volume(volumen)

# variables y config iniciales
pos_x, pos_y = config.POS_X, config.POS_Y
vidas = config.VIDAS
tiempo_inicial = pygame.time.get_ticks() # cronometro
reloj=pygame.time.Clock() # reloj para controlar los fps (frames por segundo)
puntuacion = 0
ultima_puntuacion = 0

# instancias de clases
piedras=  [Piedra() for _ in range(config.CANTIDAD_PIEDRAS)]
obstaculos= [Obstaculo(x, config.SUELO - config.TAM_OBSTACULOS) for x, y in config.POSICIONES_OBSTACULOS]
jugador= Jugador()

separacion_piedras_min = 120
piedras=[]
for i in range(config.CANTIDAD_PIEDRAS):
    posicion_x = random.randint(0, config.ANCHO - 30)
    if i > 0: # si no están juntas
        while abs(posicion_x - piedras[-1].x) < separacion_piedras_min:
            posicion_x = random.randint(0, config.ANCHO - 30)
            
    piedras.append(Piedra())
    
    
# función para reiniciar
def reiniciar_juego():
    global vidas, jugador, piedras, obstaculos, puntuacion, ultima_puntuacion
    vidas = config.VIDAS
    puntuacion = 0
    jugador.resetear()
    piedras = [Piedra() for _ in range(config.CANTIDAD_PIEDRAS)]
    obstaculos= [Obstaculo(x, config.SUELO - config.TAM_OBSTACULOS) for x, y in config.POSICIONES_OBSTACULOS]
    sonido_fondo.play(-1) # reinicio musica tambien
    
# función de pantalla de gameover o win
def pantalla_fin(pantalla, texto, color, fondo_menus_img):
    pantalla.blit(fondo_menus_img, (0,0))
    font_text(pantalla, texto, 36, color, config.ANCHO, config.ALTO, desplazamiento_y=-50)
    font_text(pantalla, f"Puntuación: {ultima_puntuacion}", 24, config.BLANCO, config.ANCHO, config.ALTO, desplazamiento_y=30)
    font_text(pantalla, f"Truco: Esquiva fácil y rápido saltando con SPACE y → o ←", 16, config.BLANCO, config.ANCHO, config.ALTO, desplazamiento_y=60)
    font_text(pantalla, "Presiona 'R' para Reiniciar o 'S' para Salir", 16, config.BLANCO, config.ANCHO, config.ALTO, desplazamiento_y=210)
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                esperando = False
                pygame.quit()
                return
            if e.type==pygame.KEYDOWN:
                if e.key == pygame.K_r: # reiniciar
                    esperando = False
                    reiniciar_juego()
                if e.key == pygame.K_s: # salir
                    esperando=False
                    pygame.quit()
                    return
                
def mostrar_cronometro():
    tiempo_actual = pygame.time.get_ticks()
    seg = (tiempo_actual - tiempo_inicial) // 1000
    font_text(pantalla, f"Tiempo: {seg}s", 16, config.BLANCO, 170, 90)
    
menu(pantalla, fondo_menus_img)
sonido_fondo.play(-1)

# bucle principal
while True:
    jugando = True
    while jugando:
        sonido_fondo.play() 
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                pygame.quit()
                exit()
        
        teclas = pygame.key.get_pressed()
        
        jugador.mover(teclas)

        # fondo
        pantalla.blit(fondo_img, (0, 0))
        
        # dibujo y muevo las piedras
        for piedra in piedras:
            piedra.mover()
            piedra.dibujar(pantalla, granizo_img)
            # colisión
            if jugador.tomar_rect().colliderect(piedra.tomar_rect()) and jugador.en_suelo:
                vidas -= 1
                piedra.y = 0  # Reseteo la piedra
                piedra.x = random.randint(0, config.ANCHO - 30)
                if vidas == 0:
                    ultima_puntuacion = puntuacion
                    pantalla_fin(pantalla, "Perdiste", config.ROJO, fondo_menus_img)
                    sonido_fondo.stop()
                    reiniciar_juego()
                    jugando = False

        # obstáculos
        for obstaculo in obstaculos:
            obstaculo.dibujar(pantalla, obs_tronco_img)
            obstaculo.x -= 2.5
            
            if obstaculo.x < -obstaculo.ancho:
                puntuacion += 1
                obstaculo.x = config.ANCHO + random.randint(0, 100)
                obstaculo.y = config.SUELO - obstaculo.alto 
            
            # colisión
            if jugador.tomar_rect().colliderect(obstaculo.tomar_rect()):
                ultima_puntuacion = puntuacion
                pantalla_fin(pantalla, "Perdiste", config.ROJO, fondo_menus_img)
                sonido_fondo.stop()
                reiniciar_juego()
                jugando = False
            
        if jugador.y >= config.ALTO - jugador.alto:
            jugador.y = config.ALTO - jugador.alto
            jugador.en_suelo = True
        
        #jugador
        jugador.dibujar(pantalla, jugador_img)
    
        # muestro contador de vidas y puntuación
        font_text(pantalla, f"Puntuación: {puntuacion}", 16, config.BLANCO, 224, 50)
        font_text(pantalla, f"Vidas: {vidas}", 16, config.BLANCO, 170, 150)
        
        # mostrar cronómetro
        mostrar_cronometro()
        
        # actualizar la pantalla
        pygame.display.flip()
         
        # controlo fps
        reloj.tick(60)  