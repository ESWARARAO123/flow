import sys
from PyQt6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene,
    QGraphicsEllipseItem, QGraphicsTextItem, QMainWindow, 
    QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtGui import QPen, QColor, QFont, QPainterPath, QBrush
from PyQt6.QtCore import Qt

# Define functions for each pipeline step
def initialization():
    return "Initialization complete."

def synthesis():
    return "Synthesis complete."

def lec1():
    return "LEC1 complete."

def floor_plan():
    return "Floor Plan complete."

def lec2():
    return "LEC2 complete."

def placement():
    return "Placement complete."

def cts():
    return "CTS complete."

def route():
    return "Route complete."

def rcext():
    return "RCEXT complete."

def sta():
    return "STA complete."

def pdv():
    return "PDV complete."

def emir():
    return "EMIR complete."

def lec3():
    return "LEC3 complete."

def power_analysis():
    return "Power Analysis complete."

# Step functions dictionary
step_functions = {
    "Initialization": initialization,
    "Synthesis": synthesis,
    "LEC1": lec1,
    "Floor Plan": floor_plan,
    "LEC2": lec2,
    "Placement": placement,
    "CTS": cts,
    "Route": route,
    "RCEXT": rcext,
    "STA": sta,
    "PDV": pdv,
    "EMIR": emir,
    "LEC3": lec3,
    "Power Analysis": power_analysis
}

# Define step dependencies
steps_dependencies = {
    "Initialization": [],
    "Synthesis": ["Initialization"],
    "LEC1": ["Synthesis"],
    "Floor Plan": ["Synthesis"],
    "LEC2": ["Floor Plan"],
    "Placement": ["Floor Plan"],
    "CTS": ["Placement"],
    "Route": ["CTS"],
    "RCEXT": ["Route"],
    "STA": ["RCEXT"],
    "PDV": ["STA"],
    "EMIR": ["PDV"],
    "Power Analysis": ["EMIR"]
}

class PipelineTree(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pipeline Flow with Branches")
        self.setGeometry(100, 100, 1000, 1000)
        
        # Set up graphics view and scene
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        
        # Set up layout and widgets
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.graphics_view)
        
        # Output display
        self.output_label = QLabel("Output:")
        layout.addWidget(self.output_label)
        
        self.setCentralWidget(central_widget)
        self.create_pipeline_flow()

    def create_pipeline_flow(self):
        # Define step positions
        step_positions = {
            "Initialization": (400, 50), "Synthesis": (400, 150),
            "LEC1": (300, 250), "Floor Plan": (500, 250),
            "LEC2": (500, 350), "Placement": (400, 350),
            "CTS": (400, 450), "Route": (400, 550),
            "RCEXT": (400, 650), "STA": (400, 750),
            "PDV": (400, 850), "EMIR": (400, 950),
            "Power Analysis": (400, 1050)
        }

        pen = QPen(Qt.GlobalColor.blue)
        pen.setWidth(2)
        brush = QBrush(QColor(51, 153, 255))

        # Draw nodes and store references
        self.nodes = {}
        for step, (x, y) in step_positions.items():
            node = QGraphicsEllipseItem(x - 20, y - 20, 40, 40)
            node.setPen(pen)
            node.setBrush(brush)
            self.graphics_scene.addItem(node)
            self.nodes[step] = (node, x, y)
            
            label = QGraphicsTextItem(step)
            label.setDefaultTextColor(Qt.GlobalColor.white)
            label.setFont(QFont("Arial", 10))
            label.setPos(x - 20 + 5, y - 20 + 5)
            self.graphics_scene.addItem(label)
            label.mousePressEvent = lambda event, step=step: self.execute_flow_from_step(step)
        
        # Draw arrows for dependencies
        self.draw_arrows(step_positions)

    def draw_arrows(self, step_positions):
        arrow_pen = QPen(Qt.GlobalColor.black)
        arrow_pen.setWidth(2)
        
        for step, dependencies in steps_dependencies.items():
            for dep in dependencies:
                # Get positions
                start_x, start_y = step_positions[dep]
                end_x, end_y = step_positions[step]
                
                # Draw arrow line
                path = QPainterPath()
                path.moveTo(start_x, start_y)
                path.lineTo(end_x, end_y)
                arrow = self.graphics_scene.addPath(path, arrow_pen)
                
                # Add arrowhead
                arrowhead = QGraphicsEllipseItem(end_x - 5, end_y - 5, 10, 10)
                arrowhead.setBrush(QBrush(Qt.GlobalColor.black))
                self.graphics_scene.addItem(arrowhead)

    def execute_flow_from_step(self, start_step):
        self.output_label.setText("Output:")
        output = self.execute_step_and_dependents(start_step)
        self.output_label.setText(f"Output:\n{output}")

    def execute_step_and_dependents(self, step_name):
        if step_name in step_functions:
            # Execute the current step and get its result
            result = step_functions[step_name]()  
            output = f"{step_name}: {result}\n"
            
            # Find dependent steps and execute them recursively
            dependents = [s for s, deps in steps_dependencies.items() if step_name in deps]
            for dependent in dependents:
                output += self.execute_step_and_dependents(dependent)
            
            return output
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipelineTree()
    window.show()
    sys.exit(app.exec())

