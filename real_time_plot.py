import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class RealTimePlot:
    def __init__(self, data_queue, simulation):
        self.data_queue = data_queue
        self.simulation = simulation
        
        plt.style.use('ggplot')
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        
        self.rabbits_data = []
        self.foxes_data = []
        self.pigs_data = []
        self.time_data = []
        
        self.line1, = self.ax.plot([], [], label='Rabbits', color='blue', linewidth=2)
        self.line2, = self.ax.plot([], [], label='Foxes', color='red', linewidth=2)
        self.line3, = self.ax.plot([], [], label='Pigs', color='green', linewidth=2)
        
        self.ax.legend(loc='upper right')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Population')
        self.ax.set_title('Ecosystem Population Dynamics')
        
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        
        self.ani = FuncAnimation(
            self.fig, 
            self.update,
            init_func=self.init_animation,
            interval=100,
            blit=True,
            cache_frame_data=False
        )

    def init_animation(self):
            """Initialize the animation with empty data"""
            self.line1.set_data([], [])
            self.line2.set_data([], [])
            self.line3.set_data([], [])
            return self.line1, self.line2, self.line3

    def update(self, frame):
        try:
            while not self.data_queue.empty():
                time, rabbits, foxes, pigs = self.data_queue.get_nowait()
                self.time_data.append(time)
                self.rabbits_data.append(rabbits)
                self.foxes_data.append(foxes)
                self.pigs_data.append(pigs)
        except:
            pass

        if len(self.time_data) > 0:
            self.line1.set_data(self.time_data, self.rabbits_data)
            self.line2.set_data(self.time_data, self.foxes_data)
            self.line3.set_data(self.time_data, self.pigs_data)
            
            # Dynamically adjust x-axis to show all data
            self.ax.set_xlim(0, max(self.time_data) + 10)
            
            # Adjust y-axis to show all population data with 10% padding
            max_pop = max(max(self.rabbits_data + self.foxes_data + self.pigs_data, default=0), 1)
            self.ax.set_ylim(0, max_pop * 1.1)
        
        return self.line1, self.line2, self.line3

    def on_close(self, event):
        """Handle plot window closing"""
        try:
            self.simulation.is_running = False
            plt.close('all')  # Close all matplotlib windows
        except:
            pass  # Ignore errors during shutdown

    def show(self):
        plt.show()