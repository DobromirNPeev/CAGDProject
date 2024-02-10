import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider,Button
import copy

class DraggablePoint:
    def __init__(self, ax, x, y, size=100, color="red", marker="o"):
        self.ax = ax
        self.x=x
        self.y=y
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
        if not event.xdata or not event.ydata:
            return
        global points
        new_x = event.xdata + self.press[0]
        new_y = event.ydata + self.press[1]
        for point in points:
            if point[0]==self.x and point[1]==self.y:
                point[0]=new_x
                point[1]=new_y
                break
        self.x=new_x
        self.y=new_y
        redraw()
        if self.dragging:
            self.dragging = False
            self.press = None

def redraw():
    control_points_updated = np.array(points)

    displaced_control_points = displace_control_points(control_points_updated, t)
    updated_curve_points = bezier_curve(control_points_updated, t_values)
    updated_polar_points = bezier_curve(displaced_control_points, t_values)

    curve.set_xdata(updated_curve_points[:, 0])
    curve.set_ydata(updated_curve_points[:, 1])

    polar.set_xdata(updated_polar_points[:, 0])
    polar.set_ydata(updated_polar_points[:, 1])
            
    control_polygon.set_xdata(control_points_updated[:, 0])
    control_polygon.set_ydata(control_points_updated[:, 1])

    control_polar_polygon.set_xdata(displaced_control_points[:, 0])
    control_polar_polygon.set_ydata(displaced_control_points[:, 1])

    polar_pts.set_xdata(displaced_control_points[:, 0])
    polar_pts.set_ydata(displaced_control_points[:, 1])
    fig.canvas.draw_idle() 
    
def de_casteljau(control_points, t):
    n = len(control_points) - 1
    
    if n == 0:
        return control_points[0]
    
    intermediate_points = []
    for i in range(n):
        intermediate_point = (1 - t) * control_points[i] + t * control_points[i + 1]
        intermediate_points.append(intermediate_point)
    return de_casteljau(intermediate_points, t)

def bezier_curve(control_points, t_values):
    curve_points = []
    for t in t_values:
        point = de_casteljau(control_points, t)
        curve_points.append(point)
    return np.array(curve_points)

def displace_control_points(original_points, t):
    displaced_points = []
    for i in range(len(original_points)-1):
        direction = original_points[i+1] - original_points[i]
        displaced_point = original_points[i] + t * direction
        displaced_points.append(displaced_point)
    return np.array(displaced_points)

def update(val):
    global t
    t = val
    redraw()

def add_point(event):
    global points,drawnPoints,ax
    global add_point_enabled
    if event.button == 1 and add_point_enabled:
        x, y = event.xdata, event.ydata
        new_point = [x, y]
        (xm,ym),(xM,yM) =  button_add_point.label.clipbox.get_points()
        if x is None or y is None:
            return
        if xm<event.x<xM and ym<event.y<yM:
            toggle_add_point()
            return
        points.append(new_point)
        drawnPoints.append(DraggablePoint(ax,x,y))
        redraw()

def remove_last_point(event):
    if len(points) >2:
        points.pop() 
        point=drawnPoints.pop()
        point.point.remove()
        redraw()

def toggle_visibility(event):
    current_visibility_polar = polar.get_visible()
    current_visibility_polar_pts = polar_pts.get_visible() 
    current_visibility_control_polar_polygon=control_polar_polygon.get_visible()
    polar.set_visible(not current_visibility_polar)
    polar_pts.set_visible(not current_visibility_polar_pts)
    control_polar_polygon.set_visible(not current_visibility_control_polar_polygon)
    plt.draw()

def set_preset(name):
    global points,drawnPoints
    for point in drawnPoints:
        point.point.remove()
    drawnPoints.clear()
    points=copy.deepcopy(preset[name])
    for point in points:
        drawnPoints.append(DraggablePoint(ax,point[0],point[1]))

def set_preset1(event):
    set_preset('preset1')
    redraw()

def set_preset2(event):
    set_preset('preset2')
    redraw()

def set_preset3(event):
    set_preset('preset3')
    redraw()

