import matplotlib.pyplot as plt

class DraggablePoint:
    def __init__(self, ax, x, y, size=100, color="red", marker="o"):
        self.ax = ax
        self.point = ax.scatter(x, y, s=size, c=color, marker=marker, picker=True)
        self.dragging = False
        self.press = None

        self.connect_events()

    def connect_events(self):
        self.ax.figure.canvas.mpl_connect('pick_event', self.on_pick)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_pick(self, event):
        if event.artist == self.point:
            self.dragging = True
            self.press = (self.point.get_offsets()[0][0] - event.mouseevent.xdata,
                          self.point.get_offsets()[0][1] - event.mouseevent.ydata)

    def on_motion(self, event):
        if self.dragging:
            new_x = event.xdata + self.press[0]
            new_y = event.ydata + self.press[1]
            self.point.set_offsets([[new_x, new_y]])
            self.ax.figure.canvas.draw()

    def on_release(self, event):
        if self.dragging:
            self.dragging = False
            self.press = None

def main():
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    draggable_point = DraggablePoint(ax, x=5, y=5)

    plt.show()

if __name__ == "__main__":
    main()
