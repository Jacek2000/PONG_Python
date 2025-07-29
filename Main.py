#Importowanie bibliotek
import pygame
import sys
from Game_Settings import *
import random

#funkcja podająca koordynaty pozycji startowych dla paletek oraz piłki
def default_positions():
    player_pos = pygame.Rect(0, 250, GAME_CONSTANTS["paddle_width"], GAME_CONSTANTS["paddle_height"])   #przechowywuje i pozwala manipulować koordynatami paletki gracza
    ai_pos = pygame.Rect(WINDOW_SETTINGS["width"] - GAME_CONSTANTS["paddle_width"], 250, GAME_CONSTANTS["paddle_width"], GAME_CONSTANTS["paddle_height"])
    ball_pos_x = WINDOW_SETTINGS["width"] // 2  #x pozycja początkowa piłki
    ball_pos_y = WINDOW_SETTINGS["height"] // 2 #y pozycja początkowa piłki
    ball_direction_x = random.randrange(1,10)   #losowanie kierunku x w którym podąży piłka
    ball_direction_y = random.randrange(1,10)   #losowanie kierunku y w którym podąży piłka
    ball_speed_x = GAME_CONSTANTS["ball_speed_x"]   #pobranie pierwotnej prędkości piłki na osi x
    ball_speed_y = GAME_CONSTANTS["ball_speed_y"]   #pobranie pierwotnej prędkości piłki na osi y 

    #przypisanie wylosowanej zmiennej x odpowedniego kierunku x piłki
    if ball_direction_x <= 5:
        ball_direction_x = 1
    else:
        ball_direction_x = -1
    
    #przypisanie wylosowanej zmiennej y odpowiedniego kierunku piłki
    if ball_direction_y <= 5:
        ball_direction_y = 1
    else:
        ball_direction_y = -1
    
    return player_pos, ai_pos, ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y, ball_speed_x, ball_speed_y

pygame.init()   #Inicjacja biblioteki pygame

window = pygame.display.set_mode((WINDOW_SETTINGS['width'], WINDOW_SETTINGS['height'])) #Ustawienie szerokości i wysokości okna  
pygame.display.set_caption(WINDOW_SETTINGS["screen_title"])  #Ustawienie tytułu okna programu
running = True  #Ustawienie flagi pozwalającej na włączenie i wyłączenie głównej pętli gry

#pierwotne ustawienie paletek oraz piłki na ekranie
player_pos, ai_pos, ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y, ball_speed_x, ball_speed_y = default_positions()

#Śledzenie wyniku
player_score = 0
ai_score = 0

#Czcionka do wyświetlania wyniku
font = pygame.font.SysFont(None, 48)

#Flaga odpalająca grę
game = False

#Flaga odpalająca AI
ai = False

#txt kto wygrał ostatnią rozgrywkę
wygrany = ""

#dźwięki
bounce_sound_1 = pygame.mixer.Sound("sciana.mp3")
bounce_sound_2 = pygame.mixer.Sound("paletka.mp3")
point_sound = pygame.mixer.Sound("punkt.mp3")

