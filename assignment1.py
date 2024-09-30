# Library
import pygame
import random


class BackGround:
    def __init__(self):
        self.img_background = pygame.image.load('./images/start.png')

    def start(self):
        self.img_background = pygame.image.load('./images/background3.jpg')

    def finished(self):
        self.img_background = pygame.image.load('./images/result.png')


class Character:
    def __init__(self):
        self.img_character_1 = pygame.image.load('./images/zomhead_3.png')
        self.img_character_2 = pygame.image.load('./images/zomhead_3.png')
        self.img_character_3 = pygame.image.load('./images/zomhead_2.png')
        self.img_character_4 = pygame.image.load('./images/zomhead_1.png')
        self.img_character_5 = pygame.image.load('./images/zomhead_4.png')
        self.img_character_6 = pygame.image.load('./images/zomhead_5.png')
        self.data = []
        self.data.append(self.img_character_1.subsurface(0, 0, 80, 90))
        self.data.append(self.img_character_2.subsurface(0, 0, 80, 90))
        self.data.append(self.img_character_3.subsurface(0, 0, 80, 90))
        self.data.append(self.img_character_4.subsurface(0, 0, 80, 90))
        self.data.append(self.img_character_5.subsurface(0, 0, 80, 90))
        self.data.append(self.img_character_6.subsurface(0, 0, 80, 90))


