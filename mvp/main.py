import pygame as pg
import globals.CONFIG as CONFIG
from pygame.math import Vector2
from display import start_planet_generation
from terrain import get_light_direction
from display import clear_screen, loading_text, draw_circle, draw_cloud
from utils import to_255

def main():
    pg.init()
    pg.display.set_caption("P.I.N.T.O")
    screen = pg.display.set_mode( ( 800, 600 ) )
    font = pg.font.SysFont("Arial" , 18 , bold = True)

    small_resolution = (200, 150) 
    small_surface = pg.Surface(small_resolution)

    small_center_x = small_resolution[0] // 2
    small_center_y = small_resolution[1] // 2
    small_position = Vector2(small_center_x, small_center_y)

    clock = pg.time.Clock()
    done = False
    
    start_planet_generation( screen )
    
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT: done = True

        time = pg.time.get_ticks() / 1000
        light_direction = get_light_direction( time )

        small_surface.fill((0, 0, 0))
        
        draw_circle(small_surface, CONFIG.RADIUS//2, small_position, light_direction, time)
        draw_cloud(small_surface, CONFIG.RADIUS//2, small_position, light_direction, time)
        scaled_surface = pg.transform.scale(small_surface, screen.get_size())
        
        screen.blit(scaled_surface, (0, 0))
        fps = int(clock.get_fps())  

        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        pg.display.flip()

        clock.tick(120)

    pg.quit()

if __name__ == "__main__":
    main()