def set_preset4(event):
    set_preset('preset4')
    redraw()

def toggle_add_point(event):
    global add_point_enabled
    add_point_enabled = not add_point_enabled
    if add_point_enabled:
        button_add_point.label.set_text("Add point (enabled)")
    else:
        button_add_point.label.set_text("Add point (disabled)")

preset4=[[0, 0], [0, 5], [5, 5],[5,0],[1.5,3]]
preset3=[[0, 0], [0, 5], [5, 5],[5,0]]
preset2=[[0, 0], [0, 5], [5, 5]]
preset1=[[0, 0], [0, 5]]
preset = { "preset1" : preset1, "preset2" : preset2, "preset3" : preset3, "preset4" : preset4}
points=copy.deepcopy(preset["preset2"])
add_point_enabled = False 
original_control_points = np.array(points)

t = 0.5

displaced_control_points = displace_control_points(original_control_points, t)

t_values = np.linspace(0, 1, 100)
original_curve_points = bezier_curve(original_control_points, t_values)
modified_curve_points = bezier_curve(displaced_control_points, t_values)


fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.axis("off")
drawnPoints=[]

curve,=plt.plot(original_curve_points[:, 0], original_curve_points[:, 1], 'r-', label='Original Bézier Curve')
for point in points:
    drawnPoints.append(DraggablePoint(ax,point[0],point[1]))
control_polygon,=plt.plot(original_control_points[:, 0], original_control_points[:, 1], 'r', label='Control Polygon')
polar,=plt.plot(modified_curve_points[:, 0], modified_curve_points[:, 1], 'g-', label=f'Modified Bézier Curve (t={t})')
polar_pts,= ax.plot(displaced_control_points[:, 0], displaced_control_points[:, 1], 'bo', label='Control Polar Points')
control_polar_polygon,=plt.plot(displaced_control_points[:, 0], displaced_control_points[:, 1], 'b', label='Control Polar Polygon')

axred = plt.axes([0.25, 0.05 ,0.65, 0.03])
slider = Slider(axred, 't:', 0.0, 1.0)
slider.on_changed(update)

ax_button = plt.axes([0.11, 0.025, 0.1, 0.04])
button_add_point = Button(ax_button, 'Add Point (disabled)', color='lightgray', hovercolor='lightblue')
button_add_point.on_clicked(toggle_add_point)

ax_button = plt.axes([0.11, 0.125, 0.1, 0.04])
button_toggle = Button(ax_button, 'Hide/Show Polar', color='lightgray', hovercolor='lightblue')
button_toggle.on_clicked(toggle_visibility)

polar.set_visible(False)
polar_pts.set_visible(False)
control_polar_polygon.set_visible(False)

ax_button_remove = plt.axes([0.11, 0.075, 0.10, 0.04])
button_remove_point = Button(ax_button_remove, 'Remove Point', color='lightgray', hovercolor='lightblue')
button_remove_point.on_clicked(remove_last_point)

ax_button_preset1 = plt.axes([0.005, 0.025, 0.1, 0.04])
button_preset1= Button(ax_button_preset1, 'Preset 1', color='lightgray', hovercolor='lightblue')
button_preset1.on_clicked(set_preset1)
ax_button_preset2 = plt.axes([0.005, 0.075, 0.1, 0.04])
button_preset2= Button(ax_button_preset2, 'Preset 2', color='lightgray', hovercolor='lightblue')
button_preset2.on_clicked(set_preset2)
ax_button_preset3 = plt.axes([0.005, 0.125, 0.1, 0.04])
button_preset3= Button(ax_button_preset3, 'Preset 3', color='lightgray', hovercolor='lightblue')
button_preset3.on_clicked(set_preset3)
ax_button_preset4 = plt.axes([0.005, 0.175, 0.1, 0.04])
button_preset4= Button(ax_button_preset4, 'Preset 4', color='lightgray', hovercolor='lightblue')
button_preset4.on_clicked(set_preset4)

plt.legend()
plt.grid(False)
plt.gcf().canvas.mpl_connect('button_press_event', add_point)
plt.show()
