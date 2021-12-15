# -------------------- IMPORTS --------------------


from random import randint, random, uniform
from matplotlib import pyplot as plt, animation as anim
from matplotlib.widgets import Button
import math
import sys
import numpy as np


# --------------------  GLOBAL VARIABLES --------------------


HEIGHT_WIDTH = 100  # Window height and width (yes, window shape must be a square)
BORDER_MIN = 1  # minimum distance from the border
BORDER_MAX = HEIGHT_WIDTH - 1  # maximum distance from the border

time = 0  # Time to initialize
dots_spawn_spacing_constant = 2  # Spacing between dots when they spawn

time_used_to_update = 0
time_before_being_able_to_infect = 0.4  # Let's pretend that you can only infect people after this period of time (after having been infected) (in days)


# --------------------  GLOBAL PARAMETERS (RETRIVED FROM FILE) --------------------

logs = []

file = sys.argv[1]
parameters = []

with open(file, "r") as f:
    lines = f.readlines()

    # In case the config file is empty
    if not lines:
        sys.exit(1)

    for line in lines:
        line = line.replace("\n", "")
        parameters.append(line)

simulation_speed = float(parameters[10])
time_step = simulation_speed / 100  # Time step for the simulation
sim_values_over_time = []

transmission_rate = int(parameters[0]) / 100  # Chance of a dot to be infected

infected_duration = int(
    parameters[2]
)  # Time to cure a dot (during this time, dot is infected)
immunity_duration = int(parameters[3])  # Time before being contagious again
number_of_dots = int(parameters[4])  # number of dots to generate
minimal_distance = int(
    parameters[5]
)  # Minimal distance at initialization and for contamination
initial_infected_population = int(parameters[6])
masked_population = int(parameters[7])
exposed_duration = int(parameters[8])
shape = parameters[9]  # tip: use '.' instead if you put a value < 3 in minimal_distance
maskedShape = "P"

# For masked population
transmission_rate_masked = (
    transmission_rate * 0.2
)  # Chance of a masked dot to be infected and to infect a susceptible dot

mortality_rate = (
    int(parameters[1]) / 1000 / infected_duration
)  # Chance of a dot to die per tick

collision_enabled = bool(int(parameters[11]))
dots_same_speed = bool(int(parameters[12]))
infected_wear_mask = bool(int(parameters[13]))
infected_slowdown = bool(int(parameters[14]))
people_travel_slower = bool(int(parameters[15]))

auto_stop = bool(int(parameters[16]))
visual = bool(int(parameters[17]))

collision_distance = 1.3 if shape == "o" else 0.65


# -------------------- CLASSES & METHODS --------------------


class Movement:
    """Class that represents the movement of a dot"""

    def __init__(self) -> None:
        """Constructor for the Movement class"""
        self.chance_to_change_direction = uniform(0.85, 1)
        self.angle = uniform(0, 50)

        reduction_factor = 100 if not people_travel_slower else simulation_speed * 20

        self.initial_speed = (
            np.random.normal(
                loc=simulation_speed / reduction_factor, scale=100 / reduction_factor
            )
            if not dots_same_speed
            else simulation_speed / reduction_factor
        )  # Making speedy dots rarer
        self.speed = self.initial_speed

    def speed_back_to_normal(self) -> None:
        """Method that resets the speed back to its original value"""
        self.speed = self.initial_speed