class GameManager():
    def __init__(self):
        # Variables for the window game
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 120
        self.CHARACTER_WIDTH = 80
        self.CHARACTER_HEIGHT = 90
        self.FONT_TOP_MARGIN = 30
        self.LEVEL_SCORE_GAP = 5
        self.GAME_TITLE = "Whack A Zom"

        # Variables for the main game
        self.time_left = 51
        self.count_down = 4
        self.count_down_time = self.count_down
        self.score = 0
        self.miss = 0
        self.rate = 0
        self.level = 0
        self.start_game = False
        self.in_game = False
        self.game_over = False

        # Font object for displaying text
        self.font_obj = pygame.font.SysFont('britannic', 20)
        self.font_obj_finish = pygame.font.SysFont('britannic', 44)
        # self.font_coor = pygame.font.SysFont('britannic', 14)

        # Possible hole positions
        self.hole_positions = [
            (120, 550),
            (300, 550),
            (500, 550),
            (700, 550),
            (900, 550),
            (120, 450),
            (300, 450),
            (500, 450),
            (700, 450),
            (900, 450),
        ]

        # Initialize screen
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption(self.GAME_TITLE)
        pygame.mouse.set_cursor(pygame.cursors.arrow)

        # Initialize background
        self.bg = BackGround()
        self.screen.blit(self.bg.img_background, (0, 0))

        # Character
        self.character = Character()

        # Sound
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant

    def level_up(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the character pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.2
        if new_interval > 0:
            return new_interval
        else:
            return 0.04

    # Check whether the mouse click hit the character or not
    def is_character_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.CHARACTER_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.CHARACTER_HEIGHT):
            return True
        else:
            return False

    # Update the game states, re-calculate the player's score, miss, level

    def update(self, s_time):
        self.screen.blit(pygame.image.load(
            './images/background4.png'), (1010, 0))
        # Update time
        current_time_string = str(int(self.time_left - (pygame.time.get_ticks() - s_time)/1000)) + "s remain"
        time_text = self.font_obj.render(
            current_time_string, True, (255, 255, 255))
        time_text_pos = time_text.get_rect()
        time_text_pos.center = (self.SCREEN_WIDTH - 80, self.FONT_TOP_MARGIN)
        self.screen.blit(time_text, time_text_pos)
        # Update the player's miss
        current_miss_string = "Miss: " + str(self.miss)
        miss_text = self.font_obj.render(
            current_miss_string, True, (255, 255, 255))
        miss_text_pos = miss_text.get_rect()
        miss_text_pos.center = (
            self.SCREEN_WIDTH - 80, self.FONT_TOP_MARGIN * 4)
        self.screen.blit(miss_text, miss_text_pos)
        # Update the player's score
        current_score_string = "Score: " + str(self.score)
        score_text = self.font_obj.render(
            current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.center = (
            self.SCREEN_WIDTH - 80, self.FONT_TOP_MARGIN * 3)
        self.screen.blit(score_text, score_text_pos)
        

    # Start the game's main loop
    def start(self):
        # Variables of the loop function
        cycle_time = 0
        num = -1
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0
        stage = True

        # Set FPS
        fpsClock = pygame.time.Clock()

        # Create rect of the play_box and play_again components
        play_box = pygame.Rect(570, 330, 270, 140)
        play_again = []
        play_again.append(pygame.image.load('./images/again.png'))
        play_again.append(pygame.image.load('./images/again.png'))
        play_again_rect = pygame.Rect(550, 520, 187, 57)

        # To make the function called just once
        hover = 0
        finish = 0
        finish_hover = 0

        # The start time based on pygame.time.get_ticks()
        s_time = 0

        # Loop
        while stage:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stage = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_game == False and event.button == 1:
                        if play_box.collidepoint(pygame.mouse.get_pos()):
                            self.start_game = True
                            # Music
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load("music/UndeadRising.mp3")
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.2)

                            # Start time
                            s_time = pygame.time.get_ticks()
                    elif self.in_game == True and self.game_over == False and event.button == 1:
                        if self.is_character_hit(pygame.mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and num < 4:
                            num = 4
                            is_down = False
                            interval = 0
                            self.score += 1
                            self.level = self.level_up()
                            # Stop popping sound effect
                            self.soundEffect.stopPop()
                            self.soundEffect.playHammer()
                            self.update(s_time)
                        else:
                            self.soundEffect.playMiss()
                            self.miss += 1
                            self.update(s_time)
                    elif self.game_over == True and event.button == 1:
                        if play_again_rect.collidepoint(pygame.mouse.get_pos()):
                            # Set initial variables
                            self.start_game = True
                            self.in_game = False
                            self.game_over = False
                            self.score = 0
                            self.miss = 0
                            self.level = 0
                            # Set variables of the loop function
                            cycle_time = 0
                            num = -1
                            is_down = False
                            interval = 0.1
                            initial_interval = 1
                            frame_num = 0
                            finish = 0
                            finish_hover = 0

                            # Music
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load("music/UndeadRising.mp3")
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.2)

                            # Start time
                            s_time = pygame.time.get_ticks()

            if self.start_game == False:
                if play_box.collidepoint(pygame.mouse.get_pos()):
                    if hover == 0:
                        self.bg.img_background = pygame.image.load(
                            './images/start.png')
                        self.screen.blit(self.bg.img_background, (0, 0))
                        hover = 1
                else:
                    if hover == 1:
                        pygame.mouse.set_cursor(pygame.cursors.arrow)
                        self.bg.img_background = pygame.image.load(
                            './images/start.png')
                        self.screen.blit(self.bg.img_background, (0, 0))
                        hover = 0

            elif self.in_game == False:
                self.bg.start()
                self.screen.blit(self.bg.img_background, (0, 0))
                font_count_down = pygame.font.SysFont('britannic', 72)
                # Countdown
                self.count_down_time = int(
                    self.count_down - (pygame.time.get_ticks() - s_time)/1000)
                count_down_string = str(self.count_down_time)
                count_down_text = font_count_down.render(
                    count_down_string, True, (255, 255, 255))
                count_down_text_pos = count_down_text.get_rect()
                count_down_text_pos.center = (
                    self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
                self.screen.blit(count_down_text, count_down_text_pos)
                if (self.count_down_time == 0):
                    self.in_game = True
                    s_time = pygame.time.get_ticks()

            elif self.game_over == True:
                if finish == 0:
                    # Set arrow
                    pygame.mouse.set_cursor(pygame.cursors.arrow)
                    # Set background
                    self.bg.finished()
                    self.screen.blit(self.bg.img_background, (0, 0))
                    # Update the final score
                    final_score_string = "SCORE: " + str(self.score)
                    final_score_text = self.font_obj_finish.render(
                        final_score_string, True, (255, 255, 255))
                    final_score_text_pos = final_score_text.get_rect()
                    final_score_text_pos.center = (640, 240)
                    self.screen.blit(final_score_text, final_score_text_pos)
                    # Update the final miss
                    final_miss_string = "MISS: " + str(self.miss)
                    final_miss_text = self.font_obj_finish.render(
                        final_miss_string, True, (255, 255, 255))
                    final_miss_text_pos = final_miss_text.get_rect()
                    final_miss_text_pos.center = (640, 320)
                    self.screen.blit(final_miss_text, final_miss_text_pos)
                    # Update the final rate
                    if self.score + self.miss == 0:
                        rate = 0
                    elif self.score == 0:
                        rate = 100
                    else:
                        rate = round(
                            self.score/(self.score + self.miss) * 100, 2)
                    final_rate_string = "RATE: " + str(rate) + ' %'
                    final_rate_text = self.font_obj_finish.render(
                        final_rate_string, True, (255, 255, 255))
                    final_rate_text_pos = final_rate_text.get_rect()
                    final_rate_text_pos.center = (640, 400)
                    self.screen.blit(final_rate_text, final_rate_text_pos)
                    self.screen.blit(play_again[0], (550, 520))

                    finish = 1
                elif finish == 1:
                    if play_again_rect.collidepoint(pygame.mouse.get_pos()):
                        if finish_hover == 0:
                            pygame.mouse.set_cursor(pygame.cursors.broken_x)
                            self.screen.blit(play_again[1], (550, 520))
                            finish_hover = 1
                    else:
                        if finish_hover == 1:
                            pygame.mouse.set_cursor(pygame.cursors.arrow)
                            self.screen.blit(play_again[0], (550, 520))
                            finish_hover = 0
            else:
                if num > 5:
                    self.screen.blit(self.bg.img_background, (0, 0))
                    self.update(s_time)
                    num = -1

                if num == -1:
                    self.screen.blit(self.bg.img_background, (0, 0))
                    self.update(s_time)
                    num = 0
                    is_down = False
                    interval = 0.5
                    frame_num = random.randint(0, 9)

                # Reset character
                mil = fpsClock.tick(self.FPS)
                sec = mil / 1000.0
                cycle_time += sec
                if cycle_time > interval:
                    self.screen.blit(self.bg.img_background, (0, 0))
                    self.screen.blit(
                        self.character.data[num], (self.hole_positions[frame_num][0], self.hole_positions[frame_num][1]))
                    self.update(s_time)
                    if is_down is False:
                        num += 1
                    else:
                        num -= 1
                    if num == 5:
                        interval = 0.3
                    elif num == 4:
                        num -= 1
                        is_down = True
                        self.soundEffect.playPop()
                        # get the newly decreased interval value
                        interval = self.get_interval_by_level(initial_interval)
                    else:
                        interval = 0.1
                    cycle_time = 0

                if (int(self.time_left - (pygame.time.get_ticks() - s_time - 5)/1000) == 0):
                    self.game_over = True
                    # Set the theme sound
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load("music\halloween-time.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.1)

                # # Set coordinates counter
                # self.screen.blit(pygame.image.load(
                #     './images/background5.png'), (1120, 670))
                # coordinates_x, coordinates_y = pygame.mouse.get_pos()
                # textCoor = self.font_coor.render(
                #     'x: ' + str(coordinates_x) + ', y: ' + str(coordinates_y), True, (255, 255, 255))
                # textCoor_pos = textCoor.get_rect()
                # textCoor_pos.centerx = self.SCREEN_WIDTH - 70
                # textCoor_pos.centery = self.SCREEN_HEIGHT - 20
                # self.screen.blit(textCoor, textCoor_pos)

            pygame.display.update()


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("music/halloween-time.mp3")
        self.countDownSound = pygame.mixer.Sound('sounds/count.wav')
        self.hammerSound = pygame.mixer.Sound('sounds/death_sound.mp3')
        self.popSound = pygame.mixer.Sound("sounds/zombie_growl.mp3")
        self.missSound = pygame.mixer.Sound("sounds/miss.wav")
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def playCountDown(self):
        self.countDownSound.play()
        self.countDownSound.set_volume(0.2)

    def stopCountDown(self):
        self.countDownSound.stop()

    def playHammer(self):
        self.hammerSound.play()
        self.hammerSound.set_volume(0.2)

    def stopHammer(self):
        self.hammerSound.stop()

    def playPop(self):
        self.popSound.play()
        self.popSound.set_volume(0.2)

    def stopPop(self):
        self.popSound.stop()

    def playMiss(self):
        self.missSound.play()
        self.missSound.set_volume(0)

    def stopMiss(self):
        self.missSound.stop()

    def playLevelUp(self):
        self.levelSound.play()
        self.levelSound.set_volume(0)

    def stopLevelUp(self):
        self.levelSound.stop()


###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Run the main loop
my_game = GameManager()
my_game.start()
# Exit the game if the main loop ends
pygame.quit()
