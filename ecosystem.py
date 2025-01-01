import pygame as pg
from settings import *
from World.world import World
from real_time_plot import RealTimePlot
import threading
import queue

class Simulation:
    def __init__(self):
        pg.init()
        pg.font.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Ecosystem Simulation")
        self.clock = pg.time.Clock()
        
        self.world = World()
        self.r_state = True
        self.is_running = True
        
        self.font = pg.font.SysFont("arial", 20, True)
        self.light_color = (183, 192, 154)
        self.dark_color = (127, 133, 109)
        self.b1_texts = ["Pause", "Unpause"]
        
        self.animal_event = pg.USEREVENT + 1
        pg.time.set_timer(self.animal_event, int(1000 / min(SPEED, 30)))
        
        self.time = 0
        self.data_queue = queue.Queue()
        self.plot = None

    def game_loop(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            elif event.type == self.animal_event and self.r_state:
                self.world.run(True, True)
                self.time += 1
                # Send data to plot
                data = (self.time, 
                       len(self.world.rabbits), 
                       len(self.world.foxes), 
                       len(self.world.pigs))
                self.data_queue.put(data)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT-75 <= mouse[1] <= HEIGHT-25:
                    self.r_state = not self.r_state

    def draw(self):
        self.screen.fill("black")
        self.world.run(self.r_state, False)
        self.__buttons__()
        self.__display_population__()
        pg.display.flip()

    def __buttons__(self):
        mouse = pg.mouse.get_pos()
        if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT-75 <= mouse[1] <= HEIGHT-25:
            button1 = pg.draw.rect(self.screen, self.light_color, [WIDTH/2-100, HEIGHT-75, 200, 50])
        else:
            button1 = pg.draw.rect(self.screen, self.dark_color, [WIDTH/2-100, HEIGHT-75, 200, 50])
        
        b1_text = self.font.render(self.b1_texts[0] if self.r_state else self.b1_texts[1], True, (0, 0, 0))
        b1_rect = b1_text.get_rect(center=(button1.centerx, button1.centery))
        self.screen.blit(b1_text, b1_rect)

    def __display_population__(self):
        rabbits = len(self.world.rabbits)
        foxes = len(self.world.foxes)
        pigs = len(self.world.pigs)
        current_season = SEASONS[self.world.current_season]
        
        texts = [
            f"Season: {current_season}",
            f"Rabbits: {rabbits}",
            f"Foxes: {foxes}",
            f"Pigs: {pigs}"
        ]
        
        for i, text in enumerate(texts):
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i*30))

    def run(self):
        try:
            # Start Pygame in a separate thread
            game_thread = threading.Thread(target=self.game_loop)
            game_thread.daemon = True  # Make thread daemon so it exits when main thread exits
            game_thread.start()

            # Run plot in main thread
            self.plot = RealTimePlot(self.data_queue, self)
            self.plot.show()
        except Exception as e:
            print(f"Error in simulation: {e}")
        finally:
            self.is_running = False  # Ensure clean shutdown

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()