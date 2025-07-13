import random
import math
from pygame import Rect
from pgzero.builtins import Actor, keyboard, music, sounds
import time

WIDTH = 800
HEIGHT = 600

TAMANHO_SPRITE = (120, 156)
BASE_GRAMA = 570
DESLOCAMENTO_HEROI_Y = -25
AJUSTE_GRAMA_INIMIGOS = [-12, -18]
CHAO_Y = BASE_GRAMA - (TAMANHO_SPRITE[1] // 2)
GRAVIDADE = 0.4
VELOCIDADE_PULO = -16

estado_jogo = "menu"
som_ativo = True
musica_tocando = False
jogo_pausado = False
VIDA_MAX = 3
vida_heroi = VIDA_MAX

CINZA = "gray"
BRANCO = "white"
VERMELHO = "red"
VERDE = (0, 200, 0)

# Botões do menu
botoes_menu = {
    "iniciar": Rect(300, 120, 200, 40),
    "som": Rect(300, 180, 200, 40),
    "sair": Rect(300, 240, 200, 40),
}
# Botões do jogo (topo direito, alinhados)
BOTAO_LARG = 44
BOTAO_ALT = 44
MARGEM = 12

botoes_jogo = {
    "som": Rect(WIDTH - BOTAO_LARG * 2 - MARGEM * 2, MARGEM, BOTAO_LARG, BOTAO_ALT),
    "pause": Rect(WIDTH - BOTAO_LARG - MARGEM, MARGEM, BOTAO_LARG, BOTAO_ALT),
}

class Heroi:
    def __init__(self):
        self.ator = Actor("hero_idle_1", (100, CHAO_Y + DESLOCAMENTO_HEROI_Y))
        self.vx = 0
        self.vy = 0
        self.no_chao = True
        self.quadro = 0
        self.idle_imgs = ["hero_idle_1", "hero_idle_2"]
        self.walk_imgs = ["hero_walk_1", "hero_walk_2"]
        self.invisivel = False
        self.tempo_invisivel = 0

    def atualizar(self):
        self.vx = -3 if keyboard.left else (3 if keyboard.right else 0)
        if keyboard.space and self.no_chao:
            self.vy = VELOCIDADE_PULO
            self.no_chao = False
            if som_ativo:
                sounds.jump.play()
        self.vy += GRAVIDADE
        self.ator.y += self.vy
        self.ator.x += self.vx
        if self.ator.y > CHAO_Y + DESLOCAMENTO_HEROI_Y:
            self.ator.y = CHAO_Y + DESLOCAMENTO_HEROI_Y
            self.vy = 0
            self.no_chao = True
        else:
            self.no_chao = False
        if self.ator.x < 0:
            self.ator.x = 0
        self.quadro = (self.quadro + 1) % 20
        imgs = self.walk_imgs if self.vx != 0 else self.idle_imgs
        self.ator.image = imgs[self.quadro // 12]
        if self.invisivel and time.time() > self.tempo_invisivel:
            self.invisivel = False

    def desenhar(self):
        if not self.invisivel or (int(time.time()*10) % 2 == 0):
            self.ator.draw()

class Inimigo:
    def __init__(self, x1, x2, ajuste_grama):
        self.ajuste_grama = ajuste_grama
        self.ator = Actor("enemy_walk_1", (x1, CHAO_Y + self.ajuste_grama))
        self.x1 = x1
        self.x2 = x2
        self.direcao = 1
        self.quadro = 0
        self.imagens = ["enemy_walk_1", "enemy_walk_2"]

    def atualizar(self):
        self.ator.x += self.direcao * 2
        self.ator.y = CHAO_Y + self.ajuste_grama
        if self.ator.x < self.x1 or self.ator.x > self.x2:
            self.direcao *= -1
        self.quadro = (self.quadro + 1) % 20
        self.ator.image = self.imagens[self.quadro // 15]

    def colisao_justa(self, heroi):
        r1 = self.ator._rect.inflate(-self.ator.width * 0.7, -self.ator.height * 0.7)
        r2 = heroi.ator._rect.inflate(-heroi.ator.width * 0.7, -heroi.ator.height * 0.7)
        return r1.colliderect(r2)

    def desenhar(self):
        self.ator.draw()

heroi = None
inimigos = []
tempo_ultimo_dano = 0
TEMPO_INVULNERAVEL = 1.0  # segundos

def desenhar_barra_vida():
    screen.draw.text("VIDA", (30, 6), fontsize=28, color=(255, 255, 0))
    x = 30
    y = 30
    largura = 40
    altura = 18
    espaco = 8
    for i in range(VIDA_MAX):
        cor = VERDE if i < vida_heroi else VERMELHO
        screen.draw.filled_rect(Rect(x + i*(largura+espaco), y, largura, altura), cor)
        screen.draw.rect(Rect(x + i*(largura+espaco), y, largura, altura), BRANCO)

def desenhar_botoes_jogo():
    # Botão de som (mute/unmute)
    if som_ativo:
        screen.blit("icon_unmuted", (botoes_jogo["som"].x, botoes_jogo["som"].y))
    else:
        screen.blit("icon_muted", (botoes_jogo["som"].x, botoes_jogo["som"].y))
    # Botão de pause/play
    if jogo_pausado:
        screen.blit("icon_play", (botoes_jogo["pause"].x, botoes_jogo["pause"].y))
    else:
        screen.blit("icon_pause", (botoes_jogo["pause"].x, botoes_jogo["pause"].y))

def desenhar_botoes_menu():
    for chave, ret in botoes_menu.items():
        screen.draw.filled_rect(ret, CINZA)
        if chave == "iniciar":
            texto = "Iniciar Jogo"
        elif chave == "som":
            texto = "Desativar som" if som_ativo else "Ativar som"
        elif chave == "sair":
            texto = "Sair"
        else:
            texto = chave
        screen.draw.text(texto, center=ret.center, color=BRANCO)

def draw():
    screen.clear()
    screen.blit("fundo", (0, 0))
    if estado_jogo == "menu":
        screen.draw.text("Resgate Thunder", center=(WIDTH // 2, 60), fontsize=40)
        desenhar_botoes_menu()
    elif estado_jogo == "jogo":
        heroi.desenhar()
        for inimigo in inimigos:
            inimigo.desenhar()
        desenhar_barra_vida()
        desenhar_botoes_jogo()
        if jogo_pausado:
            screen.draw.text("PAUSADO", center=(WIDTH//2, HEIGHT//2), fontsize=60, color=VERMELHO)
    elif estado_jogo == "fim":
        screen.blit("capturado", (0, 0))
        screen.draw.text("Capturado! Fim de jogo...", center=(WIDTH // 2, HEIGHT // 2 + 180), fontsize=40, color=VERMELHO)
    elif estado_jogo == "final_feliz":
        screen.blit("heroi_gato", (0, 0))

def update():
    global estado_jogo, vida_heroi, tempo_ultimo_dano
    if estado_jogo == "jogo" and not jogo_pausado:
        heroi.atualizar()
        agora = time.time()
        for inimigo in inimigos:
            inimigo.atualizar()
            if inimigo.colisao_justa(heroi) and (agora - tempo_ultimo_dano > TEMPO_INVULNERAVEL):
                if som_ativo:
                    sounds.hit.play()
                vida_heroi -= 1
                heroi.ator.x -= 60  # Empurrão para trás
                if heroi.ator.x < 0:
                    heroi.ator.x = 0
                tempo_ultimo_dano = agora
                heroi.invisivel = True
                heroi.tempo_invisivel = agora + TEMPO_INVULNERAVEL
                if vida_heroi <= 0:
                    estado_jogo = "fim"
        if heroi.ator.x > WIDTH:
            estado_jogo = "final_feliz"

def reiniciar_jogo():
    global heroi, inimigos, vida_heroi, tempo_ultimo_dano, jogo_pausado
    heroi = Heroi()
    inimigos = [
        Inimigo(500, 700, AJUSTE_GRAMA_INIMIGOS[0]),
        Inimigo(600, 750, AJUSTE_GRAMA_INIMIGOS[1])
    ]
    vida_heroi = VIDA_MAX
    tempo_ultimo_dano = 0
    jogo_pausado = False

def on_mouse_down(pos):
    global estado_jogo, som_ativo, musica_tocando, jogo_pausado
    if estado_jogo == "menu":
        if botoes_menu["iniciar"].collidepoint(pos):
            reiniciar_jogo()
            estado_jogo = "jogo"
        elif botoes_menu["som"].collidepoint(pos):
            som_ativo = not som_ativo
            if som_ativo:
                music.play("bg_music")
                musica_tocando = True
            else:
                music.stop()
                musica_tocando = False
        elif botoes_menu["sair"].collidepoint(pos):
            exit()
    elif estado_jogo == "fim":
        estado_jogo = "menu"
    elif estado_jogo == "final_feliz":
        reiniciar_jogo()
        estado_jogo = "jogo"
    elif estado_jogo == "jogo":
        if botoes_jogo["som"].collidepoint(pos):
            som_ativo = not som_ativo
            if som_ativo:
                music.play("bg_music")
                musica_tocando = True
            else:
                music.stop()
                musica_tocando = False
        elif botoes_jogo["pause"].collidepoint(pos):
            jogo_pausado = not jogo_pausado

def on_key_down(key):
    if estado_jogo == "final_feliz":
        reiniciar_jogo()
        globals()["estado_jogo"] = "jogo"
    elif estado_jogo == "fim":
        globals()["estado_jogo"] = "menu"
    elif estado_jogo == "jogo":
        global jogo_pausado
        if key == keys.P:
            jogo_pausado = not jogo_pausado
        elif key == keys.M:
            global som_ativo, musica_tocando
            som_ativo = not som_ativo
            if som_ativo:
                music.play("bg_music")
                musica_tocando = True
            else:
                music.stop()
                musica_tocando = False

def on_update():
    global musica_tocando
    if som_ativo and not musica_tocando:
        music.play("bg_music")
        musica_tocando = True
    elif (estado_jogo == "fim" or estado_jogo == "final_feliz") and musica_tocando:
        music.stop()
        musica_tocando = False

reiniciar_jogo()
if som_ativo:
    music.play("bg_music")
    musica_tocando = True
