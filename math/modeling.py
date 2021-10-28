# -------------------- IMPORTS --------------------


from random import randint, random
from matplotlib import pyplot as plt, animation as anim
import math
import sys


# --------------------  GLOBAL PARAMETERS (DO NOT TOUCH) --------------------


logs = []

file = sys.argv[1]
parameters = []

with open(file, "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        parameters.append(line)

transmission_rate = int(parameters[0]) / 100  # Chance of a dot to be infected
time_to_cure = int(parameters[2])  # Time to cure a dot
virus_mortality = (
    int(parameters[1]) / 1000 / time_to_cure
)  # Chance of a dot to die per tick

immunity_duration = int(parameters[3])  # Time before being contagious again
number_of_dots = int(parameters[4])  # number of dots to generate
minimal_distance = int(
    parameters[5]
)  # Minimal distance at initialization and for contamination
initial_infected_population = int(parameters[6])
masked_population = int(parameters[7])
incubation_duration = int(parameters[8])
shape = parameters[9]  # tip: use '.' instead if you put a value < 3 in minimal_distance
maskedShape = "P"

# For masked population
transmission_rate_masked = (
    transmission_rate * 0.2
)  # Chance of a masked dot to be infected


# --------------------  GLOBAL VARIABLES --------------------


HEIGHT_WIDTH = 100  # Window height and width (yes, window shape must be a square)
BORDER_MIN = 1  # minimum distance from the border
BORDER_MAX = HEIGHT_WIDTH - 1  # maximum distance from the border

time = 0  # Time to initialize
time_step = 0.1  # Time step for the simulation


# -------------------- CLASSES & METHODS --------------------


class Dot:
    def __init__(self, x: int, y: int) -> None:
        """Constructor for the Dot class

        Args:
            x (int): abscissa of the dot
            y (int): ordinate of the dot
        """
        self.x = x
        self.y = y
        self.velx = (random() - 0.5) / 5
        self.vely = (random() - 0.5) / 5
        self.is_infected = False
        self.infected_at = -1
        self.has_been_infected = False
        self.cured_at = -1
        self.wears_mask = False

    @staticmethod
    def init_checker(x: float, y: float, already_used_coords: list) -> bool:
        """Checks if the dot is in a distance of a minimal_distance from another dot

        Args:
            x (float): abscissa of the first dot
            y (float): ordinate of the first dot
            already_used_coords (list): list of already occupied coordinates (by initialized dots)

        Returns:
            boolean: Whether the Dot should be initialized or not
        """
        for coord in already_used_coords:
            a = Dot(x, y)
            if a.get_distance(coord[0], coord[1]) < minimal_distance:
                return False
        return True

    def get_distance(self, x: float, y: float) -> float:
        """Gets the distance between a dot and coordinates objects

        Args:
            x (float): abscissa of the first dot
            y (float): ordinate of the first dot

        Returns:
            float: distance between the two dots
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    @staticmethod
    def initalize_multiple_dots() -> list:
        """Generates a list of Dots

        Returns:
            list: initialized dots
        """
        dots = []
        already_used_coords = []

        while len(dots) != number_of_dots:
            randx = randint(BORDER_MIN, BORDER_MAX)
            randy = randint(BORDER_MIN, BORDER_MAX)
            # So the dots keep distances between each other
            if Dot.init_checker(randx, randy, already_used_coords):
                dot = Dot(randx, randy)
                already_used_coords.append((randx, randy))
            else:
                continue
            dots.append(dot)

        return dots

    def try_infect(self) -> None:
        """Tries to infect a dot (if it's "eligible")"""
        near_infected_dots_list = [
            dot
            for dot in dots
            if dot.is_infected and self.get_distance(dot.x, dot.y) < minimal_distance
        ]

        for dot in near_infected_dots_list:
            if (
                dot.wears_mask and random() < transmission_rate_masked
            ) or not dot.wears_mask:
                self.is_infected = True
                self.infected_at = time
                break
            break

    def move(self) -> None:
        """Moves the dot and makes sure they don't go out of the area or touch each other. They've 4% chance to change direction."""
        if random() < 0.96:
            self.x += self.velx
            self.y += self.vely

        else:
            self.x = self.x + self.velx
            self.y = self.y + self.vely
            # Change 2 to lower value to make the dots go faster
            self.velx = (random() - 0.5) / (2 / (time_step + 1))
            # Change 2 to lower value to make the dots go faster
            self.vely = (random() - 0.5) / (2 / (time_step + 1))

        if self.x >= BORDER_MAX:
            self.x = BORDER_MAX
            self.velx *= -1

        if self.x <= BORDER_MIN:
            self.x = BORDER_MIN
            self.velx *= -1

        if self.y >= BORDER_MAX:
            self.y = BORDER_MAX
            self.vely *= -1

        if self.y <= BORDER_MIN:
            self.y = BORDER_MIN
            self.vely *= -1

    def kill(self) -> None:
        """Kills the dot"""
        global dead_dots_list
        dead_dots_list.append(self)
        dots.remove(self)

    def become_immune(self) -> None:
        """Makes the dot immune"""
        self.is_infected = False
        self.has_been_infected = True
        self.cured_at = time

    def become_healthy(self) -> None:
        """Makes the dot healthy"""
        self.has_been_infected = False
        self.infected_at = -1
        self.cured_at = -1

    def update_state(self) -> None:
        """Updates the state of the dot"""
        if -time_step < time - math.floor(time) < time_step:
            if self.is_infected and random() < virus_mortality:
                self.kill()

            if (not self.has_been_infected and not self.is_infected) and (
                (self.wears_mask and random() < transmission_rate_masked)
                or (not self.wears_mask and random() < transmission_rate)
            ):
                Dot.try_infect(self)

        if (
            self.is_infected
            and self.infected_at != -1
            and self.infected_at + time_to_cure < time
        ):
            self.become_immune()

        if (
            self.has_been_infected
            and self.cured_at != -1
            and self.cured_at + immunity_duration < time
        ):
            self.become_healthy()

    @staticmethod
    def move_all(dots: list) -> None:
        """Moves a given list of dots. Also applies everything that goes with moving (kills, infects, etc.)

        Args:
            dots (list): List of Dot objects
        """
        for dot in dots:
            dot.move()

            dot.update_state()

        update_data()

        update_values()


def should_i_stop(number_of_healthy_dots, number_of_alive_dots) -> bool:
    """Checks if the simulation should stop"""
    if number_of_healthy_dots == number_of_alive_dots:
        sys.exit(0)


def update_values() -> None:
    """Updates the values of the counters"""
    number_of_alive_dots = len(dots)
    number_of_healthy_dots = len(
        [dot for dot in dots if not dot.is_infected and not dot.has_been_infected]
    )
    number_of_infected_dots = len([dot for dot in dots if dot.is_infected])
    number_of_cured_dots = len([dot for dot in dots if dot.has_been_infected])
    number_of_exposed_dots = len([dot for dot in dots if dot.is_infected and dot.infected_at + incubation_duration > time])
    number_of_dead_dots = len([dot for dot in dead_dots_list])

    plt.title(
        f"Healthy: {number_of_healthy_dots}"
        + f"   |   Exposed: {number_of_exposed_dots}"
        + f"   |   Infected: {number_of_infected_dots}"
        + f"   |   Cured: {number_of_cured_dots}"
        + f"   |   Dead: {number_of_dead_dots}"
        + f"   |   Days: {round(time)}"
    )

    write_logs(
        number_of_healthy_dots,
        number_of_infected_dots,
        number_of_cured_dots,
        number_of_exposed_dots,
        number_of_dead_dots,
        time,
    )

    should_i_stop(number_of_healthy_dots, number_of_alive_dots)


def update_data() -> None:
    """Updates the data of the plot"""
    global healthy_dots, infected_dots, cured_dots, time, dead_dots, dots_area, healthy_dots, infected_dots, cured_dots, dead_dots_masked, incubation_dots, incubation_dots_masked

    healthy_dots.set_data(
        [
            dot.x
            for dot in dots
            if not dot.is_infected and not dot.has_been_infected and not dot.wears_mask
        ],
        [
            dot.y
            for dot in dots
            if not dot.is_infected and not dot.has_been_infected and not dot.wears_mask
        ],
    )

    infected_dots.set_data(
        [dot.x for dot in dots if dot.is_infected and not dot.wears_mask],
        [dot.y for dot in dots if dot.is_infected and not dot.wears_mask],
    )

    cured_dots.set_data(
        [dot.x for dot in dots if dot.has_been_infected and not dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and not dot.wears_mask],
    )
    
    incubation_dots.set_data(
        [dot.x for dot in dots if dot.is_infected and not dot.wears_mask and dot.infected_at + incubation_duration > time],
        [dot.y for dot in dots if dot.is_infected and not dot.wears_mask and dot.infected_at + incubation_duration > time]
    )


    dead_dots.set_data(
        [dot.x for dot in dead_dots_list if not dot.wears_mask],
        [dot.y for dot in dead_dots_list if not dot.wears_mask],
    )

    # For masked dots

    healthy_dots_masked.set_data(
        [
            dot.x
            for dot in dots
            if not dot.is_infected and not dot.has_been_infected and dot.wears_mask
        ],
        [
            dot.y
            for dot in dots
            if not dot.is_infected and not dot.has_been_infected and dot.wears_mask
        ],
    )

    infected_dots_masked.set_data(
        [dot.x for dot in dots if dot.is_infected and dot.wears_mask],
        [dot.y for dot in dots if dot.is_infected and dot.wears_mask],
    )

    cured_dots_masked.set_data(
        [dot.x for dot in dots if dot.has_been_infected and dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and dot.wears_mask],
    )
    
    incubation_dots_masked.set_data(
        [dot.x for dot in dots if dot.is_infected and dot.wears_mask and dot.infected_at + incubation_duration < time],
        [dot.y for dot in dots if dot.is_infected and dot.wears_mask and dot.infected_at + incubation_duration < time]
    )

    dead_dots_masked.set_data(
        [dot.x for dot in dead_dots_list if dot.wears_mask],
        [dot.y for dot in dead_dots_list if dot.wears_mask],
    )

    time += time_step


def write_logs(
    number_of_healthy_dots: int,
    number_of_infected_dots: int,
    number_of_cured_dots: int,
    number_of_exposed_dots: int,
    number_of_dead_dots: int,
    time: float,
) -> None:
    """Writes logs to a file

    Args:
        number_of_healthy_dots (int): Number of healthy dots
        number_of_infected_dots (int): Number of infected dots
        number_of_cured_dots (int): Number of cured dots
        number_of_exposed_dots (int): Number of exposed dots
        number_of_dead_dots (int): Number of dead dots
        time (float): Time in days
    """
    with open("files\\logs.txt", "a") as f:
        f.write(
            f"{number_of_healthy_dots}, {number_of_infected_dots}, {number_of_cured_dots}, {number_of_exposed_dots}, {number_of_dead_dots}, {time}\n"
        )


def generate_not_taken_index(index_list: list) -> int:
    """Generates an index that has not been taken yet

    Args:
        index_list (list): List of taken indices

    Returns:
        int: Index that has not been taken yet
    """
    while True:
        index = randint(0, len(dots) - 1)
        if index not in index_list:
            return index


# -------------------- MAIN FUNCTION --------------------


def main() -> None:
    """Main function"""
    global dots, dead_dot, graph, dots_area

    # Dots initialization
    dots = Dot.initalize_multiple_dots()

    already_used_indexes = []
    for _ in range(initial_infected_population):

        rdm = generate_not_taken_index(already_used_indexes)

        dots[rdm].is_infected = True
        dots[rdm].infected_at = time
        already_used_indexes.append(rdm)

    already_used_indexes = []
    for _ in range(masked_population):

        rdm = generate_not_taken_index(already_used_indexes)

        dots[rdm].wears_mask = True
        already_used_indexes.append(rdm)

    # Graph initialization
    figure_dots = plt.figure(facecolor="white", figsize=(8, 6))
    dots_area = plt.axes(xlim=(0, HEIGHT_WIDTH), ylim=(0, HEIGHT_WIDTH))

    # Differentiating dots between each others
    global healthy_dots
    healthy_dots = dots_area.plot(
        [dot.x for dot in dots if not dot.is_infected and not dot.wears_mask],
        [dot.y for dot in dots if not dot.is_infected and not dot.wears_mask],
        f"g{shape}",
    )[0]

    global infected_dots
    infected_dots = dots_area.plot(
        [dot.x for dot in dots if dot.is_infected and not dot.wears_mask],
        [dot.y for dot in dots if dot.is_infected and not dot.wears_mask],
        f"r{shape}",
    )[0]

    global cured_dots
    cured_dots = dots_area.plot(
        [dot.x for dot in dots if dot.has_been_infected and not dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and not dot.wears_mask],
        f"b{shape}",
    )[0]

    global incubation_dots
    incubation_dots = dots_area.plot(
        [dot.x for dot in dots if dot.has_been_infected and not dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and not dot.wears_mask],
        f"m{shape}",
    )[0]

    global dead_dots_list, dead_dots
    dead_dots_list = []
    dead_dots = dots_area.plot(
        [dot.x for dot in dead_dots_list if not dot.wears_mask],
        [dot.y for dot in dead_dots_list if not dot.wears_mask],
        f"k{shape}",
    )[0]

    # For masked population

    global healthy_dots_masked
    healthy_dots_masked = dots_area.plot(
        [dot.x for dot in dots if not dot.is_infected and dot.wears_mask],
        [dot.y for dot in dots if not dot.is_infected and dot.wears_mask],
        f"g{maskedShape}",
    )[0]

    global infected_dots_masked
    infected_dots_masked = dots_area.plot(
        [dot.x for dot in dots if dot.is_infected and dot.wears_mask],
        [dot.y for dot in dots if dot.is_infected and dot.wears_mask],
        f"r{maskedShape}",
    )[0]

    global cured_dots_masked
    cured_dots_masked = dots_area.plot(
        [dot.x for dot in dots if dot.has_been_infected and dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and dot.wears_mask],
        f"b{maskedShape}",
    )[0]
    
    global incubation_dots_masked
    incubation_dots_masked = dots_area.plot(
        [dot.x for dot in dots if dot.has_been_infected and dot.wears_mask],
        [dot.y for dot in dots if dot.has_been_infected and dot.wears_mask],
        f"m{maskedShape}",
    )[0]

    global dead_dots_masked
    dead_dots_masked = dots_area.plot(
        [dot.x for dot in dead_dots_list if dot.wears_mask],
        [dot.y for dot in dead_dots_list if dot.wears_mask],
        f"k{maskedShape}",
    )[0]

    # We need to keep this in an unused variable, otherwise the function won't work
    _ = anim.FuncAnimation(
        figure_dots, lambda z: Dot.move_all(dots), frames=60, interval=0
    )
    dots_area.axis("off")
    plt.show()


# -------------------- MAIN CALL --------------------


if __name__ == "__main__":
    main()
