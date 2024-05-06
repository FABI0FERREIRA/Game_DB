import pygame
import random
import sys
from button import Button
from pymongo import MongoClient
import pygame.mixer

pygame.init()

try:
    # Conectar-se ao cluster MongoDB Atlas
    cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net")
    # Acessar o banco de dados e a coleção
    db = cluster["python"]
    collection = db["game"]
    print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar-se ao banco de dados: {e}")

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir tamanho da janela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Carregar imagem de fundo
BG = pygame.image.load("Background.png").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Definir fonte
font = pygame.font.Font("Jersey25-Regular.ttf", 48)

global score
score = 0

global player_name
player_name = ""

global player_score
player_score = 0



pygame.mixer.music.load("mixkit-space-game-668.mp3")


def play2():


    # Definição das cores
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    # Definição das dimensões da tela
    width, height = 1280, 720
    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game')

    # Carregamento das imagens
    try:
        snake_img = pygame.image.load('cobra1.jpg')
        fruit_img = pygame.image.load('fruit.jpg')
        background_img = pygame.image.load('cenario.jpg')
        turtle_img = pygame.image.load('tartaruga.png')
    except pygame.error as e:
        print("Erro ao carregar imagem:", e)

    # Redimensionamento das imagens para o tamanho desejado
    block_size = 20
    snake_img = pygame.transform.scale(snake_img, (block_size, block_size))
    fruit_img = pygame.transform.scale(fruit_img, (block_size, block_size))
    background_img = pygame.transform.scale(background_img, (width, height))
    turtle_img = pygame.transform.scale(turtle_img, (block_size, block_size))

    # Definição da velocidade da cobra
    snake_speed = 10

    # Definição da classe Turtle
    class Turtle:
        def __init__(self, image, speed):
            self.image = image
            self.rect = self.image.get_rect()
            self.speed = speed
            self.rect.x = random.randrange(0, width - block_size)
            self.rect.y = random.randrange(0, height - block_size)

        def move(self):
            self.rect.x += self.speed

        def draw(self):
            game_display.blit(self.image, self.rect)

    def draw_fruit(fruit_x, fruit_y):
        game_display.blit(fruit_img, (fruit_x, fruit_y))

    def game_loop():
        global score  # Declare a variável global

        game_over = False
        game_close = False

        x1 = width / 2
        y1 = height / 2

        x1_change = 0
        y1_change = 0

        snake_list = []
        length_of_snake = 1

        # Posição inicial da fruta
        fruit_x = round(random.randrange(0, width - block_size) / block_size) * block_size
        fruit_y = round(random.randrange(0, height - block_size) / block_size) * block_size

        # Inicialização da tartaruga
        turtle_speed = 10
        turtle_spawn_rate = 200  # Definindo a taxa de aparecimento da tartaruga
        turtle_counter = 0  # Contador para controlar o aparecimento da tartaruga
        turtle = Turtle(turtle_img, turtle_speed)

        score = 0

        while not game_over:
            while game_close:
                # Tela de Game Over
                game_display.fill(black)
                font_style = pygame.font.SysFont(None, 40)
                message = font_style.render("Você perdeu! Pressione C para jogar novamente ou Q para sair.", True,
                                            white)
                game_display.blit(message, [width / 5, height / 3])

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -block_size
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = block_size
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -block_size
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = block_size
                        x1_change = 0

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            game_display.blit(background_img, (0, 0))  # Desenha o cenário
            draw_fruit(fruit_x, fruit_y)
            game_display.blit(snake_img, (x1, y1))  # Desenha a cobra

            # Movimento e desenho da tartaruga
            turtle.move()
            turtle.draw()

            # Verificação de colisão da cobra com a tartaruga
            if pygame.Rect(x1, y1, block_size, block_size).colliderect(turtle.rect):
                game_close = True

            # Exibe o escore na tela
            font = pygame.font.SysFont(None, 25)
            text = font.render("score: " + str(score), True, white)
            game_display.blit(text, (10, 10))

            pygame.display.update()

            if x1 == fruit_x and y1 == fruit_y:
                fruit_x = round(random.randrange(0, width - block_size) / block_size) * block_size
                fruit_y = round(random.randrange(0, height - block_size) / block_size) * block_size
                length_of_snake += 1
                score += 1  # Aumenta o escore quando a cobra come uma fruta

            # Contador da tartaruga
            turtle_counter += 1
            if turtle_counter >= turtle_spawn_rate:
                turtle_counter = 0
                turtle = Turtle(turtle_img, turtle_speed)  # Cria uma nova tartaruga

            clock = pygame.time.Clock()
            clock.tick(snake_speed)

        # Atualiza o score do jogador no banco de dados após o jogo
        try:
            player_data = collection.find_one({"name": player_name})
            # Verifique se o jogador existe no banco de dados antes de tentar atualizar o score
            if player_data:
                # Recuperar o score atual do jogador do documento
                player_score = player_data.get("score", 0)  # Aqui você recupera o score do jogador
                current_score = player_score  # Usando a variável player_score em vez de current_score

                # Somar o score atual com o novo score
                new_score = current_score + score

                # Atualizar o score do jogador no banco de dados
                collection.update_one(
                    {"name": player_name},
                    {"$set": {"score": new_score}}
                )
                print("Score do jogador atualizado com sucesso!")
            else:
                print("Jogador não encontrado no banco de dados.")
        except Exception as e:
            print(f"Erro ao atualizar o score do jogador: {e}")

    # Variáveis globais para o nome do jogador e o score
    global player_name, score

    # Consulta ao banco de dados para recuperar o nome do jogador
    player_data = collection.find_one({}, {"name": 1})
    player_name = player_data["name"]

    game_loop()

    main_menu()