class Dot:
    def __init__(self, x: int, y: int) -> None:
        """Constructor for the Dot class

        Args:
            x (int): abscissa of the dot
            y (int): ordinate of the dot
        """
        self.id = 0
        self.x = x
        self.y = y
        self.velx = (random() - 0.5) / 5
        self.vely = (random() - 0.5) / 5
        self.is_infected = False
        self.infected_at = -1
        self.has_been_infected = False
        self.recovered_at = -1
        self.wears_mask = False
        self.was_originally_wearing_mask = False
        self.movement = (
            Movement()
        )  # Default Movements values (change in Movement class to adjust their movements)

    @staticmethod
    def init_checker(x: float, y: float, already_used_coords: list) -> bool:
        """Checks if the dot is in a distance of the dots_spawn_spacing_constant from another dot

        Args:
            x (float): abscissa of the first dot
            y (float): ordinate of the first dot
            already_used_coords (list): list of already occupied coordinates (by initialized dots)

        Returns:
            boolean: Whether the Dot should be initialized or not
        """
        for coord in already_used_coords:
            a = Dot(x, y)
            if a.get_distance(coord[0], coord[1]) < dots_spawn_spacing_constant:
                return False
        return True

    def get_distance(self, x: float, y: float) -> float:
        """Gets the distance between a dot and coordinates objects

        Args:
            x (float): abscissa of the distant dot
            y (float): ordinate of the distant dot

        Returns:
            float: distance between the two dots
        """
        return math.hypot(
            x - self.x, y - self.y
        )  # Another way but more laggy: math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

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

    @staticmethod
    def get_all_susceptible() -> list:
        """Gets all the susceptible dots

        Returns:
            list: list of susceptible dots
        """
        return [
            dot for dot in dots if not dot.is_infected and not dot.has_been_infected
        ]

    @staticmethod
    def get_all_exposed() -> list:
        """Gets all the exposed dots

        Returns:
            list: list of exposed dots
        """
        return [dot for dot in dots if dot.is_only_exposed()]

    @staticmethod
    def get_all_infected() -> list:
        """Gets all the infected dots

        Returns:
            list: list of infected dots
        """
        return [dot for dot in dots if dot.is_infected and not dot.is_only_exposed()]

    @staticmethod
    def get_all_recovered() -> list:
        """Gets all the recovered dots

        Returns:
            list: list of recovered dots
        """
        return [dot for dot in dots if dot.has_been_infected]

    def is_only_exposed(self):
        """Returns true if the dot is asymptomatic, else return false"""
        return self.is_infected and self.infected_at + exposed_duration > time

    def try_infect(self) -> None:
        """Tries to infect a dot (if it's "eligible")"""
        near_infected_dots_list = [
            dot
            for dot in dots
            if dot.is_infected
            and self.get_distance(dot.x, dot.y) < minimal_distance
            and self.id != dot.id
            and self.infected_at + time_before_being_able_to_infect < time
        ]

        for dot in near_infected_dots_list:
            if (
                dot.wears_mask and random() < transmission_rate_masked
            ) or not dot.wears_mask:
                self.become_infected()
                break
            break

    def handle_collisions(self) -> None:
        """Handles collisions between dots"""
        # To avoid checking already checked dots, I check every iteration the id of the dot
        i = self.id
        while i < len(dots):
            dot = dots[i]
            if (
                self.id != dot.id
                and self.get_distance(dot.x, dot.y) < collision_distance
            ):
                # Whenever a dot makes contact with another dot, both will bounce back (their direction will be inverted)
                self.velx *= -1
                self.vely *= -1
                dot.velx *= -1
                dot.vely *= -1
                break
            i += 1

    def move(self) -> None:
        """Moves the dot and makes sure they don't go out of the area or touch each other.
        Their movements are determined by their Movement class attribute and a normal distribution
        """
        if random() >= self.movement.chance_to_change_direction:
            alpha = math.radians(np.random.normal(loc=0, scale=self.movement.angle))
            theta = math.atan2(self.vely, self.velx)
            norm = math.sqrt(self.velx ** 2 + self.vely ** 2)

            self.velx = norm * math.cos(theta + alpha)
            self.vely = norm * math.sin(theta + alpha)

        # Increment x and y by their velocities and time_step
        self.x += self.velx * ((simulation_speed * (1 + self.movement.speed)) / 10)
        self.y += self.vely * ((simulation_speed * (1 + self.movement.speed)) / 10)

        # Dots can collide each other
        if collision_enabled:
            self.handle_collisions()

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

    def become_infected(self) -> None:
        """Infects the dot"""
        self.is_infected = True
        self.infected_at = time

        if infected_slowdown:
            self.movement.speed *= 0.5  # Reduce speed by 50%

        if infected_wear_mask and not self.is_only_exposed():
            self.wears_mask = True

    def kill(self) -> None:
        """Kills the dot"""
        global dead_dots_list
        dead_dots_list.append(self)
        dots.remove(self)

    def become_recovered(self) -> None:
        """Makes the dot recovered"""
        self.is_infected = False
        self.has_been_infected = True
        self.recovered_at = time
        self.movement.speed_back_to_normal()

        if infected_wear_mask and not self.was_originally_wearing_mask:
            self.wears_mask = False

    def become_susceptible(self) -> None:
        """Makes the dot susceptible"""
        self.has_been_infected = False
        self.infected_at = -1
        self.recovered_at = -1

    def update_state(self) -> None:
        """Updates the state of the dot"""
        if (
            not self.is_only_exposed()
            and self.is_infected
            and random() <= mortality_rate
        ):
            self.kill()

        if (not self.has_been_infected and not self.is_infected) and (
            (self.wears_mask and random() < transmission_rate_masked)
            or (not self.wears_mask and random() < transmission_rate)
        ):
            self.try_infect()

        if (
            self.is_infected
            and self.infected_at != -1
            and self.infected_at + infected_duration < time
        ):
            self.become_recovered()

        if (
            self.has_been_infected
            and self.recovered_at != -1
            and self.recovered_at + immunity_duration < time
        ):
            self.become_susceptible()

    @staticmethod
    def move_all(dots: list) -> None:
        """Moves a given list of dots. Also applies everything that goes with moving (kills, infects, etc.)

        Args:
            dots (list): List of Dot objects
        """
        global time, time_used_to_update

        for dot in dots:
            dot.move()

            # When a day passed, update the state of the dots (at the end of the day, so before next day)
            if math.floor(time + time_step) == math.floor(time) + 1:
                dot.update_state()
                time_used_to_update = 0

        if visual:
            update_data()
            update_values()
        else:
            update_values_no_visual()

        if auto_stop:
            should_i_stop()

        time += time_step
        time_used_to_update += 1


