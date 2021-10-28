import matplotlib.pyplot as plt
import sys
from scipy.interpolate import splrep, splev


def create(file):
    healthy = []
    infected = []
    cured = []
    exposed = []
    dead = []
    time = []

    with open(f"{file}", "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.split(", ")
        healthy.append(int(line[0]))
        infected.append(int(line[1]))
        cured.append(int(line[2]))
        exposed.append(int(line[3]))
        dead.append(int(line[4]))
        time.append(float(line[5].strip("\n")))
        

    # Making the curve smoother before ploting
    healthy_bspline = splrep(time, healthy, s=5000)
    healthy_smooth = splev(time, healthy_bspline)
    
    infected_bspline = splrep(time, infected, s=5000)
    infected_smooth = splev(time, infected_bspline)

    cured_bspline = splrep(time, cured, s=5000)
    cured_smooth = splev(time, cured_bspline)
    
    exposed_bspline = splrep(time, exposed, s=5000)
    exposed_smooth = splev(time, exposed_bspline)
    
    dead_bspline = splrep(time, dead, s=5000)
    dead_smooth = splev(time, dead_bspline)

    # Setting up plots
    #plt.plot(time, healthy, color="green")
    #plt.plot(time, infected, color="red")
    #plt.plot(time, cured, color="blue")
    #plt.plot(time, dead, color="black")
    plt.plot(time, healthy_smooth, label="Healthy", color="green")
    plt.plot(time, infected_smooth, label="Infected", color="red")
    plt.plot(time, exposed_smooth, label="Exposed", color="purple")
    plt.plot(time, cured_smooth, label="Immune", color="blue")
    plt.plot(time, dead_smooth, label="Dead", color="black")

    # Setting up graphic title and legend properties
    plt.title("Epidemic modeling (see modeling.py)", loc="center")
    plt.legend(loc="right")
    plt.pause(0.001)

    # Show plots
    plt.show()


if __name__ == "__main__":
    create(sys.argv[1])
