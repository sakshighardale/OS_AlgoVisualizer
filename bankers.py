import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, FancyBboxPatch

class BankersVisualization:
    def __init__(self):
        # Initialize data
        self.max_matrix = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
        self.allocation_matrix = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
        self.available_vector = np.array([3, 3, 2])
        self.need_matrix = self.max_matrix - self.allocation_matrix
        self.safe_sequence = [1, 3, 4, 0, 2]
        self.process_names = [f"P{i}" for i in range(len(self.max_matrix))]
        
        # Color scheme
        self.colors = {
            'background': '#F5F5F5',
            'text': '#333333',
            'highlight': '#FFD700',
            'completed': '#4CAF50',
            'executing': '#FFA500',
            'waiting': '#E0E0E0',
            'resources': ['#66B2FF', '#5CDB95', '#FF8C66'],
            'table_header': '#E1E1E1',
            'instruction_box': '#EEEEEE'
        }
        
        # Initialize figure
        self.fig = plt.figure(figsize=(18, 12), facecolor=self.colors['background'])
        self.gs = GridSpec(3, 3, figure=self.fig, hspace=0.4, wspace=0.2)
        self.setup_axes()
        self.add_instructions()
        
        # Animation state
        self.current_step = 0
        self.max_steps = len(self.safe_sequence) + 1
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        # Initial draw
        self.update_visualization()
        
    def setup_axes(self):
        """Create and style all axes"""
        self.axes = {
            'max': self.fig.add_subplot(self.gs[0, 0]),
            'allocation': self.fig.add_subplot(self.gs[0, 1]),
            'need': self.fig.add_subplot(self.gs[0, 2]),
            'resources': self.fig.add_subplot(self.gs[1, :]),
            'sequence': self.fig.add_subplot(self.gs[2, :])
        }
        
        # Style all axes
        for ax in self.axes.values():
            ax.set_facecolor(self.colors['background'])
    
    def add_instructions(self):
        """Add instructional text box"""
        instructions = [
            "Keyboard Controls:",
            "→ or ↓ : Next step",
            "← or ↑ : Previous step",
            "R : Reset animation",
            "",
            "Process States:",
            "Green: Completed safely",
            "Orange: Currently executing",
            "Gray: Waiting to be checked"
        ]
        
        instruction_text = "\n".join(instructions)
        self.fig.text(0.02, 0.02, instruction_text, 
                     ha='left', va='bottom', fontsize=11,
                     bbox=dict(facecolor=self.colors['instruction_box'], 
                              edgecolor='#CCCCCC', 
                              boxstyle='round,pad=0.5'))
    
    def create_matrix_table(self, ax, matrix, title, highlight_cell=None):
        """Create a styled matrix table with optional cell highlighting"""
        ax.clear()
        ax.set_title(title, fontsize=14, pad=15, color=self.colors['text'])
        
        # Create table
        cell_text = [[str(val) for val in row] for row in matrix]
        table = ax.table(cellText=cell_text, 
                        loc='center', 
                        cellLoc='center', 
                        colLabels=['R0', 'R1', 'R2'], 
                        rowLabels=self.process_names,
                        bbox=[0, 0, 1, 1])
        
        # Style table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        
        # Header styling
        for (row, col), cell in table.get_celld().items():
            if row == 0 or col == -1:  # Header row or column
                cell.set_facecolor(self.colors['table_header'])
                cell.set_text_props(weight='bold')
            cell.set_edgecolor('#DDDDDD')
            
            # Highlight specific cell if needed
            if highlight_cell and row == highlight_cell[0]+1 and col == highlight_cell[1]:
                cell.set_facecolor(self.colors['highlight'])
                cell.set_text_props(weight='bold')
        
        ax.axis('off')
    
    def create_resource_bars(self, ax):
        """Create horizontal resource bars with current values"""
        ax.clear()
        ax.set_title("Available Resources", fontsize=14, pad=15, color=self.colors['text'])
        
        # Calculate current available resources
        if self.current_step > 0 and self.current_step <= len(self.safe_sequence):
            current_available = self.available_vector.copy()
            for i in range(self.current_step):
                current_available += self.allocation_matrix[self.safe_sequence[i], :]
        else:
            current_available = self.available_vector.copy()
        
        # Create bars
        resources = ['R0', 'R1', 'R2']
        y_pos = np.arange(len(resources))
        bars = ax.barh(y_pos, current_available, 
                      color=self.colors['resources'], 
                      edgecolor='#333333', 
                      height=0.6)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 0.1, i, f'{width}', 
                   va='center', fontsize=12, color=self.colors['text'])
        
        # Style the plot
        ax.set_yticks(y_pos)
        ax.set_yticklabels(resources, fontsize=12)
        ax.set_xlim(0, max(current_available)*1.5)
        ax.grid(axis='x', linestyle=':', alpha=0.7)
        ax.set_facecolor(self.colors['background'])
        
        # Add current step info
        if 0 < self.current_step <= len(self.safe_sequence):
            ax.text(0.98, 0.95, f"After P{self.safe_sequence[self.current_step-1]} completes", 
                   ha='right', va='top', transform=ax.transAxes,
                   bbox=dict(facecolor=self.colors['instruction_box'], alpha=0.8))
    
    def create_process_sequence(self, ax):
        """Visualize the process sequence and status"""
        ax.clear()
        ax.set_title("Process Execution Sequence", fontsize=14, pad=15, color=self.colors['text'])
        ax.axis('off')
        
        # Layout parameters
        circle_radius = 0.08
        circle_spacing = 0.2
        start_x = 0.1
        start_y = 0.7
        
        # Draw process circles
        for i, process in enumerate(self.process_names):
            x = start_x + i * circle_spacing
            y = start_y
            
            # Determine status
            if self.current_step > 0 and i in self.safe_sequence[:self.current_step]:
                status = 'completed'
            elif self.current_step < len(self.safe_sequence) and i == self.safe_sequence[self.current_step]:
                status = 'executing'
            else:
                status = 'waiting'
            
            # Draw circle
            circle = plt.Circle((x, y), circle_radius, 
                               color=self.colors[status], 
                               ec='#333333', lw=1.5)
            ax.add_patch(circle)
            
            # Add process label
            ax.text(x, y, f"P{i}", ha='center', va='center', 
                   fontsize=12, color='black' if status != 'waiting' else '#666666')
            
            # Add resource needs if executing
            if status == 'executing':
                needs = self.need_matrix[i]
                ax.text(x, y - circle_radius - 0.05, 
                       f"Needs: {needs[0]},{needs[1]},{needs[2]}", 
                       ha='center', fontsize=10)
        
        # Draw sequence arrows
        if self.current_step > 0:
            for i in range(min(self.current_step, len(self.safe_sequence))):
                x1 = start_x + self.safe_sequence[i] * circle_spacing + circle_radius
                y1 = start_y
                x2 = start_x + (self.safe_sequence[i+1] * circle_spacing - circle_radius 
                               if i+1 < len(self.safe_sequence) else x1 + circle_spacing)
                y2 = y1
                
                if i+1 < len(self.safe_sequence):
                    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                              arrowprops=dict(arrowstyle="->", color='#333333', lw=1.5))
        
        # Display current safe sequence
        if self.current_step > 0:
            seq_text = "Current Safe Sequence: " + " → ".join([f"P{p}" for p in self.safe_sequence[:self.current_step]])
            ax.text(0.5, 0.3, seq_text, ha='center', fontsize=12, 
                   bbox=dict(facecolor=self.colors['instruction_box'], alpha=0.8))
        
        # Display final sequence if complete
        if self.current_step == len(self.safe_sequence):
            final_text = "Final Safe Sequence: " + " → ".join([f"P{p}" for p in self.safe_sequence])
            ax.text(0.5, 0.15, final_text, ha='center', fontsize=14,
                   bbox=dict(facecolor=self.colors['completed'], alpha=0.3))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    
    def update_visualization(self):
        """Update all visualization components"""
        # Highlight the current process being checked
        highlight_cell = None
        if self.current_step < len(self.safe_sequence):
            current_process = self.safe_sequence[self.current_step]
            highlight_cell = (current_process, 0)  # Highlight first column of the row
        
        # Update all components
        self.create_matrix_table(self.axes['max'], self.max_matrix, "Maximum Matrix")
        self.create_matrix_table(self.axes['allocation'], self.allocation_matrix, "Allocation Matrix")
        self.create_matrix_table(self.axes['need'], self.need_matrix, "Need Matrix", highlight_cell)
        self.create_resource_bars(self.axes['resources'])
        self.create_process_sequence(self.axes['sequence'])
        
        # Update main title
        if self.current_step < len(self.safe_sequence):
            title = f"Step {self.current_step+1}: Checking if P{self.safe_sequence[self.current_step]} can be allocated resources"
        elif self.current_step == len(self.safe_sequence):
            title = "Safety Check Complete - System is in Safe State"
        else:
            title = "Banker's Algorithm Visualization"
        
        self.fig.suptitle(title, fontsize=16, y=0.98, color=self.colors['text'])
        
        plt.draw()
    
    def on_key_press(self, event):
        """Handle keyboard navigation"""
        if event.key == 'right' or event.key == 'down':
            self.current_step = min(self.current_step + 1, self.max_steps)
        elif event.key == 'left' or event.key == 'up':
            self.current_step = max(self.current_step - 1, 0)
        elif event.key == 'r' or event.key == 'R':
            self.current_step = 0
        
        self.update_visualization()

# Create and show the visualization
plt.close('all')  # Close any existing figures
bankers_vis = BankersVisualization()
plt.tight_layout()
plt.show()