def should_i_stop() -> None:
    """Check if simulation should stop (if auto_stop is enabled only)"""
    if (
        len([dot for dot in dots if dot.is_infected and not dot.is_only_exposed()]) == 0
        and time > exposed_duration
    ):
        stop()


def stop() -> None:
    """Stops the simulation"""
    write_logs()
    sys.exit(0)


def show_data(
    number_of_susceptible_dots,
    number_of_infected_dots,
    number_of_recovered_dots,
    number_of_exposed_dots,
    number_of_dead_dots,
    time,
) -> None:
    """Shows the data on prompt"""
    print(
        f"{number_of_susceptible_dots} susceptible, {number_of_infected_dots} infected, {number_of_recovered_dots} recovered, {number_of_exposed_dots} exposed, {number_of_dead_dots} dead, {int(time)} days"
    )


def update_values_no_visual() -> None:
    """Updates the values of the file"""
    number_of_susceptible_dots = len(Dot.get_all_susceptible())
    number_of_infected_dots = len(Dot.get_all_infected())
    number_of_recovered_dots = len(Dot.get_all_recovered())
    number_of_exposed_dots = len(Dot.get_all_exposed())
    number_of_dead_dots = len(dead_dots_list)

    sim_values_over_time.append(
        [
            number_of_susceptible_dots,
            number_of_infected_dots,
            number_of_recovered_dots,
            number_of_exposed_dots,
            number_of_dead_dots,
            time,
        ]
    )

    show_data(
        number_of_susceptible_dots,
        number_of_infected_dots,
        number_of_recovered_dots,
        number_of_exposed_dots,
        number_of_dead_dots,
        time,
    )


