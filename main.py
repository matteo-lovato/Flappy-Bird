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
            
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

# game variables
gravity = 0.25
bird_movement = 0


# get image from assets
bg_surface = pygame.image.load('assets/background-day.png').convert() #convert help pygame to work with that image
# scale background image
bg_surface = pygame.transform.scale2x(bg_surface)
# get floor image
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0
# bird picture
bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
# bird rectangle collisions
bird_rect = bird_surface.get_rect(center = (100, 512))
# get pipe picture
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
# list of pipes
pipe_list = []
# create an event to trigger the spawn of a new pipe
SPAWNPIPE = pygame.USEREVENT
# set timer to spawn pipes
pygame.time.set_timer(SPAWNPIPE, 1200)
# different heights for pipes
pipe_heights = [400,600,800]

# game loop
while True:
    # look for events
    for event in pygame.event.get():
        # if click X quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
        if event.type == SPAWNPIPE:
            # append a new pipe to the list
            pipe_list.extend(create_pipe())
    # draw background
    screen.blit(bg_surface,(0,0))

    # add gravity to the bird
    bird_movement += gravity
    # update bird position
    bird_rect.centery += bird_movement
    
    # update pipes position
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # draw bird
    screen.blit(bird_surface, bird_rect)
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
