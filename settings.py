WIDTH = 1000 # WINDOW WIDTH
HEIGHT = 800 # WINDOW HEIGHT
FPS = 60 # 
SPEED = 5 # ANIMAL EVENTS PER SECOND
TILESIZE = 20 # SIZE OF ONE TILE
MAPSIZE = 50 # LENGTH/HEIGHT OF THE ENTIRE MAP
B_PERCENT = 0.04 # PERCENT OF LANDTILES COVERED IN BERRIES
H_PERCENT = 0.045 # PERCENT OF LANDTILES COVERED BY HERBIS
C_PERCENT = 0.02 # PERCENT OF LANDTILES COVERED BY CARNIS
O_PERCENT = 0.01 # PERCENT OF LANDTILES COVERED BY OMNIS
# Season settings
SEASON_LENGTH = 100  # Length of each season in ticks
SEASONS = ["Winter","Spring", "Summer", "Fall"]

# Season effects - Modified for more dramatic changes
WINTER_HUNGER_MULTIPLIER = 1.5       # Increased hunger in winter
WINTER_THIRST_MULTIPLIER = 1.2       # Increased thirst in winter
WINTER_FOOD_MULTIPLIER = 0.8         # Significantly less food in winter
WINTER_BREEDING_MULTIPLIER = 1.2    # Much harder to breed in winter

SPRING_BREEDING_MULTIPLIER = 0.3     # Breeding happens much faster in spring
SPRING_FOOD_MULTIPLIER = 1.7         # More food in spring
SPRING_THIRST_MULTIPLIER = 0.8       # Less thirst in spring due to rain

SUMMER_THIRST_MULTIPLIER = 1.8       # Much more thirst in summer
SUMMER_FOOD_MULTIPLIER = 1.0         # Normal food availability
SUMMER_BREEDING_MULTIPLIER = 1.0     # Normal breeding

FALL_FOOD_MULTIPLIER = 2.0           # Abundant food in fall
FALL_BREEDING_MULTIPLIER = 1.2       # Slightly harder breeding
FALL_THIRST_MULTIPLIER = 1.0         # Normal thirst