def update_values() -> None:
    """Updates the values of the plot counters"""
    number_of_susceptible_dots = len(Dot.get_all_susceptible())
    number_of_infected_dots = len(Dot.get_all_infected())
    number_of_recovered_dots = len(Dot.get_all_recovered())
    number_of_exposed_dots = len(Dot.get_all_exposed())
    number_of_dead_dots = len(dead_dots_list)

    dots_area.set_title(
        f"Susceptible: {number_of_susceptible_dots}"
        + f"   |   Exposed: {number_of_exposed_dots}"
        + f"   |   Infected: {number_of_infected_dots}"
        + f"   |   Recovered: {number_of_recovered_dots}"
        + f"   |   Dead: {number_of_dead_dots}"
        + f"   |   Days: {round(time)}"
    )

    sim_values_over_time.append(
        [
            number_of_susceptible_dots,
            number_of_infected_dots,
            number_of_recovered_dots,
            number_of_exposed_dots,
            number_of_dead_dots,
            time,
        ]
    )


def update_data() -> None:
    """Updates the data of the plot"""
    global susceptible_dots, infected_dots, recovered_dots, time, dead_dots, dots_area, susceptible_dots, infected_dots, recovered_dots, dead_dots_masked, exposed_dots, exposed_dots_masked

    susceptible_dots.set_data(
        [dot.x for dot in Dot.get_all_susceptible() if not dot.wears_mask],
        [dot.y for dot in Dot.get_all_susceptible() if not dot.wears_mask],
    )

    exposed_dots.set_data(
        [dot.x for dot in Dot.get_all_exposed() if not dot.wears_mask],
        [dot.y for dot in Dot.get_all_exposed() if not dot.wears_mask],
    )

    infected_dots.set_data(
        [
            dot.x
            for dot in Dot.get_all_infected()
            if not dot.wears_mask and not infected_wear_mask
        ],
        [
            dot.y
            for dot in Dot.get_all_infected()
            if not dot.wears_mask and not infected_wear_mask
        ],
    )

    recovered_dots.set_data(
        [dot.x for dot in Dot.get_all_recovered() if not dot.wears_mask],
        [dot.y for dot in Dot.get_all_recovered() if not dot.wears_mask],
    )

    dead_dots.set_data(
        [dot.x for dot in dead_dots_list if not dot.wears_mask],
        [dot.y for dot in dead_dots_list if not dot.wears_mask],
    )

    # For masked dots

    susceptible_dots_masked.set_data(
        [dot.x for dot in Dot.get_all_susceptible() if dot.wears_mask],
        [dot.y for dot in Dot.get_all_susceptible() if dot.wears_mask],
    )

    exposed_dots_masked.set_data(
        [dot.x for dot in Dot.get_all_exposed() if dot.wears_mask],
        [dot.y for dot in Dot.get_all_exposed() if dot.wears_mask],
    )

    infected_dots_masked.set_data(
        [
            dot.x
            for dot in Dot.get_all_infected()
            if dot.wears_mask or infected_wear_mask
        ],
        [
            dot.y
            for dot in Dot.get_all_infected()
            if dot.wears_mask or infected_wear_mask
        ],
    )

    recovered_dots_masked.set_data(
        [dot.x for dot in Dot.get_all_recovered() if dot.wears_mask],
        [dot.y for dot in Dot.get_all_recovered() if dot.wears_mask],
    )

    dead_dots_masked.set_data(
        [dot.x for dot in dead_dots_list if dot.wears_mask],
        [dot.y for dot in dead_dots_list if dot.wears_mask],
    )


def write_logs() -> None:
    """Write simulation logs to text file."""
    with open("files\\logs.txt", "a") as f:
        for values in sim_values_over_time:
            f.write(
                f"{values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}\n"
            )


def generate_not_taken_index(index_list: list) -> int:
    """Generates a random index that has not been taken yet.

    Args:
        index_list (list): List of taken indices

    Raises:
        IndexError: If all indices have been taken

    Returns:
        int: Index that has not been taken yet
    """
    if len(dots) == len(index_list):
        raise IndexError("All indices have been taken")

    while True:
        index = randint(0, len(dots) - 1)
        if index not in index_list:
            return index


# -------------------- MAIN FUNCTION --------------------


