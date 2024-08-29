from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot

class GraphApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create a graph
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5, x_ticks_major=1,
                      y_ticks_major=1, y_grid_label=True, x_grid_label=True,
                      padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=5, ymin=-1, ymax=25)

        # Create a plot and add it to the graph
        plot = MeshLinePlot(color=[1, 0, 0, 1])  # Red color
        plot.points = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
        graph.add_plot(plot)

        layout.add_widget(graph)
        return layout

if __name__ == '__main__':
    GraphApp().run()