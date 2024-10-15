from pygame.math import Vector3

def to_255(color: Vector3) -> tuple:
    return (int(min(max(color.x, 0), 255)),
            int(min(max(color.y, 0), 255)),
            int(min(max(color.z, 0), 255)))