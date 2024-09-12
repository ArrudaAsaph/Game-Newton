import sys
import random
import time
import pygame


# INICIAR O JOGO
def game_start(w, h):
    pygame.init()
    tamanho = w, h
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Apple Newton")
    return tela


# CRIAR AS MAÇAS
def create_apple(apples, apples_rect):
    ranges = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115), 
              (265, 200), (430, 200), (835, 200), (900, 180), (160, 180), 
              (260, 280), (910, 280), (910, 330), (320, 330)]
    apple = pygame.image.load(("testes/maca.png"))
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()
    n_aleatorio = random.randrange(14)
    teste = ranges[n_aleatorio]
    apple_rect.x, apple_rect.y = teste
    apples.append(apple)
    apples_rect.append(apple_rect)


# DESENHAR AS MAÇAS
def draw_apples(apples, apples_rect, display):
    for i in range(len(apples)):
        display.blit(apples[i], apples_rect[i])


# CAPTURAR AS MAÇAS
def capture_apples(apples, apples_rect, personagem_rect):
    new_apples = []
    new_apples_rect = []
    for i in range(0, len(apples)):
        x = apples_rect[i].x
        y = apples_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if not (personagem_rect.colliderect(crop)):
            new_apples.append(apples[i])
            new_apples_rect.append(apples_rect[i])

    return new_apples, new_apples_rect


# Controle do tempo e velocidade das maçãs
def tempo(apple_speed, personagem_speed, sec):
    if sec < 15:
        apple_speed = 50   
        personagem_speed = 7.5
    elif 25 > sec >= 15:
        apple_speed = 2.5 
        personagem_speed = 8
    elif 35 > sec >= 25:
        apple_speed = 3.5
        personagem_speed = 8.5
    elif 50 > sec >= 35:
        apple_speed = 5
        personagem_speed = 9

    return apple_speed, personagem_speed


# Faz a maçã cair com base na velocidade
def cair_maca(apples_rect, velocidade):
    for i in range(len(apples_rect)):
        apples_rect[i].y += velocidade


# Controla a queda de uma nova maçã com base na posição da anterior
def queda_das_macas(apples, apples_rect, velocidade, distancia):
    cair_maca(apples_rect, velocidade)

    # Quando a primeira maçã passa da "distancia", uma nova começa a cair
    if apples_rect[0].y > distancia:
        create_apple(apples, apples_rect)


# Inicializar o display do jogo
display = game_start(1080, 720)

# Criar as maçãs
apples = []
apples_rect = []
for i in range(0, 2):  # Começa com 2 maçãs caindo
    create_apple(apples, apples_rect)

# Imagem de fundo e personagem
bg_image = pygame.image.load(("testes/imagem_bg.jpg"))
bg_image = pygame.transform.scale(bg_image, (1080, 720))

personagem = pygame.image.load("testes/boneco_newton.png")
personagem_rect = personagem.get_rect()
personagem_rect.x = -30
personagem_rect.y = 520

# Variáveis de controle
sec = 0
t = pygame.time.get_ticks()
apple_speed, personagem_speed = 50, 6
distancia_proxima_maca = 720  # Distância no eixo y para lançar uma nova maçã

# Loop principal do jogo
while True:
    # Atualizar a velocidade das maçãs com base no tempo decorrido
    apple_speed, personagem_speed = tempo(apple_speed, personagem_speed, sec)
    
    # Eventos do Pygame (sair do jogo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controles do personagem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        personagem_rect.x -= personagem_speed
        if personagem_rect.left < -30:
            personagem_rect.left = -30
    if keys[pygame.K_RIGHT]:
        personagem_rect.x += personagem_speed
        if personagem_rect.right > 1200:
            personagem_rect.right = 1200
   
    # Controla a queda das maçãs e adiciona novas quando necessário
    queda_das_macas(apples, apples_rect, 5, distancia_proxima_maca)

    # Verificar se o personagem capturou a maçã
    apples, apples_rect = capture_apples(apples, apples_rect, personagem_rect)
    
    # Adicionar novas maçãs se necessário
    if len(apples) < 20:
        if random.randrange(100) > 90:  # Adiciona uma nova maçã com 10% de chance
            create_apple(apples, apples_rect)

    # Cronômetro
    if (pygame.time.get_ticks() - t) >= 1000:
        sec += 1
        t = pygame.time.get_ticks()

    # Desenhar fundo e todos os objetos
    display.blit(bg_image, (0, 0))
    draw_apples(apples, apples_rect, display)
    display.blit(personagem, personagem_rect)
    
    pygame.display.flip()
    time.sleep(0.015)
