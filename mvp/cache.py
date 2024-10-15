NOISE_CACHE_FILE = "cache/noise_cache.txt"
CLOUD_CACHE_FILE = "cache/cloud_cache.txt"
NOISE_CACHE = {}
CLOUD_CACHE = {}

def save_noise_to_cache( file_name: str = NOISE_CACHE_FILE ) -> bool:
    with open(file_name, 'w') as file:
        for key, value in NOISE_CACHE.items():
            x, y, step = key
            file.write( f'{x} {y} {step} {value}\n' )

def load_noise_from_cache( file_name: str = NOISE_CACHE_FILE ) -> None:
    with open( file_name, 'r' ) as file:
        for line in file:
            x, y, step, value = map( float, line.split() )
            NOISE_CACHE[( int( x ), int( y ), int( step ) )] = value

def save_cloud_to_cache( file_name: str = CLOUD_CACHE_FILE ) -> bool:
    with open(file_name, 'w') as file:
        for key, value in CLOUD_CACHE.items():
            x, y, step = key
            file.write( f'{x} {y} {step} {value}\n' )

def load_cloud_from_cache( file_name: str = CLOUD_CACHE_FILE ) -> None:
    with open( file_name, 'r' ) as file:
        for line in file:
            x, y, step, value = map( float, line.split() )
            CLOUD_CACHE[( int( x ), int( y ), int( step ) )] = value