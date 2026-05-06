import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as funi
from matplotlib.ticker import MultipleLocator as loc
import numpy as np
from Drone import Drone
from Fleet import Fleet
from Package import Package
#Values for testing not related to code
"""routes = np.array([
    [(5, 0), (5, 20), (-10, 20), (-10, -10)],
    [(8, 0), (8, 15), (-5, 15)],
    [(0, 3), (-5, 3), (-5, 8)],
    [(0, 10), (10, 10), (10, -5)],
    [(-8, 0), (-8, 12), (4, 12)],])
test_obstacles=[(1,5),(2,3)]
Birds=Fleet()
Dr1=Drone("Condor",100,)
Dr2=Drone("Rooster",100,)
Dr3=Drone("Eagle",100,)
Dr4=Drone("Pigeon",100,)
Dr5=Drone("Lobster",100,)  #cause why not
Birds.add_drone(Dr1,Dr2,Dr3,Dr4,Dr5) """ #edited using *args cause i am too laze to type the function 5 times
"""    def add_drone(self, *args):
        for i in args:
            self.drones.append(i)
            """ #edited version
    
def simulation(routes,drones): #routes should be a list of lists or numpy arrays (arrays are faster so we should use them) and drones is a list of the drones going out could also use names in this case change label value to drones[i] in line 37
#error check
    if len(routes)!=len(drones):
        print("Error the amount of routes and drones aren't the same")
        return
# figure and axisflying_shit[drn]ects setup
    fig,ax=plt.subplots(layout="constrained",figsize=(14,10)) #constrained makes it so numbers don't overlap
    ax.grid() #disp grid
    ax.set_axisbelow(True) #makesflying_shit[drn]ects appear on top of grid
    ax.yaxis.set_major_locator(loc(1)) #forces axes to have values going up 1 each time
    ax.xaxis.set_major_locator(loc(1))
#The limit is to be changed later
    ax.set_xlim(-25,25)
    ax.set_ylim(-25,25)
#The Drones
    flying_shit=[]
    for i in range(len(drones)):
        flying_shit.append({"drone":ax.scatter([],[],s=100,color=(np.random.random(),np.random.random(),np.random.random()), edgecolors="black",label=drones[i].drone_id) , "done":False,"x":0,"y":0})
            #colors are randomized each time(otherwise i would have to use a list of colors or something)
    step = 20 #used to make values for smooth animation
    full_routes=[]
    for i in routes:
        full_routes.append(np.array([(0, 0)] + i + list(reversed(i)) +[(0, 0)])) #the routes with returning trip included
#assigning x and y coordinates
    for drn in range(len(flying_shit)):
        x, y = [], []
        route_pts = full_routes[drn]  # full round trip waypoints for this drone

        for i in range(len(route_pts) - 1):
            x0, y0 = route_pts[i]
            x1, y1 = route_pts[i + 1]
            dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            steps = max(int(dist * step / 2), 2)
            x.extend(np.linspace(x0, x1, steps, endpoint=False))
            y.extend(np.linspace(y0, y1, steps, endpoint=False))

        x.append(route_pts[-1][0])
        y.append(route_pts[-1][1])

        flying_shit[drn]["x"] = np.array(x)
        flying_shit[drn]["y"] = np.array(y)
    max_frames = max(len(flying_shit[drn]["x"]) for drn in range(len(flying_shit))) 
#the animation 
    def animate(frame):
        idk_what_to_name=[]
        for drn in range(len(flying_shit)):
            if not flying_shit[drn]["done"]:
                if frame != 0 and flying_shit[drn]["x"][frame]==0 and flying_shit[drn]["y"][frame]==0:
                    flying_shit[drn]["done"]=True
                    flying_shit[drn]["drone"].set_visible(False)
                else:
                   flying_shit[drn]["drone"].set_offsets((flying_shit[drn]["x"][frame],flying_shit[drn]["y"][frame]))
            idk_what_to_name.append(flying_shit[drn]["drone"])
        return idk_what_to_name
    
    ani= funi(fig,animate,frames=max_frames,blit=True, interval=5 )
#unimportant but kinda looks better than original
    plt.style.use("grayscale")
#displaying no fly zones as red squares
    xo,yo=zip(*test_obstacles) #change test_obstacles to the name of the no fly zones variable
    plt.scatter(xo,yo,color="red",s=50,marker="s",label="No Fly Zones")
    plt.legend()
    plt.show()
#remaining stuff:
#add the t so drones don't overlap
#make the x,y grid limits dynamic not fixed
#some optimization since the code slows a bit when many drones are added or limit the amount to on that runs well