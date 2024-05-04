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



    # Definindo as cores
    # # Definindo as cores
    # white = (255, 255, 255)
    # black = (0, 0, 0)
    # red = (213, 50, 80)
    # green = (0, 255, 0)
    # blue = (50, 153, 213)
    #
    # # Definindo as dimensões da tela
    # width, height = 1280, 720
    # game_display = pygame.display.set_mode((width, height))
    # pygame.display.set_caption('Snake Game')
    #
    # # Definindo o tamanho da cobrinha
    # block_size = 10
    # snake_speed = 15
    #
    # # Função para desenhar a cobra na tela
    # def draw_snake(snake_block, snake_list):
    #     for block in snake_list:
    #         pygame.draw.rect(game_display, green, [block[0], block[1], snake_block, snake_block])
    #
    # # Função para desenhar a fruta na tela
    # def draw_fruit(fruit_block, fruit_x, fruit_y):
    #     pygame.draw.rect(game_display, red, [fruit_x, fruit_y, fruit_block, fruit_block])
    #
    # # Função para desenhar matinhos na tela
    # def draw_grass(grass_block, grass_list):
    #     for grass in grass_list:
    #         pygame.draw.rect(game_display, (34, 139, 34), [grass[0], grass[1], grass_block, grass_block])
    #
    # # Função principal do jogo
    # def game_loop():
    #     game_over = False
    #     game_close = False
    #
    #     x1 = width / 2
    #     y1 = height / 2
    #
    #     x1_change = 0
    #     y1_change = 0
    #
    #     snake_list = []
    #     length_of_snake = 1
    #
    #     # Posição inicial da fruta
    #     fruit_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    #     fruit_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    #
    #     # Posição dos matinhos
    #     grass_list = []
    #     for _ in range(20):
    #         grass_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    #         grass_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    #         grass_list.append([grass_x, grass_y])
    #
    #     while not game_over:
    #
    #         while game_close:
    #             # Tela de Game Over
    #             game_display.fill(blue)
    #             font_style = pygame.font.SysFont(None, 30)
    #             message = font_style.render("Você perdeu! Pressione C para jogar novamente ou Q para sair.", True, red)
    #             game_display.blit(message, [width / 5, height / 3])
    #
    #             pygame.display.update()
    #
    #             for event in pygame.event.get():
    #                 if event.type == pygame.KEYDOWN:
    #                     if event.key == pygame.K_q:
    #                         game_over = True
    #                         game_close = False
    #                     if event.key == pygame.K_c:
    #                         game_loop()
    #
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 game_over = True
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_LEFT:
    #                     x1_change = -block_size
    #                     y1_change = 0
    #                 elif event.key == pygame.K_RIGHT:
    #                     x1_change = block_size
    #                     y1_change = 0
    #                 elif event.key == pygame.K_UP:
    #                     y1_change = -block_size
    #                     x1_change = 0
    #                 elif event.key == pygame.K_DOWN:
    #                     y1_change = block_size
    #                     x1_change = 0
    #
    #         if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
    #             game_close = True
    #         x1 += x1_change
    #         y1 += y1_change
    #         game_display.fill(blue)
    #         draw_fruit(block_size, fruit_x, fruit_y)
    #         draw_grass(block_size, grass_list)
    #         snake_head = []
    #         snake_head.append(x1)
    #         snake_head.append(y1)
    #         snake_list.append(snake_head)
    #         if len(snake_list) > length_of_snake:
    #             del snake_list[0]
    #
    #         for segment in snake_list[:-1]:
    #             if segment == snake_head:
    #                 game_close = True
    #
    #         draw_snake(block_size, snake_list)
    #
    #         pygame.display.update()
    #
    #         if x1 == fruit_x and y1 == fruit_y:
    #             fruit_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    #             fruit_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    #             length_of_snake += 1
    #
    #         # Definindo a velocidade da cobra
    #         clock = pygame.time.Clock()
    #         clock.tick(snake_speed)
    #     try:
    #         # Consultar o documento do jogador no banco de dados pelo nome
    #         player_data = collection.find_one({"name": player_name})
    #
    #         # Atualizar o campo de score no documento do jogador
    #         collection.update_one(
    #             {"name": player_name},
    #             {"$set": {"score_game2": player_score}}
    #         )
    #
    #         print("Score do jogo dois armazenado com sucesso!")
    #     except Exception as e:
    #         print(f"Erro ao armazenar score do jogo dois: {e}")
    #
    #
    #
    #     main_menu()
    #     #pygame.quit()
    #     #quit()
    #
    # game_loop()

    main_menu()


