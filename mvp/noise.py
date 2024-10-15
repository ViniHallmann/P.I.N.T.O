import opensimplex
import numpy as np
import random
import math
import os
from pygame.math import Vector3
from cache import save_noise_to_cache, save_cloud_to_cache
from terrain import calculate_normal

from cache import NOISE_CACHE, NOISE_CACHE_FILE, CLOUD_CACHE, CLOUD_CACHE_FILE

def get_noise(normal_vector: Vector3, seed: int = None) -> float:

    if seed is not None:
        random.seed(seed)
    
    low_freq   = opensimplex.noise3(normal_vector.x , normal_vector.y , normal_vector.z )
    mid_freq   = opensimplex.noise3(4 * (normal_vector.x ), 4 * (normal_vector.y ), 4 * (normal_vector.z ))
    high_freq  = opensimplex.noise3(8 * (normal_vector.x ), 8 * (normal_vector.y ), 8 * (normal_vector.z ))

    terrain_values = 0.5 * low_freq
    terrain_values =  ( low_freq ) / 2
    terrain_values += 0.25 * (mid_freq + 1) / 2
    terrain_values += 0.125 * (high_freq + 1) / 2
    
    return terrain_values

def get_cloud_noise(normal_vector: Vector3 ) -> float:
    cloud_value = opensimplex.noise3(normal_vector.x * 1.5, normal_vector.y * 1.5, normal_vector.z * 1.5)
    return cloud_value

"""def get_cloud_noise( normal_vector: Vector3, time: float, seed: int = None ) -> float:
    cloud_value = opensimplex.noise3((normal_vector.x + (time * 0.1)) * 1.5, (normal_vector.y + (time * 0.1)) * 1.5, (normal_vector.z  * 1.5 ))
    return cloud_value"""

def precompute_static_noise( radius: int, file_name: str = NOISE_CACHE_FILE ) -> bool:
    for x in range( -radius, radius ):
        for y in range( -radius, radius ):
            if x**2 + y**2 <= radius**2:  
                NOISE_CACHE[( x, y )] = get_noise( calculate_normal( x, y, radius ), 42 )

    return save_noise_to_cache( file_name )


def precompute_rotating_noise( radius: int, file_name: str = NOISE_CACHE_FILE, angle_steps: int = 72 ) -> bool:
    for step in range(angle_steps):
        angle = step * ( 2 * math.pi / angle_steps )
        rotation_matrix = generate_rotation_matrix_y( angle )
        print( f'Precomputing noise step {step} for angle {angle}...' )

        for x in range( -radius, radius ):
            for y in range( -radius, radius ):
                if x**2 + y**2 <= radius**2:
                    normal = calculate_normal( x, y, radius )
                    rotated_normal = apply_rotation_matrix( normal, rotation_matrix )
                    noise_value = get_noise( rotated_normal )
                    NOISE_CACHE[( x, y, step )] = noise_value
                    if not os.path.exists( "cache/cloud_cache.txt" ):
                        CLOUD_CACHE[( x, y, step )] = get_cloud_noise( rotated_normal )

    save_noise_to_cache( file_name )
    save_cloud_to_cache( CLOUD_CACHE_FILE )


def apply_rotation_matrix( vector: Vector3, rotation_matrix: list[list[float]] ) -> Vector3:
    rotated_vector = Vector3(
        vector.x * rotation_matrix[0][0] + vector.y * rotation_matrix[0][1] + vector.z * rotation_matrix[0][2],
        vector.x * rotation_matrix[1][0] + vector.y * rotation_matrix[1][1] + vector.z * rotation_matrix[1][2],
        vector.x * rotation_matrix[2][0] + vector.y * rotation_matrix[2][1] + vector.z * rotation_matrix[2][2]
    )
    return rotated_vector


def generate_rotation_matrix_x( angle: float ) -> list[list[float]]:
    rotation_x = [
        [1, 0, 0],
        [0, math.cos( angle ), -math.sin( angle )],
        [0, math.sin( angle ), math.cos( angle )]
    ]
    return rotation_x

def generate_rotation_matrix_y( angle: float ) -> list[list[float]]:
    rotation_y = [
        [math.cos( angle ), 0, math.sin( angle )],
        [0, 1, 0],
        [-math.sin( angle ), 0, math.cos( angle )]
    ]
    return rotation_y

def generate_rotation_matrix_z( angle: float ) -> list[list[float]]:
    rotation_z = [
        [math.cos( angle ), -math.sin( angle ), 0],
        [math.sin( angle ), math.cos( angle ), 0],
        [0, 0, 1]
    ]
    return rotation_z
