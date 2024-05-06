import pygame
import random
import sys
from button import Button
from pymongo import MongoClient

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

def play():
    # Definindo a nave
    class Ship(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            original_image = pygame.image.load('spacenave.jpeg').convert()
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

    # Pontuação inicial
    score = 0

    # Loop do jogo
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

    pygame.quit()
    sys.exit()
def options():
    # Função para exibir as opções do jogo
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = font.render("Opções de jogo", True, WHITE)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None,
                              pos=(640, 460),
                              text_input="BACK",
                              font=font,
                              base_color="Black",
                              hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

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

# if __name__ == '__main__':
#     main_menu()
#

# import pygame
# import sys
# import pymongo
# from pymongo import MongoClient
#
# # Inicialize o Pygame
# pygame.init()
#
# try:
#     # Conectar-se ao cluster MongoDB Atlas
#     cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net")
#     # Acessar o banco de dados e a coleção
#     db = cluster["python"]
#     collection = db["game"]
#     print("Conexão com o banco de dados estabelecida com sucesso!")
# except Exception as e:
#     print(f"Erro ao conectar-se ao banco de dados: {e}")
#
# # Definir cores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
#
# # Definir tamanho da janela
# WIDTH, HEIGHT = 1280, 720
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Tela de Login")
#
# # Carregar imagem de fundo
# background_image = pygame.image.load("Background.png").convert()
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
#
# # Definir fonte personalizada
# font = pygame.font.Font("Jersey25-Regular.ttf", 48)
#
# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, 1, color)
#     textrect = textobj.get_rect()
#     textrect.topleft = (x, y)
#     surface.blit(textobj, textrect)
#
# def login_screen():
#



    # username = ''
    # email = ''
    # number = ''
    # password = ''
    # input_active = None
    #
    # submit_button = pygame.Rect(WIDTH/2-100, HEIGHT/4+400, 200, 50)
    #
    # while True:
    #     screen.blit(background_image, (0, 0))  # Desenha a imagem de fundo
    #
    #     draw_text('Tela de Login', font, BLACK, screen, WIDTH/2-150, HEIGHT/4)
    #
    #     # Desenhar caixas de texto para inserir nome, e-mail, número e senha
    #     username_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+80, 400, 50)
    #     email_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+160, 400, 50)
    #     number_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+240, 400, 50)
    #     password_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+320, 400, 50)
    #
    #     # Desenhar rótulos ao lado das caixas de texto
    #     draw_text('Nome:', font, WHITE, screen, username_rect.x - 100, username_rect.y + 10)
    #     draw_text('E-mail:', font, WHITE, screen, email_rect.x - 100, email_rect.y + 10)
    #     draw_text('Telefone:', font, WHITE, screen, number_rect.x - 100, number_rect.y + 10)
    #     draw_text('Senha:', font, WHITE, screen, password_rect.x - 100, password_rect.y + 10)
    #
    #     # Desenhar texto nas caixas de texto
    #     draw_text(username, font, WHITE, screen, username_rect.x + 10, username_rect.y + 10)
    #     draw_text(email, font, WHITE, screen, email_rect.x + 10, email_rect.y + 10)
    #     draw_text(number, font, WHITE, screen, number_rect.x + 10, number_rect.y + 10)
    #     draw_text(password, font, WHITE, screen, password_rect.x + 10, password_rect.y + 10)
    #
    #     pygame.draw.rect(screen, BLACK, username_rect, 2)
    #     pygame.draw.rect(screen, BLACK, email_rect, 2)
    #     pygame.draw.rect(screen, BLACK, number_rect, 2)
    #     pygame.draw.rect(screen, BLACK, password_rect, 2)
    #
    #     # Desenhar botão submit
    #     pygame.draw.rect(screen, BLACK, submit_button)
    #     draw_text('Submit', font, WHITE, screen, submit_button.x + 50, submit_button.y + 10)
    #
    #     # Atualizar a tela
    #     pygame.display.update()
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if username_rect.collidepoint(event.pos):
    #                 input_active = username_rect
    #             elif email_rect.collidepoint(event.pos):
    #                 input_active = email_rect
    #             elif number_rect.collidepoint(event.pos):
    #                 input_active = number_rect
    #             elif password_rect.collidepoint(event.pos):
    #                 input_active = password_rect
    #             elif submit_button.collidepoint(event.pos):
    #                 # Adicionar lógica para armazenar o cadastro no MongoDB
    #                 user_data = {
    #                     "username": username,
    #                     "email": email,
    #                     "number": number,
    #                     "password": password
    #                 }
    #                 collection.insert_one(user_data)
    #                 return True
    #             else:
    #                 input_active = None
    #         if event.type == pygame.KEYDOWN:
    #             if input_active:
    #                 if event.key == pygame.K_RETURN:
    #                     # Adicionar lógica para armazenar o cadastro no MongoDB
    #                     user_data = {
    #                         "username": username,
    #                         "email": email,
    #                         "number": number,
    #                         "password": password
    #                     }
    #                     collection.insert_one(user_data)
    #                     return True
    #                 elif event.key == pygame.K_BACKSPACE:
    #                     if input_active == username_rect:
    #                         username = username[:-1]
    #                     elif input_active == email_rect:
    #                         email = email[:-1]
    #                     elif input_active == number_rect:
    #                         number = number[:-1]
    #                     elif input_active == password_rect:
    #                         password = password[:-1]
    #                 else:
    #                     if input_active == username_rect:
    #                         username += event.unicode
    #                     elif input_active == email_rect:
    #                         email += event.unicode
    #                     elif input_active == number_rect:
    #                         number += event.unicode
    #                     elif input_active == password_rect:
    #                         password += event.unicode

#
# def main_menu():
#     while True:
#         # Coloque aqui o código para o menu principal
#         print("Menu principal")

# if __name__ == '__main__':
#      login_screen()
#         #main_menu()


#
# import pygame
# import sys
# import pymongo
# from pymongo import MongoClient
#
# # Inicialize o Pygame
# pygame.init()
#
# # # Inicialize o cliente MongoDB
# # client = pymongo.MongoClient("mongodb://localhost:27017/")
# # db = client["cadastro"]  # Nome do banco de dados
# # collection = db["usuarios"]  # Nome da coleção de usuários
#
# try:
#     # Conectar-se ao cluster MongoDB Atlas
#     #cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net")
#     cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net/test?retryWrites=true&w=majority")
#     # Acessar o banco de dados e a coleção
#     db = cluster["python"]
#     collection = db["game"]
#     print("Conexão com o banco de dados estabelecida com sucesso!")
# except Exception as e:
#     print(f"Erro ao conectar-se ao banco de dados: {e}")
#
# # Definir cores
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
#
# # Definir tamanho da janela
# WIDTH, HEIGHT = 1280, 720
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Tela de Login")
#
# # Carregar imagem de fundo
# background_image = pygame.image.load("Background.png").convert()
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
#
# # Definir fonte personalizada
# font = pygame.font.Font("Jersey25-Regular.ttf", 48)
#
# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, 1, color)
#     textrect = textobj.get_rect()
#     textrect.topleft = (x, y)
#     surface.blit(textobj, textrect)
#
# def login_screen():
#     username = ''
#     email = ''
#     number = ''
#     password = ''
#     input_active = None
#
#     while True:
#         screen.blit(background_image, (0, 0))  # Desenha a imagem de fundo
#
#         draw_text('Tela de Login', font, BLACK, screen, WIDTH/2-150, HEIGHT/4)
#
#         # Desenhar caixas de texto para inserir nome, e-mail, número e senha
#         username_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+80, 400, 50)
#         email_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+160, 400, 50)
#         number_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+240, 400, 50)
#         password_rect = pygame.Rect(WIDTH/2-200, HEIGHT/4+320, 400, 50)
#
#         # Desenhar texto nas caixas de texto
#         draw_text(username, font, WHITE, screen, username_rect.x + 10, username_rect.y + 10)
#         draw_text(email, font, WHITE, screen, email_rect.x + 10, email_rect.y + 10)
#         draw_text(number, font, WHITE, screen, number_rect.x + 10, number_rect.y + 10)
#         draw_text(password, font, WHITE, screen, password_rect.x + 10, password_rect.y + 10)
#
#         pygame.draw.rect(screen, BLACK, username_rect, 2)
#         pygame.draw.rect(screen, BLACK, email_rect, 2)
#         pygame.draw.rect(screen, BLACK, number_rect, 2)
#         pygame.draw.rect(screen, BLACK, password_rect, 2)
#
#         # Atualizar a tela
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if username_rect.collidepoint(event.pos):
#                     input_active = username_rect
#                 elif email_rect.collidepoint(event.pos):
#                     input_active = email_rect
#                 elif number_rect.collidepoint(event.pos):
#                     input_active = number_rect
#                 elif password_rect.collidepoint(event.pos):
#                     input_active = password_rect
#                 else:
#                     input_active = None
#             if event.type == pygame.KEYDOWN:
#                 if input_active:
#                     if event.key == pygame.K_RETURN:
#                         # Adicionar lógica para armazenar o cadastro no MongoDB
#                         user_data = {
#                             "username": username,
#                             "email": email,
#                             "number": number,
#                             "password": password
#                         }
#                         collection.insert_one(user_data)
#                         return True  # Retorna True após o cadastro ser realizado
#                     elif event.key == pygame.K_BACKSPACE:
#                         if input_active == username_rect:
#                             username = username[:-1]
#                         elif input_active == email_rect:
#                             email = email[:-1]
#                         elif input_active == number_rect:
#                             number = number[:-1]
#                         elif input_active == password_rect:
#                             password = password[:-1]
#                     else:
#                         if input_active == username_rect:
#                             username += event.unicode
#                         elif input_active == email_rect:
#                             email += event.unicode
#                         elif input_active == number_rect:
#                             number += event.unicode
#                         elif input_active == password_rect:
#                             password += event.unicode
#
# def main_menu():
#     while True:
#         # Coloque aqui o código para o menu principal
#         print("Menu principal")
#
# if __name__ == '__main__':
#     if login_screen():
#         main_menu()

