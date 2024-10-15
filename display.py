import os
import math

import pygame as pg
from pygame.math import Vector3, Vector2

import noise
import globals.CONFIG as CONFIG
from terrain import apply_terrain_shading, calculate_normal
from utils import to_255
from cache import load_noise_from_cache, load_cloud_from_cache


def draw_circle(display: pg.Surface, radius: int, position: Vector2, light_direction: Vector3, time: float) -> None:
    rotation_angle = time * CONFIG.ROTATION_SPEED
    rotation_step = int((rotation_angle % (2 * math.pi)) / (2 * math.pi) * 72)  

    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if (x**2) + (y**2) <= radius**2:
                if (x, y, rotation_step) in noise.NOISE_CACHE:
                    noise_value = noise.NOISE_CACHE[(x, y, rotation_step)]
                    normal = calculate_normal(x, y, radius)
                    light_intensity = max(normal.dot(light_direction), 0)
                    color = apply_terrain_shading(noise_value, light_intensity)
                    display.set_at((int(position.x + x), int(position.y + y)), color)

def draw_cloud(display: pg.Surface, radius: int, position: Vector2, light_direction: Vector3, time: float) -> None:
    shadow_offset = Vector2(3, 3)
    rotation_angle = time * CONFIG.ROTATION_SPEED
    rotation_step = int((rotation_angle % (2 * math.pi)) / (2 * math.pi) * 72)  
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if (x**2) + (y**2) <= radius**2:
                    normal = calculate_normal(x, y, radius)
                    noise_value = noise.CLOUD_CACHE[(x, y, rotation_step)]
                    if noise_value > 0.4:
                        light_power = max(normal.dot(light_direction), 0)
                        shadow_x = x + int(shadow_offset.x)
                        shadow_y = y + int(shadow_offset.y)
                        if (shadow_x**2) + (shadow_y**2) <= radius**2:
                            display.set_at((int(position.x + shadow_x), int(position.y + shadow_y)), to_255(Vector3(50, 50, 50) * light_power))
                        display.set_at((int(position.x + x), int(position.y + y)), to_255(CONFIG.CLOUD_COLOR * light_power))

"""def draw_cloud(display: pg.Surface, radius: int, position: Vector2, light_direction: Vector3, time: float) -> None:
    shadow_offset = Vector2(3, 3)
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if (x**2) + (y**2) <= radius**2:
                    normal = calculate_normal(x, y, radius)
                    noise_value = noise.get_cloud_noise(normal, time, 42)
                    if noise_value > 0.4:
                        light_power = max(normal.dot(light_direction), 0)
                        shadow_x = x + int(shadow_offset.x)
                        shadow_y = y + int(shadow_offset.y)
                        if (shadow_x**2) + (shadow_y**2) <= radius**2:
                            display.set_at((int(position.x + shadow_x), int(position.y + shadow_y)), to_255(CONFIG.SHADOW_COLOR * light_power))
                        #get_cloud_shadow(normal, light_direction)
                        display.set_at((int(position.x + x), int(position.y + y)), to_255(CONFIG.CLOUD_COLOR * light_power))"""

def loading_text( display: pg.Surface, text: str ) -> None:
    font = pg.font.Font( None, 36 )
    text = font.render( text, True, ( 255, 255, 255 ) )
    text_rect = text.get_rect( center=( CONFIG.CENTER_X, CONFIG.CENTER_Y ) )
    display.blit( text, text_rect )
    pg.display.flip()

def clear_screen( display: pg.Surface ) -> None:
    display.fill( ( 0, 0, 0 ) )

def start_planet_generation( screen: pg.Surface ) -> None:
    if os.path.exists( "cache/noise_cache.txt" ):
        print("Loading from cache")
        loading_text( screen, "Loading..." )
        load_noise_from_cache()
        load_cloud_from_cache()
    else:
        print("Creating cache")
        loading_text( screen, "Creating..." )
        noise.precompute_rotating_noise( CONFIG.RADIUS, noise.NOISE_CACHE_FILE, 72 )
        if os.path.exists( "cache/cloud_cache.txt" ):
            load_cloud_from_cache()
    clear_screen( screen )