def play():
    global player_name

    global player_score
    #player_score = 0

    global score
    score = 0



    pygame.mixer.music.play(-1)
    class Ship(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            original_image = pygame.image.load('spacenave.gif').convert()
            self.image = pygame.transform.scale(original_image, (100, 100))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
            self.speed_x = 0
            self.life = 3  # Defina a vida inicial da nave

        def update(self):
            self.speed_x = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speed_x = -5
            if keystate[pygame.K_RIGHT]:
                self.speed_x = 5
            self.rect.x += self.speed_x
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    # Definindo os asteroides
    class Asteroid(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            #self.image = pygame.image.load('asteroide.jpeg').convert()
            original_image = pygame.image.load('asteroides.gif').convert()
            self.image = pygame.transform.scale(original_image, (50 ,50))
            self.image.set_colorkey(BLACK)


            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)


        def update(self):
            self.rect.y += self.speed_y
            if self.rect.top > HEIGHT + 10:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speed_y = random.randrange(1, 2)




    # Classe para os projéteis
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((10, 20))  # Tamanho do projétil
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speed_y = -10  # Velocidade do projétil

        def update(self):
            self.rect.y += self.speed_y
            # Remover o projétil se ele sair da tela
            if self.rect.bottom < 0:
                self.kill()

    # Carregando as imagens
    background = pygame.image.load('backend.webp').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    # Criando os sprites
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Adicionando a nave
    player = Ship()
    all_sprites.add(player)

    # Adicionando os asteroides
    for i in range(8):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)


    #Loop do jogo
    running = True
    clock = pygame.time.Clock()
    while running:

        # Mantém o loop rodando na velocidade correta
        clock.tick(60)

        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()  # Disparar projéteis ao pressionar a tecla de espaço

        # Atualização
        all_sprites.update()

        # Checar colisões entre projéteis e asteroides
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit_asteroid in hits:
            score += 1  # Incrementar a pontuação ao destruir um asteroide
            # Adicionar novos asteroides após destruir um
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

        # Checar colisões entre nave e asteroides
        hits = pygame.sprite.spritecollide(player, asteroids, True)
        for hit_asteroid in hits:
            player.life -= 1  # Reduzir a vida da nave ao colidir com um asteroide
            if player.life <= 0:
                running = False  # Se a vida da nave acabar, encerrar o jogo

        # Desenhar / renderizar
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Exibir pontuação na tela
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Após desenhar tudo, flipa o display
        pygame.display.flip()


        asteroid_speed = 1
        speed_increase = 0.1

        # Loop do jogo
        running = True
        clock = pygame.time.Clock()
        while running:

            # Mantém o loop rodando na velocidade correta
            clock.tick(40)

            # Aumentar a velocidade dos asteroides com o tempo
            asteroid_speed += speed_increase

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()  # Disparar projéteis ao pressionar a tecla de espaço

            # Atualização
            all_sprites.update()

            # Checar colisões entre projéteis e asteroides
            hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
            for hit_asteroid in hits:
                score += 1  # Incrementar a pontuação ao destruir um asteroide
                # Adicionar novos asteroides após destruir um
                asteroid = Asteroid()
                asteroid.speed_y = asteroid_speed  # Atualizar a velocidade do novo asteroide
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

            # Checar colisões entre nave e asteroides
            hits = pygame.sprite.spritecollide(player, asteroids, True)
            for hit_asteroid in hits:
                player.life -= 1  # Reduzir a vida da nave ao colidir com um asteroide
                if player.life <= 0:
                    running = False  # Se a vida da nave acabar, encerrar o jogo

            # Desenhar / renderizar
            screen.blit(background, (0, 0))
            all_sprites.draw(screen)

            # Exibir pontuação na tela
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))


            # Após desenhar tudo, flipa o display
            pygame.display.flip()
        pygame.mixer.music.stop()

    global player_name  # Declare a variável global

    # Consulta ao banco de dados para recuperar o nome do jogador
    player_data = collection.find_one({}, {"name": 1})
    player_data1 = collection.find_one({}, {"score": 1})
    player_name = player_data["name"]
    player_score = player_data1["score"]

    print(f"O jogador {player_name} está jogando.")
    print(player_name)
    try:
        player_data = collection.find_one({"name": player_name})
        print(player_name)
        # Verifique se o jogador existe no banco de dados antes de tentar atualizar o score
        if player_data:
            # Recuperar o score atual do jogador do documento
            if player_data:
                # Recuperar o score atual do jogador do documento
                player_score = player_data.get("score", 0)  # Aqui você recupera o score do jogador
                current_score = player_score  # Usando a variável player_score em vez de current_score

                # Somar o score atual com o novo score
                new_score = current_score + score

                # Atualizar o score do jogador no banco de dados
                collection.update_one(
                    {"name": player_name},
                    {"$set": {"score": new_score}}
                )
            print("Score do jogador atualizado com sucesso!")
        else:
            print("Jogador não encontrado no banco de dados.")
    except Exception as e:
        print(f"Erro ao atualizar o score do jogador: {e}")

    # Ao sair do loop do jogo, definir o score final na variável global