def main() -> None:
    """Main function"""
    global dots, dead_dot, graph, dots_area, dead_dots_list

    # Dots initialization
    dots = Dot.initalize_multiple_dots()

    # Giving IDs to Dots
    for dot in dots:
        dot.id = dots.index(dot)

    already_used_indexes = []
    for _ in range(initial_infected_population):

        rdm = generate_not_taken_index(already_used_indexes)

        dots[rdm].become_infected()

        if infected_wear_mask and not dots[rdm].is_only_exposed():
            dots[rdm].wears_mask = True

        already_used_indexes.append(rdm)

    already_used_indexes = []
    for _ in range(masked_population):

        rdm = generate_not_taken_index(already_used_indexes)

        dots[rdm].wears_mask = True
        dots[rdm].was_originally_wearing_mask = True
        already_used_indexes.append(rdm)

    dead_dots_list = []

    if visual:
        # Graph initialization
        figure_dots = plt.figure(facecolor="white", figsize=(8.5, 6))
        dots_area = plt.axes(xlim=(0, HEIGHT_WIDTH), ylim=(0, HEIGHT_WIDTH))

        # Differentiating dots between each others
        global susceptible_dots
        susceptible_dots = dots_area.plot(
            [dot.x for dot in dots if not dot.is_infected and not dot.wears_mask],
            [dot.y for dot in dots if not dot.is_infected and not dot.wears_mask],
            f"g{shape}",
        )[0]

        global exposed_dots
        exposed_dots = dots_area.plot(
            [dot.x for dot in Dot.get_all_exposed() if not dot.wears_mask],
            [dot.y for dot in Dot.get_all_exposed() if not dot.wears_mask],
            f"m{shape}",
        )[0]

        global infected_dots
        infected_dots = dots_area.plot(
            [
                dot.x
                for dot in Dot.get_all_infected()
                if not dot.wears_mask and not infected_wear_mask
            ],
            [
                dot.y
                for dot in Dot.get_all_infected()
                if not dot.wears_mask and not infected_wear_mask
            ],
            f"r{shape}",
        )[0]

        global recovered_dots
        recovered_dots = dots_area.plot(
            [dot.x for dot in Dot.get_all_recovered() if not dot.wears_mask],
            [dot.y for dot in Dot.get_all_recovered() if not dot.wears_mask],
            f"b{shape}",
        )[0]

        global dead_dots
        dead_dots = dots_area.plot(
            [dot.x for dot in dead_dots_list if not dot.wears_mask],
            [dot.y for dot in dead_dots_list if not dot.wears_mask],
            f"k{shape}",
        )[0]

        # For masked population

        global susceptible_dots_masked
        susceptible_dots_masked = dots_area.plot(
            [dot.x for dot in Dot.get_all_susceptible() if dot.wears_mask],
            [dot.y for dot in Dot.get_all_susceptible() if dot.wears_mask],
            f"g{maskedShape}",
        )[0]

        global exposed_dots_masked
        exposed_dots_masked = dots_area.plot(
            [dot.x for dot in Dot.get_all_exposed() if dot.wears_mask],
            [dot.y for dot in Dot.get_all_exposed() if dot.wears_mask],
            f"m{maskedShape}",
        )[0]

        global infected_dots_masked
        infected_dots_masked = dots_area.plot(
            [
                dot.x
                for dot in Dot.get_all_infected()
                if dot.wears_mask or infected_wear_mask
            ],
            [
                dot.y
                for dot in Dot.get_all_infected()
                if dot.wears_mask or infected_wear_mask
            ],
            f"r{maskedShape}",
        )[0]

        global recovered_dots_masked
        recovered_dots_masked = dots_area.plot(
            [dot.x for dot in Dot.get_all_recovered() if dot.wears_mask],
            [dot.y for dot in Dot.get_all_recovered() if dot.wears_mask],
            f"b{maskedShape}",
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

        # Button to stop the simulation
        axstop = figure_dots.add_axes([0.88, 0.02, 0.1, 0.075])
        b_stop = Button(axstop, "Stop")

        # Positioning the button at bottom right corner
        b_stop.on_clicked(lambda _: stop())

        # Showing the plot
        plt.show()

    else:
        while True:
            Dot.move_all(dots)


# -------------------- MAIN CALL --------------------


if __name__ == "__main__":
    main()
