import pygame, sys, random

# functions

# draw the floor
def draw_floor():
    # position floor
    screen.blit(floor_surface,(floor_x_pos, 900))
    # create a second floor next to the first
    # so doesn't go out of view field
    screen.blit(floor_surface,(floor_x_pos + 576, 900))

def create_pipe():
    # get a random height for the new pipe from heights array
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    # get the list of pipes and move them left
    for pipe in pipes:
        pipe.centerx -= 5
    # return the updated list of pipes
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        # take the pipe and if it's the bottom one
        if pipe.bottom >= 1024:
            # draw it
            screen.blit(pipe_surface, pipe)
        # else if it's the upper one
        else:
            # flip the image
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            # draw it
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    # if collision with roof or floor
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3 , 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == True:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == False:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if high_score < score:
        high_score = score
    game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
    game_over_rect = game_over_surface.get_rect(center = (288, 512))
    screen.blit(game_over_surface, game_over_rect)
    return high_score

# init the sound mixer
# low the quality of the sound to play it instantly
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
# init pygame
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.ttf',40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# get image from assets
bg_surface = pygame.image.load('assets/background-day.png').convert() #convert help pygame to work with that image
# scale background image
bg_surface = pygame.transform.scale2x(bg_surface)
# get floor image
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# bird picture
# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird rectangle collisions
# bird_rect = bird_surface.get_rect(center = (100, 512))

# get bird pictures and scale them
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
# list of bird pictures to animate it
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
# index to loop over bird_frames
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

# get pipe picture
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
# list of pipes
pipe_list = []

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# create an event to trigger the spawn of a new pipe
SPAWNPIPE = pygame.USEREVENT
# set timer to spawn pipes
pygame.time.set_timer(SPAWNPIPE, 1200)
# different heights for pipes
pipe_heights = [400,600,800]

# load sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

# game loop
while True:
    # look for events
    for event in pygame.event.get():
        # if click X quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:    
                bird_movement = 0
                bird_movement -= 12
                # play wing sound
                # flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                # restart the game
                game_active = True
                # reset variables
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
                
        if event.type == SPAWNPIPE:
            # append a new pipe to the list
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
            
    # draw background
    screen.blit(bg_surface,(0,0))
    if game_active:
        # add gravity to the bird
        bird_movement += gravity
        # animate the bird
        rotated_bird = rotate_bird(bird_surface)
        # update bird position
        bird_rect.centery += bird_movement
        # draw bird
        screen.blit(rotated_bird, bird_rect)

        # update pipes position
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)
        
        score += 0.01
    else:
        high_score = update_score(score, high_score)
    score_display(game_active)
        
    # move floor ( games logic: player is still and the universe moves )
    floor_x_pos -= 1
    # update floor position
    draw_floor()
    # if the floor goes out of the view
    if floor_x_pos <= -576:
        # reset it to 0 and keep the loop
        floor_x_pos = 0
    #update canvas
    pygame.display.update()

    # fix to a maximum framerate of 120
    clock.tick(120)