#Główna pętla gry 
while running:
    #Obsłużenie eventów
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #obsługa kliknięcia x na oknie 
            running = False
            pygame.quit()
            sys.exit()

    window.fill("black")    #wypełnienie ekranu na czarno
    key_pressed = pygame.key.get_pressed()  #pobranie przyciśniętego przycisku
    
    #Ekran początkowy
    if not game:
        enter_text = font.render(f"Wybierz jedną z opcji aby rozpocząć", True, COLORS["ball_paddle_white"])
        window.blit(enter_text, (WINDOW_SETTINGS["width"] // 2 - enter_text.get_width() // 2, WINDOW_SETTINGS["height"] // 4 - enter_text.get_height() // 2))
        option_1_text = font.render(f"Wciśnij 1 - Player vs AI", True, COLORS["ball_paddle_white"])
        window.blit(option_1_text, (WINDOW_SETTINGS["width"] // 2 - enter_text.get_width() // 2, (WINDOW_SETTINGS["height"] // 4 - enter_text.get_height() // 2) + enter_text.get_height() + 30 ))
        option_2_text = font.render(f"Wciśnij 2 - Player vs Player", True, COLORS["ball_paddle_white"])
        window.blit(option_2_text, (WINDOW_SETTINGS["width"] // 2 - enter_text.get_width() // 2, (WINDOW_SETTINGS["height"] // 4 - enter_text.get_height() // 2) + 2 * enter_text.get_height() + 60 ))
        win_text = font.render(wygrany, True, COLORS["ball_paddle_white"])
        window.blit(win_text, (WINDOW_SETTINGS["width"] // 2 - enter_text.get_width() // 2, (WINDOW_SETTINGS["height"] // 4 - enter_text.get_height() // 2) + 3 * enter_text.get_height() + 90 ))

    #Włączenie gry
    if key_pressed[pygame.K_1]:
        game = True
        ai = True
    
    if key_pressed[pygame.K_2]:
        game = True
        ai = False

    #Logika i przebieg gry
    if game:
        #Poruszanie się lewej paletki kontrolowanej przez gracza
        if key_pressed[pygame.K_w]:    #Sprawdzenie czy przyciśnięto przycisk strzałki w górę
            if player_pos.top > 0:
                player_pos.top -= GAME_CONSTANTS["paddle_speed"] 

        if key_pressed[pygame.K_s]:  #Sprawdzenie czy przyciśnięto przycisk strzałki w dół
            if player_pos.bottom < WINDOW_SETTINGS["height"]:
                player_pos.bottom += GAME_CONSTANTS["paddle_speed"] 

        if ai:
            #Poruszanie się prawej paletki kontrolowanej przez AI
            error = random.randint(-20, 20) #wprowadzenie błędu określenia położenia piłki
            center_ai = ai_pos.top + GAME_CONSTANTS["paddle_height"] // 2
            if ball_pos_x > WINDOW_SETTINGS["width"] * 0.8:
                if ball_pos_y + error > center_ai:  #Piłka znajduje się poniżej środka paletki AI
                    if ai_pos.bottom < WINDOW_SETTINGS["height"]:
                        ai_pos.bottom += GAME_CONSTANTS["paddle_speed"] 

            if ball_pos_x > WINDOW_SETTINGS["width"] * 0.8:
                if ball_pos_y + error < center_ai:  #Piłka znajduje się powyżej środka paletki AI
                    if ai_pos.top > 0:
                        ai_pos.top -= GAME_CONSTANTS["paddle_speed"]  
        
        else:
            if key_pressed[pygame.K_DOWN]:
                if ai_pos.bottom < WINDOW_SETTINGS["height"]:
                        ai_pos.bottom += GAME_CONSTANTS["paddle_speed"]
            
            if key_pressed[pygame.K_UP]:
                if ai_pos.top > 0:
                        ai_pos.top -= GAME_CONSTANTS["paddle_speed"]

        #Odbijanie się piłki od ściany górnej oraz dolnej
        if ball_pos_y <= 0 or ball_pos_y >= WINDOW_SETTINGS["height"]:
            ball_direction_y = ball_direction_y * (-1)  #zmiana kierunku piłki 
            bounce_sound_1.play()

        #Sprawdzenie czy gracz odbił piłkę
        if ball_pos_x <= 15:
            
            #udało się odbić piłkę
            if ball_pos_y >= player_pos.top and ball_pos_y <= player_pos.bottom:
                ball_direction_x = ball_direction_x * (-1)
                ball_speed_x += 0.01
                bounce_sound_2.play()
            
            #nie udało się odbić piłki
            else:
                ai_score += 1
                point_sound.play()
                player_pos, ai_pos, ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y, ball_speed_x, ball_speed_y = default_positions()
            
        #Sprawdzenie czy ai odbiło piłkę
        if ball_pos_x >= WINDOW_SETTINGS["width"] - 15:
            
            #udało się odbić piłkę
            if ball_pos_y >= ai_pos.top and ball_pos_y <= ai_pos.bottom:
                ball_direction_x = ball_direction_x * (-1)
                ball_speed_x += 0.01
                bounce_sound_2.play()
            
            #nie udało się odbić piłki
            else:
                player_score += 1
                point_sound.play()
                player_pos, ai_pos, ball_pos_x, ball_pos_y, ball_direction_x, ball_direction_y, ball_speed_x, ball_speed_y = default_positions()
        
        ball_pos_x = ball_pos_x + ball_direction_x * ball_speed_x
        ball_pos_y = ball_pos_y + ball_direction_y * ball_speed_y
        
        #rysowanie paletek oraz piłki na nowych położeniach
        pygame.draw.rect(window, COLORS["ball_paddle_white"], player_pos)
        pygame.draw.rect(window, COLORS["ball_paddle_white"], ai_pos)
        pygame.draw.circle(window, COLORS["ball_paddle_white"], (ball_pos_x, ball_pos_y), GAME_CONSTANTS["ball_radius"])

        #rysowanie wyniku
        score_text = font.render(f"{player_score} : {ai_score}", True, COLORS["ball_paddle_white"])
        window.blit(score_text, (WINDOW_SETTINGS["width"] // 2 - score_text.get_width() // 2, 20))

        #Sprawdzenie wyniku
        if player_score == 7:
            game = False
            ai_score = 0
            player_score = 0
            if ai:
                wygrany = "Wygrał PLAYER"
            else:
                wygrany = "Wygrał PLAYER 1"
        
        if ai_score == 7:
            game = False
            ai_score = 0
            player_score = 0
            if ai:
                wygrany = "Wygrało AI"
            else:
                wygrany = "Wygrał PLAYER 2"


    pygame.display.flip()   #Wyrzuca zmiany na okno gry, działa jako odświeżanie ekranu 