#    global player_score
#    player_score = score





    main_menu()
#------------Player

def options():

    input_mode = True
    password = ""


    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("INDIGO")

        global player_name  # Declare a variável global

            # Consulta ao banco de dados para recuperar o nome do jogador
        player_data = collection.find_one({}, {"name": 1})
        player_data1 = collection.find_one({}, {"score": 1})
        player_name = player_data["name"]
        player_score = player_data1["score"]

        # Exibir nome do jogador e score na tela
        font_small = pygame.font.Font(None, 36)
        player_text = font_small.render(f"Nome: {player_name}", True, BLACK)
        score_text = font_small.render(f"Score: {player_score}", True, BLACK)
        screen.blit(player_text, (500, 450))
        screen.blit(score_text, (500, 500))

        OPTIONS_TEXT = font.render("Opções de jogo", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None,
                              pos=(640, 660),
                              text_input="BACK",
                              font=font,
                              base_color="Black",
                              hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        password_text_input = pygame.Rect(400, 250, 400, 50)

        if input_mode:
            pygame.draw.rect(screen, BLACK, password_text_input, 2)

            font_small = pygame.font.Font(None, 36)
            password_text_surface = font_small.render(password, True, BLACK)
            screen.blit(password_text_surface, (password_text_input.x + 5, password_text_input.y + 5))

        font_small = pygame.font.Font(None, 36)
        password_text_surface = font_small.render("Senha:", True, BLACK)
        screen.blit(password_text_surface, (250, 260))

        submit_button = Button(image=None,
                               pos=(640, 350),
                               text_input="Apagar",
                               font=font,
                               base_color="White",
                               hovering_color="Green")
        submit_button.changeColor(OPTIONS_MOUSE_POS)
        submit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif submit_button.checkForInput(OPTIONS_MOUSE_POS):
                    if input_mode:
                        try:
                            collection.delete_one({"password": password})
                            print("Usuário apagado com sucesso!")
                        except Exception as e:
                            print(f"Erro ao apagar usuário: {e}")
                    else:
                        input_mode = True

                elif password_text_input.collidepoint(event.pos):
                    input_mode = True

            elif event.type == pygame.KEYDOWN:
                if input_mode:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_mode = False
                    else:
                        password += event.unicode

        pygame.display.update()


def registro():
    # Função para registrar um novo usuário
    name = ""
    email = ""
    phone = ""
    password = ""
    registration_successful = False

    submit_button_rect = pygame.Rect(500, 600, 280, 60)

    while True:
        REG_MOUSE_POS = pygame.mouse.get_pos()

        # Define as cores
        BLACK = (0, 0, 0)
        GRAY = (100, 100, 100)

        # Preenche a tela com um degradê de preto para cinza
        for y in range(HEIGHT):
            # Calcula a cor com base na posição vertical (y)
            color = tuple((BLACK[i] * (HEIGHT - y) + GRAY[i] * y) // HEIGHT for i in range(3))
            pygame.draw.rect(screen, color, pygame.Rect(0, y, WIDTH, 1))

        REG_TEXT = font.render("Registro", True, WHITE)
        REG_RECT = REG_TEXT.get_rect(center=(640, 100))
        screen.blit(REG_TEXT, REG_RECT)

        # Caixas de texto para nome, email, telefone e senha
        name_text_input = pygame.Rect(400, 200, 400, 50)
        email_text_input = pygame.Rect(400, 300, 400, 50)
        phone_text_input = pygame.Rect(400, 400, 400, 50)
        password_text_input = pygame.Rect(400, 500, 400, 50)

        # Desenhar caixas de texto
        pygame.draw.rect(screen, BLACK, name_text_input, 2)
        pygame.draw.rect(screen, BLACK, email_text_input, 2)
        pygame.draw.rect(screen, BLACK, phone_text_input, 2)
        pygame.draw.rect(screen, BLACK, password_text_input, 2)

        font_small = pygame.font.Font(None, 36)
        text_surface_name = font_small.render("Nome:", True, BLACK)
        text_surface_email = font_small.render("Email:", True, BLACK)
        text_surface_phone = font_small.render("Telefone:", True, BLACK)
        text_surface_password = font_small.render("Senha:", True, BLACK)

        screen.blit(text_surface_name, (250, 210))
        screen.blit(text_surface_email, (250, 310))
        screen.blit(text_surface_phone, (250, 410))
        screen.blit(text_surface_password, (250, 510))

        # Renderizar botão de "Submit"
        submit_button = Button(image=None,
                               pos=(640, 600),
                               text_input="Submit",
                               font=font,
                               base_color="White",
                               hovering_color="Green")
        submit_button.changeColor(REG_MOUSE_POS)
        submit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if name:
                        name = name[:-1]
                    elif email:
                        email = email[:-1]
                    elif phone:
                        phone = phone[:-1]
                    elif password:
                        password = password[:-1]
                else:
                    if name_text_input.collidepoint(pygame.mouse.get_pos()):
                        name += event.unicode
                    elif email_text_input.collidepoint(pygame.mouse.get_pos()):
                        email += event.unicode
                    elif phone_text_input.collidepoint(pygame.mouse.get_pos()):
                        phone += event.unicode
                    elif password_text_input.collidepoint(pygame.mouse.get_pos()):
                        password += event.unicode


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.checkForInput(REG_MOUSE_POS):
                    # Inserir informações no banco de dados MongoDB
                    user_data = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "password": password,
                        "score": score
                    }
                    collection.insert_one(user_data)
                    # Após registrar, definir a flag de registro bem-sucedido
                    registration_successful = True

        # Renderizar texto digitado
        name_surface = font.render(name, True, BLACK)
        email_surface = font.render(email, True, BLACK)
        phone_surface = font.render(phone, True, BLACK)
        password_surface = font.render("*" * len(password), True, BLACK)

        screen.blit(name_surface, (name_text_input.x + 5, name_text_input.y + 5))
        screen.blit(email_surface, (email_text_input.x + 5, email_text_input.y + 5))
        screen.blit(phone_surface, (phone_text_input.x + 5, phone_text_input.y + 5))
        screen.blit(password_surface, (password_text_input.x + 5, password_text_input.y + 5))

        # Se o registro for bem-sucedido, exibir uma mensagem
        if registration_successful:
            success_message = font.render("Registro bem-sucedido!", True, BLACK)
            success_rect = success_message.get_rect(center=(640, 650))
            screen.blit(success_message, success_rect)

        # Renderizar botão de "BACK"
        back_button = Button(image=None,
                             pos=(100, 50),
                             text_input="BACK",
                             font=font,
                             base_color="White",
                             hovering_color="Green")
        back_button.changeColor(REG_MOUSE_POS)
        back_button.update(screen)

        if back_button.checkForInput(REG_MOUSE_POS):
            main_menu()

        pygame.display.flip()


def main_menu():
    global player_name
    # Função para exibir o menu principal
    while True:
        screen.blit(BG, (0, 0))



        MENU_MOUSE_POS = pygame.mouse.get_pos()


        MENU_TEXT = font.render("KINGS RPG", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"),
                             pos=(451, 250),
                             text_input="JOGAR",
                             font=font,
                             base_color="#d7fcd4",
                             hovering_color="White")
        PLAY2_BUTTON = Button(image=pygame.image.load("Play Rect.png"),
                             pos=(839, 250),
                             text_input="JOGAR2",
                             font=font,
                             base_color="#d7fcd4",
                             hovering_color="White")
        REG_BUTTON = Button(image=pygame.image.load("registro Rect.png"),
                            pos=(640, 370),
                            text_input="REGISTRAR",
                            font=font,
                            base_color="#d7fcd4",
                            hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"),
                                pos=(640, 490),
                                text_input="OPÇÕES/SCORE",
                                font=font,
                                base_color="#d7fcd4",
                                hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"),
                             pos=(640, 610),
                             text_input="SAIR",
                             font=font,
                             base_color="#d7fcd4",
                             hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON,  PLAY2_BUTTON,REG_BUTTON,OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if PLAY2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play2()  # Atualize o score do jogador
                elif REG_BUTTON.checkForInput(MENU_MOUSE_POS):
                    registro()
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()