def play():

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

            try:
                player_data = collection.find_one({"name": player_name})

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

            # # Loop principal do jogo
            # try:
            #
            #     player_data = collection.find_one({"name": player_name})
            #
            #     # Recuperar o score atual do jogador do documento
            #     current_score = player_data.get("score", 0)
            #
            #     # Somar o score atual com o novo score
            #     new_score = current_score + score
            #     # Atualizar o score do jogador no banco de dados
            #     collection.update_one(
            #         {"name": player_name},
            #         {"$set": {"score": score}}
            #     )
            #     print("Score do jogador atualizado com sucesso!")
            # except Exception as e:
            #     print(f"Erro ao atualizar o score do jogador: {e}")

                # Após desenhar tudo, flipa o display


            # Após desenhar tudo, flipa o display
            pygame.display.flip()
        pygame.mixer.music.stop()


    # Ao sair do loop do jogo, definir o score final na variável global
#    global player_score
#    player_score = score





    main_menu()
#------------Player

def options():
    global player_score

    input_mode = True
    password = ""


    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("INDIGO")

        #global player_name

        global player_name

        # Consulta ao banco de dados para recuperar o nome e o score do jogador
        player_data = collection.find_one({"name": player_name})
        if player_data:
            # Recuperar o score atual do jogador do documento
            player_score = player_data.get("score", 0)
        else:
            # Se o jogador não for encontrado, defina o score como 0
            player_score = 0

        # Consulta ao banco de dados para recuperar o nome e o score do jogador
        #player_data = collection.find_one({"name": player_name}, {"score": 0})
        #player_score = player_data.get("score", 0)

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




    # global player_score
    # # Função para exibir as opções do jogo
    # input_mode = True  # Modo de inserção de texto desativado inicialmente
    # password = ""  # Variável para armazenar a senha inserida
    #
    # while True:
    #     OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    #     screen.fill(WHITE)
    #
    #     global player_name  # Declare a variável global
    #
    #     # Consulta ao banco de dados para recuperar o nome do jogador
    #     player_data = collection.find_one({}, {"name": 1})
    #     player_name = player_data["name"]
    #
    #     # Exibir nome do jogador e score na tela
    #     font_small = pygame.font.Font(None, 36)
    #     player_text = font_small.render(f"Nome: {player_name}", True, BLACK)
    #     score_text = font_small.render(f"Score: {player_score}", True, BLACK)
    #     screen.blit(player_text, (500, 450))
    #     screen.blit(score_text, (500, 500))
    #     # player_score += 0.1
    #
    #     OPTIONS_TEXT = font.render("Opções de jogo", True, WHITE)
    #     OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
    #     screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
    #
    #     OPTIONS_BACK = Button(image=None,
    #                           pos=(640, 660),
    #                           text_input="BACK",
    #                           font=font,
    #                           base_color="Black",
    #                           hovering_color="Green")
    #
    #     OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    #     OPTIONS_BACK.update(screen)
    #
    #     # Caixa de texto para senha
    #     password_text_input = pygame.Rect(400, 250, 400, 50)
    #
    #     # Desenhar caixa de texto apenas se estiver no modo de inserção de texto
    #     if input_mode:
    #         pygame.draw.rect(screen, BLACK, password_text_input, 2)
    #
    #         font_small = pygame.font.Font(None, 36)
    #         password_text_surface = font_small.render(password, True, BLACK)
    #         screen.blit(password_text_surface, (password_text_input.x + 5, password_text_input.y + 5))
    #
    #     font_small = pygame.font.Font(None, 36)
    #     password_text_surface = font_small.render("Senha:", True, BLACK)
    #     screen.blit(password_text_surface, (250, 260))
    #
    #     # Botão de submit para apagar usuário
    #     submit_button = Button(image=None,
    #                            pos=(640, 350),
    #                            text_input="Apagar",
    #                            font=font,
    #                            base_color="White",
    #                            hovering_color="Green")
    #     submit_button.changeColor(OPTIONS_MOUSE_POS)
    #     submit_button.update(screen)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
    #                 main_menu()
    #             elif submit_button.checkForInput(OPTIONS_MOUSE_POS):
    #                 if input_mode:
    #                     # Realizar ação de apagar usuário no banco de dados
    #                     try:
    #                         # Faça a exclusão do usuário do banco de dados MongoDB usando a senha
    #                         collection.delete_one({"password": password})
    #                         print("Usuário apagado com sucesso!")
    #                     except Exception as e:
    #                         print(f"Erro ao apagar usuário: {e}")
    #                 else:
    #                     input_mode = True  # Ativar o modo de inserção de texto
    #             elif password_text_input.collidepoint(event.pos):
    #                 input_mode = True  # Ativar o modo de inserção de texto
    #
    #         elif event.type == pygame.KEYDOWN:
    #             if input_mode:
    #                 if event.key == pygame.K_BACKSPACE:
    #                     # Remover o último caractere da senha se a tecla de backspace for pressionada
    #                     password = password[:-1]
    #                 elif event.key == pygame.K_RETURN:
    #                     input_mode = False  # Desativar o modo de inserção de texto ao pressionar Enter
    #                 else:
    #                     # Adicionar caracteres digitados à senha
    #                     password += event.unicode
    #
    #     pygame.display.update()


    # while True:
    #     OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    #     screen.fill("Indigo")
    #
    #     global player_name  # Declare a variável global
    #
    #     # Consulta ao banco de dados para recuperar o nome do jogador
    #     player_data = collection.find_one({}, {"name": 1})
    #     player_name = player_data["name"]
    #
    #     # Exibir nome do jogador e score na tela
    #     font_small = pygame.font.Font(None, 36)
    #     player_text = font_small.render(f"Nome: {player_name}", True, BLACK)
    #     score_text = font_small.render(f"Score: {player_score}", True, BLACK)
    #     screen.blit(player_text, (500, 450))
    #     screen.blit(score_text, (500, 500))
    #     # player_score += 0.1
    #
    #     OPTIONS_TEXT = font.render("Opções de jogo", True, WHITE)
    #     OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
    #     screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
    #
    #     OPTIONS_BACK = Button(image=None,
    #                           pos=(640, 660),
    #                           text_input="BACK",
    #                           font=font,
    #                           base_color="Black",
    #                           hovering_color="Green")
    #
    #     OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
    #     OPTIONS_BACK.update(screen)
    #
    #     # Caixa de texto para senha
    #     password_text_input = pygame.Rect(400, 250, 400, 50)
    #
    #     # Desenhar caixa de texto apenas se estiver no modo de inserção de texto
    #     if input_mode:
    #         pygame.draw.rect(screen, BLACK, password_text_input, 2)
    #
    #         font_small = pygame.font.Font(None, 36)
    #         password_text_surface = font_small.render(password, True, BLACK)
    #         screen.blit(password_text_surface, (password_text_input.x + 5, password_text_input.y + 5))
    #
    #     font_small = pygame.font.Font(None, 36)
    #     password_text_surface = font_small.render("Senha:", True, BLACK)
    #     screen.blit(password_text_surface, (250, 260))
    #
    #     # Botão de submit para apagar usuário
    #     submit_button = Button(image=None,
    #                            pos=(640, 350),
    #                            text_input="Apagar",
    #                            font=font,
    #                            base_color="White",
    #                            hovering_color="Green")
    #     submit_button.changeColor(OPTIONS_MOUSE_POS)
    #     submit_button.update(screen)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
    #                 main_menu()
    #             elif submit_button.checkForInput(OPTIONS_MOUSE_POS):
    #                 if input_mode:
    #                     # Realizar ação de apagar usuário no banco de dados
    #                     try:
    #                         # Faça a exclusão do usuário do banco de dados MongoDB usando a senha
    #                         collection.delete_one({"password": password})
    #                         print("Usuário apagado com sucesso!")
    #                     except Exception as e:
    #                         print(f"Erro ao apagar usuário: {e}")
    #                 else:
    #                     input_mode = True  # Ativar o modo de inserção de texto
    #             elif password_text_input.collidepoint(event.pos):
    #                 input_mode = True  # Ativar o modo de inserção de texto
    #
    #         elif event.type == pygame.KEYDOWN:
    #             if input_mode:
    #                 if event.key == pygame.K_BACKSPACE:
    #                     # Remover o último caractere da senha se a tecla de backspace for pressionada
    #                     password = password[:-1]
    #                 elif event.key == pygame.K_RETURN:
    #                     input_mode = False  # Desativar o modo de inserção de texto ao pressionar Enter
    #                 else:
    #                     # Adicionar caracteres digitados à senha
    #                     password += event.unicode
    #
    #     pygame.display.update()




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
                        "password": password
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


