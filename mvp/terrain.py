import math
import pygame as pg
from pygame.math import Vector2, Vector3
import globals.CONFIG as CONFIG
import noise as noise
from utils import to_255

def apply_terrain_shading( noise_value: float, light_intensity: float ) -> tuple:
    if noise_value   <= CONFIG.WATER_THRESHOLD: base_color = CONFIG.WATER_COLOR
    elif noise_value <= CONFIG.SEA_THRESHOLD:   base_color = CONFIG.SEA_COLOR
    elif noise_value <= CONFIG.LAND_THRESHOLD:  base_color = CONFIG.LAND_COLOR
    elif noise_value <= CONFIG.GRASS_THRESHOLD: base_color = CONFIG.GRASS_COLOR
    
    else: base_color = CONFIG.GRASS_COLOR
    
    shaded_color = base_color * light_intensity

    return to_255(shaded_color)
            
def calculate_normal( x: int, y: int, radius: int ) -> Vector3:
    normal = Vector3()
    normal.x = x / radius
    normal.y = -y / radius 
    normal.z = ( 1 - ( normal.x**2 + normal.y**2 ) )**0.5 if normal.x**2 + normal.y**2 <= 1 else 0
    return normal

def get_normal_color( normal: Vector3 ) -> Vector3:
    color = Vector3()
    color.x = int( ( normal.x + 1 ) * 127.5 )
    color.y = int( ( normal.y + 1 ) * 127.5 )
    color.z = int( ( normal.z + 1 ) * 127.5 )
    return color

def get_light_direction( time: float ) -> Vector3: 
    return Vector3( math.cos( time * CONFIG.ROTATION_SPEED ), 0, math.sin( time * CONFIG.ROTATION_SPEED ) ).normalize()