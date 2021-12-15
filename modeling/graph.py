import matplotlib.pyplot as plt
import sys
from scipy.interpolate import splrep, splev


def create(file):
    susceptible = []
    infected = []
    recovered = []
    exposed = []
    dead = []
    time = []

    with open(f"{file}", "r") as f:
        lines = f.readlines()

        # In case the simulation has crashed and the logs couldn't be written we avoid adding another error message that would flood the console
        if not lines:
            sys.exit(1)

    for line in lines:
        line = line.split(", ")
        susceptible.append(int(line[0]))
        infected.append(int(line[1]))
        recovered.append(int(line[2]))
        exposed.append(int(line[3]))
        dead.append(int(line[4]))
        time.append(float(line[5].strip("\n")))

    # Making the curve smoother before ploting
    susceptible_bspline = splrep(time, susceptible, s=5000)
    susceptible_smooth = splev(time, susceptible_bspline)

    infected_bspline = splrep(time, infected, s=5000)
    infected_smooth = splev(time, infected_bspline)

    recovered_bspline = splrep(time, recovered, s=5000)
    recovered_smooth = splev(time, recovered_bspline)

    exposed_bspline = splrep(time, exposed, s=5000)
    exposed_smooth = splev(time, exposed_bspline)

    dead_bspline = splrep(time, dead, s=5000)
    dead_smooth = splev(time, dead_bspline)

    # Setting up plots

    # Not smoothed
    plt.plot(time, susceptible, "-", color="green", label="Susceptible")
    plt.plot(time, exposed, "-", color="magenta", label="Exposed")
    plt.plot(time, infected, "-", color="red", label="Infected")
    plt.plot(time, dead, "-", color="black", label="Dead")
    plt.plot(time, recovered, "-", color="blue", label="Recovered")

    # Smoothed
    plt.plot(time, susceptible_smooth, "--", label="_nolegend_", color="green")
    plt.plot(time, exposed_smooth, "--", label="_nolegend_", color="magenta")
    plt.plot(time, infected_smooth, "--", label="_nolegend_", color="red")
    plt.plot(time, dead_smooth, "--", label="_nolegend_", color="black")
    plt.plot(time, recovered_smooth, "--", label="_nolegend_", color="blue")

    # Setting up graphic title and legend properties
    plt.title(label="SEIDR Simulation results", loc="center")
    plt.xlabel("Time (days)")
    plt.ylabel("SEIDR Populations")
    plt.legend(loc="right")
    plt.pause(0.001)

    # Show plots
    plt.show()


if __name__ == "__main__":
    create(sys.argv[1])
