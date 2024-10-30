import pygame
import config

def font_text(pantalla, texto, tamaño, color, ancho_pantalla, alto_pantalla, desplazamiento_y=0):
    fuente = pygame.font.Font("fonts/PressStart2P-Regular.ttf", tamaño)
    texto_superficie=fuente.render(texto, True, color) 
    
    # objeto de variables x,y,w,h -> return > Rect(0,0,w,h) - toma el ancho y alto de una superficie (en este caso la pantalla)
    # obtengo el rectángulo del texto y lo centro
    texto_rect=texto_superficie.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + desplazamiento_y))
    
    # creo la sombra
    sombra = fuente.render(texto,True,(0,0,0))
    sombra_rect=sombra.get_rect(center=(ancho_pantalla // 2 + 2, alto_pantalla // 2 + 2 + desplazamiento_y))
    
    pantalla.blit(sombra, sombra_rect)
    pantalla.blit(texto_superficie, texto_rect)

def menu(pantalla, fondo_menus_img):
    while True:
        pantalla.blit(fondo_menus_img, (0, 0))
        
        ancho_pantalla = config.ANCHO
        alto_pantalla = config.ALTO
        
        font_text(pantalla, "Menú Principal", 36, config.BLANCO, ancho_pantalla, alto_pantalla, desplazamiento_y=-150)
        
        font_text(pantalla, "1. Jugar", 24, config.VERDE, ancho_pantalla, alto_pantalla, desplazamiento_y=-40)
        font_text(pantalla, "2. Salir", 24, config.ROJO, ancho_pantalla, alto_pantalla, desplazamiento_y=10)
        
        font_text(pantalla, "Controles:", 24, config.AZUL, ancho_pantalla, alto_pantalla, desplazamiento_y=150)
        font_text(pantalla, "← Moverse a la Izquierda | → Moverse a la Derecha | SPACE: Saltar | R: Reiniciar", 10, config.AMARILLO, ancho_pantalla, alto_pantalla, desplazamiento_y=200)
        
        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_1: # jugar
                    return
                if e.key==pygame.K_2: # salir
                    pygame.quit()
                    exit()
