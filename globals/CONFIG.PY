from pygame.math import Vector2
from pygame.math import Vector3

CENTER_X: int = 400
CENTER_Y: int = 300
RADIUS:   int = 100
POSITION: Vector2 = Vector2( CENTER_X, CENTER_Y )
COLOR:    Vector3 = Vector3( 255, 255, 255 )

WATER_THRESHOLD: float = 0.0
SEA_THRESHOLD:   float = 0.25
LAND_THRESHOLD:  float = 0.3
GRASS_THRESHOLD: float = 0.65
MOUNTAIN_THRESHOLD: float = 0.9

WATER_COLOR:    Vector3 = Vector3( 79,76,176 )
SEA_COLOR:      Vector3 = Vector3( 107,147,214 )
LAND_COLOR:     Vector3 = Vector3( 216,197,150 )
GRASS_COLOR:    Vector3 = Vector3( 159,193,100 )
MOUNTAIN_COLOR: Vector3 = Vector3( 139, 69, 19 )
CLOUD_COLOR:    Vector3 = Vector3( 255, 255, 255 )
SHADOW_COLOR:   Vector3 = Vector3( 50, 50, 50 )

ROTATION_SPEED:  float = 0.75
ROTATION_STEPS:  int = 72