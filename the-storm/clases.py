import random
import pygame
import config

class Jugador:
    def __init__(self):
        self.x = config.POS_X
        self.y = config.SUELO - config.ALTO_JUGADOR
        self.ancho = config.ANCHO_JUGADOR
        self.alto = config.ALTO_JUGADOR
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.en_salto = False
        
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.vel_x = -config.VEL
        elif teclas[pygame.K_RIGHT]:
            self.vel_x = config.VEL
        else:
            self.vel_x = 0
        
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = -config.SALTO 
            # self.en_salto = True
            self.en_suelo = False
    
        if not self.en_suelo:
            self.vel_y += config.GRAVEDAD
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        if self.y >= config.SUELO - self.alto:
            self.y = config.SUELO - self.alto 
            self.vel_y = 0  
            # self.en_salto = False
            self.en_suelo = True 

    def dibujar(self, pantalla, jugador_img):
        pantalla.blit(jugador_img, (self.x, self.y))
        
    def tomar_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def resetear(self):
        self.x = config.POS_X
        self.y = config.SUELO - self.alto
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = True
        self.en_salto = False


class Piedra:   
    def __init__(self):
        self.x = random.randint(0, config.ANCHO - 30)
        self.y = 0
        self.velocidad = random.randint(4,8)
        
    def mover(self):
        self.y += self.velocidad
        if self.y > config.ALTO:
            self.y = 0
            self.x = random.randint(0, config.ANCHO - 30)
        
    def dibujar(self, pantalla, granizo_img):
        pantalla.blit(granizo_img, (self.x, self.y))
        
    def tomar_rect(self):
        return pygame.Rect(self.x, self.y, 20, 20)

class Obstaculo:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.ancho=config.TAM_OBSTACULOS
        self.alto=config.TAM_OBSTACULOS

    def dibujar(self, pantalla, obs_tronco_img):
        pantalla.blit(obs_tronco_img, (self.x, self.y))
        
    def tomar_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)