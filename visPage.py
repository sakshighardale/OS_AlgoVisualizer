import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation

class PageReplacementVisualization:
    def __init__(self):
        # Initialize data
        self.frames = 3
        self.page_references = [7, 0, 1, 2, 0, 3, 0, 4]
        self.memory_fifo = [-1] * self.frames  # FIFO memory
        self.memory_lru = [-1] * self.frames  # LRU memory
        self.memory_opt = [-1] * self.frames  # Optimal memory
        self.page_faults_fifo = 0
        self.page_faults_lru = 0
        self.page_faults_opt = 0
        self.current_step = 0
        self.max_steps = len(self.page_references)
        
        # Initialize figure
        self.fig = plt.figure(figsize=(18, 12))
        self.gs = GridSpec(3, 3, figure=self.fig, hspace=0.4, wspace=0.2)
        self.setup_axes()
        
        # Initial draw
        self.update_visualization()
        
    def setup_axes(self):
        """Create and style all axes"""
        self.axes = {
            'memory_fifo': self.fig.add_subplot(self.gs[0, 0]),
            'memory_lru': self.fig.add_subplot(self.gs[0, 1]),
            'memory_opt': self.fig.add_subplot(self.gs[0, 2]),
            'page_refs': self.fig.add_subplot(self.gs[1, :]),
            'stats': self.fig.add_subplot(self.gs[2, :])
        }
        
    def create_memory_table(self, ax, memory, title):
        """Create a table to display current memory frames"""
        ax.clear()
        ax.set_title(title, fontsize=14, pad=15)
        
        # Create table for memory state
        cell_text = [list(map(str, memory))]
        table = ax.table(cellText=cell_text, loc='center', cellLoc='center', colLabels=['Frame 1', 'Frame 2', 'Frame 3'])
        
        # Style table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor('#DDDDDD')
            if row == 0:
                cell.set_facecolor('#E1E1E1')  # Header style
            elif memory[col] == -1:  # Empty frame
                cell.set_facecolor('#F5F5F5')
            else:
                cell.set_facecolor('#B2FF66')  # Filled frame color
                
        ax.axis('off')
    
    def create_page_ref_sequence(self, ax):
        """Visualize the page reference sequence"""
        ax.clear()
        ax.set_title("Page Reference Sequence", fontsize=14, pad=15)
        
        ax.plot(range(len(self.page_references)), self.page_references, marker='o', linestyle='-', color='blue')
        ax.set_xticks(range(len(self.page_references)))
        ax.set_xticklabels(self.page_references, fontsize=12)
        ax.set_xlim(-0.5, len(self.page_references)-0.5)
        ax.set_ylim(min(self.page_references)-1, max(self.page_references)+1)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.set_facecolor('white')
        
        # Add current step info
        ax.text(0.98, 0.98, f"Step: {self.current_step+1}", ha='right', va='top', transform=ax.transAxes, fontsize=12, color='black')

    def create_stats(self, ax):
        """Display page faults count for all algorithms"""
        ax.clear()
        ax.set_title("Statistics", fontsize=14, pad=15)
        
        ax.text(0.3, 0.8, f"FIFO Faults: {self.page_faults_fifo}", ha='center', fontsize=12, color='black')
        ax.text(0.5, 0.8, f"LRU Faults: {self.page_faults_lru}", ha='center', fontsize=12, color='black')
        ax.text(0.7, 0.8, f"Optimal Faults: {self.page_faults_opt}", ha='center', fontsize=12, color='black')
        ax.axis('off')
    
    def fifo_step(self):
        """FIFO page replacement step"""
        page = self.page_references[self.current_step]
        if page not in self.memory_fifo:
            self.page_faults_fifo += 1
            if -1 in self.memory_fifo:  # If there's an empty frame
                empty_index = self.memory_fifo.index(-1)
                self.memory_fifo[empty_index] = page
            else:  # If no empty frame, replace the first page (FIFO logic)
                self.memory_fifo.pop(0)  
                self.memory_fifo.append(page)  

    def lru_step(self):
        """LRU page replacement step"""
        page = self.page_references[self.current_step]
        if page not in self.memory_lru:
            self.page_faults_lru += 1
            if -1 in self.memory_lru: 
                empty_index = self.memory_lru.index(-1)
                self.memory_lru[empty_index] = page
            else: 
                last_used = self.memory_lru.index(min(self.memory_lru, key=lambda x: self.page_references.index(x)))
                self.memory_lru[last_used] = page

    def optimal_step(self):
        """Optimal page replacement step"""
        page = self.page_references[self.current_step]
        if page not in self.memory_opt:
            self.page_faults_opt += 1
            if -1 in self.memory_opt: 
                empty_index = self.memory_opt.index(-1)
                self.memory_opt[empty_index] = page
            else:  
                future_use = [self.page_references[self.current_step + 1:].index(p) if p in self.page_references[self.current_step + 1:] else float('inf') for p in self.memory_opt]
                farthest_page = future_use.index(max(future_use))
                self.memory_opt[farthest_page] = page

    def page_replacement_step(self):
        """Call the appropriate page replacement algorithm step"""
        self.fifo_step()
        self.lru_step()
        self.optimal_step()

    def update_visualization(self):
        """Update all visualization components"""
        self.page_replacement_step()
        
        # Create and update tables for all algorithms
        self.create_memory_table(self.axes['memory_fifo'], self.memory_fifo, 'FIFO')
        self.create_memory_table(self.axes['memory_lru'], self.memory_lru, 'LRU')
        self.create_memory_table(self.axes['memory_opt'], self.memory_opt, 'Optimal')
        
        # Update page reference sequence and statistics
        self.create_page_ref_sequence(self.axes['page_refs'])
        self.create_stats(self.axes['stats'])
        
        plt.draw()
    
    def animate(self, i):
        """Function to update the animation every 15 seconds"""
        self.current_step = min(i, self.max_steps - 1)
        self.update_visualization()

# Create and show the visualization
plt.close('all')  # Close any existing figures
page_vis = PageReplacementVisualization()

# Create the animation, updating every 15 seconds
ani = FuncAnimation(page_vis.fig, page_vis.animate, frames=range(page_vis.max_steps), interval=7000, repeat=False)

plt.tight_layout()
plt.show()
