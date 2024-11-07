import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import sys
from random import uniform

class SimulationConfig:
    """Configuration parameters for the SEIDR simulation."""
    
    def __init__(self, config_file: str):
        """Initialize simulation parameters from config file."""
        with open(config_file, 'r') as f:
            params = [line.strip() for line in f]
            if not params:
                sys.exit(1)
                
        self.transmission_rate = float(params[0]) / 100
        self.mortality_rate = float(params[1]) / 1000
        self.infected_duration = int(params[2])      # days in infectious state (after incubation)
        self.immunity_duration = int(params[3])
        self.population_size = int(params[4])
        self.minimal_distance = int(params[5])
        self.initial_infected = int(params[6])
        self.masked_population = int(params[7])
        self.exposed_duration = int(params[8])         # incubation time (non‐infectious)
        self.dot_shape = params[9]
        self.simulation_speed = float(params[10])
        
        self.collision_enabled = bool(int(params[11]))
        self.dots_same_speed = bool(int(params[12]))
        self.infected_wear_mask = bool(int(params[13]))
        self.infected_slowdown = bool(int(params[14]))
        self.people_travel_slower = bool(int(params[15]))
        self.auto_stop = bool(int(params[16]))
        self.visual = bool(int(params[17]))
        
        # time_step is in days; when simulation_speed is lower than 100, the simulation updates several ticks per day
        self.time_step = self.simulation_speed / 100
        self.transmission_rate_masked = self.transmission_rate / 3
        self.transmission_rate_masked_emit = self.transmission_rate / 18
        self.mortality_rate_per_tick = self.mortality_rate
        self.collision_distance = 1.3 if self.dot_shape == 'o' else 0.65
        self.masked_shape = 'P'
        
        self.grid_size = 100
        self.border_min = 1
        self.border_max = self.grid_size - 1
        self.infection_delay = 0.4
        self.dots_spawn_spacing = 2

class Population:
    """Manages the entire population of dots in the simulation."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.time = 0
        self.values_over_time = []
        
        self.positions = self._initialize_positions()
        self.velocities = self._initialize_velocities()
        self.speeds = self._initialize_speeds()
        self.states = np.zeros(config.population_size, dtype=np.int8)  # 0: susceptible, 1: exposed, 2: infected, 3: recovered, 4: dead
        self.masks = np.zeros(config.population_size, dtype=bool)
        self.infection_times = np.full(config.population_size, -1.0)
        self.recovery_times = np.full(config.population_size, -1.0)
        
        self._set_initial_infected()   # now sets them as "exposed"
        self._set_masked_population()
        # Save the original mask configuration so that recovered individuals revert to it
        self.initial_masks = self.masks.copy()
        
        self.direction_change_chances = np.random.uniform(0.85, 1, config.population_size)
        self.angles = np.random.uniform(0, 50, config.population_size)
        
    def _initialize_positions(self) -> np.ndarray:
        """Initialize random positions for all dots ensuring minimum spacing."""
        positions = np.zeros((self.config.population_size, 2))
        for i in range(self.config.population_size):
            while True:
                pos = np.random.uniform(
                    self.config.border_min,
                    self.config.border_max,
                    2
                )
                if i == 0 or np.all(
                    np.linalg.norm(positions[:i] - pos, axis=1) 
                    >= self.config.dots_spawn_spacing
                ):
                    positions[i] = pos
                    break
        return positions
    
    def _initialize_velocities(self) -> np.ndarray:
        """Initialize random velocities for all dots."""
        return (np.random.random((self.config.population_size, 2)) - 0.5) / 5
    
    def _initialize_speeds(self) -> np.ndarray:
        """Initialize movement speeds for all dots."""
        reduction = self.config.simulation_speed * 100 if self.config.people_travel_slower else 100
        
        if self.config.dots_same_speed:
            return np.full(
                self.config.population_size,
                self.config.simulation_speed / reduction
            )
        return np.random.normal(
            loc=self.config.simulation_speed / reduction,
            scale=200 / reduction,
            size=self.config.population_size
        )
    
    def _set_initial_infected(self):
        """Set initial infected population (starting as exposed)."""
        infected_indices = np.random.choice(
            self.config.population_size,
            self.config.initial_infected,
            replace=False
        )
        # Set as exposed (state 1) so that they go through incubation before becoming infectious.
        self.states[infected_indices] = 1
        self.infection_times[infected_indices] = self.time
        # Note: The slowdown and mask-forcing will be applied when they transition to state 2.
    
    def _set_masked_population(self):
        """Set initial masked population."""
        available_indices = np.where(~self.masks)[0]
        mask_indices = np.random.choice(
            available_indices,
            min(self.config.masked_population, len(available_indices)),
            replace=False
        )
        self.masks[mask_indices] = True

    def update(self):
        """Update the entire population for one time step."""
        self._move()
        
        # Update states only when a new day begins.
        if np.floor(self.time + self.config.time_step) == np.floor(self.time) + 1:
            self._update_states()
            
        self.time += self.config.time_step
        
        return self.should_stop()
    
    def _move(self):
        """Update positions of all dots."""
        alive_mask = self.states != 4
        
        # Randomly change direction for some dots.
        mask = (np.random.random(self.config.population_size) >= self.direction_change_chances) & alive_mask
        if np.any(mask):
            alpha = np.radians(np.random.normal(0, self.angles[mask]))
            theta = np.arctan2(self.velocities[mask, 1], self.velocities[mask, 0])
            norm = np.linalg.norm(self.velocities[mask], axis=1)
            
            self.velocities[mask, 0] = norm * np.cos(theta + alpha)
            self.velocities[mask, 1] = norm * np.sin(theta + alpha)
        
        movement = np.zeros_like(self.velocities)
        movement[alive_mask] = self.velocities[alive_mask] * ((self.config.simulation_speed * (1 + self.speeds[alive_mask, np.newaxis])) / 10)
        self.positions += movement
        
        # Normalize velocities: use proper indexing so the changes are applied in-place.
        alive_indices = np.where(alive_mask)[0]
        velocities_norm = np.linalg.norm(self.velocities[alive_indices], axis=1)
        min_speed = 0.005
        max_speed = 0.2
        
        mask_slow = velocities_norm < min_speed
        if np.any(mask_slow):
            scale = min_speed / velocities_norm[mask_slow]
            slow_indices = alive_indices[mask_slow]
            self.velocities[slow_indices] *= scale[:, np.newaxis]
        
        mask_fast = velocities_norm > max_speed
        if np.any(mask_fast):
            scale = max_speed / velocities_norm[mask_fast]
            fast_indices = alive_indices[mask_fast]
            self.velocities[fast_indices] *= scale[:, np.newaxis]
        
        if self.config.collision_enabled:
            self._handle_collisions(alive_mask)
        
        self._handle_boundaries(alive_mask)
    
    def _handle_collisions(self, alive_mask):
        """Handle collisions between dots."""
        positions_alive = self.positions[alive_mask]
        if len(positions_alive) <= 1:
            return
            
        distances = np.linalg.norm(
            positions_alive[:, np.newaxis] - positions_alive, 
            axis=2
        )
        np.fill_diagonal(distances, np.inf)
        
        collisions = distances < self.config.collision_distance
        if np.any(collisions):
            i, j = np.nonzero(collisions)
            unique_collisions = i < j
            i, j = i[unique_collisions], j[unique_collisions]
            
            alive_indices = np.where(alive_mask)[0]
            i = alive_indices[i]
            j = alive_indices[j]
            
            self.velocities[i] *= -1
            self.velocities[j] *= -1

    def _handle_boundaries(self, alive_mask):
        """Handle boundary conditions."""
        damping = 0.8
        
        x_max_mask = (self.positions[:, 0] >= self.config.border_max) & alive_mask
        x_min_mask = (self.positions[:, 0] <= self.config.border_min) & alive_mask
        
        self.positions[x_max_mask, 0] = self.config.border_max
        self.positions[x_min_mask, 0] = self.config.border_min
        self.velocities[x_max_mask | x_min_mask, 0] *= -damping
        
        y_max_mask = (self.positions[:, 1] >= self.config.border_max) & alive_mask
        y_min_mask = (self.positions[:, 1] <= self.config.border_min) & alive_mask
        
        self.positions[y_max_mask, 1] = self.config.border_max
        self.positions[y_min_mask, 1] = self.config.border_min
        self.velocities[y_max_mask | y_min_mask, 1] *= -damping
    
    def _update_states(self):
        """Update health states of all dots for the new day."""
        # 1. Transition exposed individuals to infected (and reset their infection timer)
        self._transition_exposed()
        # 2. Process new infections from the current infectious individuals.
        self._handle_infections()
        # 3. Process deaths (only in the infectious state).
        self._handle_deaths()
        # 4. Process recoveries for those who have been infectious long enough.
        self._handle_recoveries()
        # 5. Handle loss of immunity.
        self._handle_immunity_loss()
        # 6. Record daily statistics.
        self._record_statistics()
    
    def _transition_exposed(self):
        """Transition exposed individuals to the infectious state after incubation ends."""
        exposed_mask = (self.states == 1) & (self.time - self.infection_times >= self.config.exposed_duration)
        if np.any(exposed_mask):
            self.states[exposed_mask] = 2
            # Reset infection time so that the infected (symptomatic) period lasts the full duration.
            self.infection_times[exposed_mask] = self.time
            if self.config.infected_wear_mask:
                self.masks[exposed_mask] = True
            if self.config.infected_slowdown:
                self.speeds[exposed_mask] *= 0.25
    
    def _handle_deaths(self):
        """Handle deaths of infectious individuals."""
        infected_mask = self.states == 2
        death_candidates = np.random.random(self.config.population_size) <= self.config.mortality_rate_per_tick
        new_deaths = infected_mask & death_candidates
        self.states[new_deaths] = 4
    
    def _handle_infections(self):
        """Handle new infections based on contacts between susceptible and infectious dots."""
        susceptible_mask = self.states == 0
        if not np.any(susceptible_mask):
            return
            
        infected_mask = self.states == 2
        if not np.any(infected_mask):
            return
            
        distances = np.linalg.norm(
            self.positions[susceptible_mask][:, np.newaxis] - self.positions[infected_mask],
            axis=2
        )
        
        possible_infections = distances < self.config.minimal_distance
        
        for i, susceptible_idx in enumerate(np.where(susceptible_mask)[0]):
            if not np.any(possible_infections[i]):
                continue
                
            infected_indices = np.where(infected_mask)[0][possible_infections[i]]
            
            for infected_idx in infected_indices:
                base_rate = (self.config.transmission_rate_masked_emit 
                           if self.masks[infected_idx] 
                           else self.config.transmission_rate)
                
                if self.masks[susceptible_idx]:
                    base_rate *= (self.config.transmission_rate_masked / 
                                self.config.transmission_rate)
                
                if np.random.random() < base_rate:
                    self.states[susceptible_idx] = 1  # become exposed
                    self.infection_times[susceptible_idx] = self.time
                    break
    
    def _handle_recoveries(self):
        """Handle recovery of infectious individuals."""
        infected_mask = (self.states == 2) & (self.time - self.infection_times >= self.config.infected_duration)
        if np.any(infected_mask):
            self.states[infected_mask] = 3
            self.recovery_times[infected_mask] = self.time
            # Restore the original mask status (some individuals may be masked from the start)
            self.masks[infected_mask] = self.initial_masks[infected_mask]
            if self.config.infected_slowdown:
                self.speeds[infected_mask] *= 4
    
    def _handle_immunity_loss(self):
        """Handle loss of immunity for recovered individuals."""
        recovered_mask = self.states == 3
        immunity_time = self.time - self.recovery_times
        immunity_loss = recovered_mask & (immunity_time >= self.config.immunity_duration)
        
        self.states[immunity_loss] = 0
        self.infection_times[immunity_loss] = -1
        self.recovery_times[immunity_loss] = -1
    
    def _record_statistics(self):
        """Record current population statistics."""
        stats = [
            np.sum(self.states == 0),  # susceptible
            np.sum(self.states == 2),  # infected (state 2)
            np.sum(self.states == 3),  # recovered
            np.sum(self.states == 1),  # exposed
            np.sum(self.states == 4),  # dead
            self.time
        ]
        self.values_over_time.append(stats)
        
    def should_stop(self) -> bool:
        """Determine if simulation should stop."""
        if not self.config.auto_stop:
            return False
        
        return (np.sum(self.states == 1) + np.sum(self.states == 2) == 0 
                and self.time > self.config.exposed_duration)
    
    def get_plot_data(self):
        """Get current positions for plotting."""
        return {
            'susceptible': {
                'unmasked': self.positions[(self.states == 0) & ~self.masks],
                'masked': self.positions[(self.states == 0) & self.masks]
            },
            'exposed': {
                'unmasked': self.positions[(self.states == 1) & ~self.masks],
                'masked': self.positions[(self.states == 1) & self.masks]
            },
            'infected': {
                'unmasked': self.positions[(self.states == 2) & ~self.masks],
                'masked': self.positions[(self.states == 2) & self.masks]
            },
            'recovered': {
                'unmasked': self.positions[(self.states == 3) & ~self.masks],
                'masked': self.positions[(self.states == 3) & self.masks]
            },
            'dead': {
                'unmasked': self.positions[(self.states == 4) & ~self.masks],
                'masked': self.positions[(self.states == 4) & self.masks]
            }
        }

class Visualizer:
    """Handles visualization of the simulation."""
    
    def __init__(self, population: Population, config: SimulationConfig):
        self.population = population
        self.config = config
        
        self.fig = plt.figure(facecolor="white", figsize=(8.5, 6))
        self.ax = plt.axes(xlim=(0, config.grid_size), ylim=(0, config.grid_size))
        self.ax.axis('off')
        
        self.plots = {}
        for state in ['susceptible', 'exposed', 'infected', 'recovered', 'dead']:
            self.plots[state] = {
                'unmasked': self.ax.plot([], [], f"{self._get_color(state)}{config.dot_shape}")[0],
                'masked': self.ax.plot([], [], f"{self._get_color(state)}{config.masked_shape}")[0]
            }
        
        ax_stop = self.fig.add_axes([0.88, 0.02, 0.1, 0.075])
        self.stop_button = Button(ax_stop, 'Stop')
        self.stop_button.on_clicked(self._handle_stop)
        
    @staticmethod
    def _get_color(state: str) -> str:
        """Get color code for each state."""
        colors = {
            'susceptible': 'g',
            'exposed': 'm',
            'infected': 'r',
            'recovered': 'b',
            'dead': 'k'
        }
        return colors[state]
    
    def update(self, frame):
        """Update visualization for current frame."""
        plot_data = self.population.get_plot_data()
        
        for state, data in plot_data.items():
            for mask_state in ['unmasked', 'masked']:
                positions = data[mask_state]
                if len(positions) > 0:
                    self.plots[state][mask_state].set_data(positions[:, 0], positions[:, 1])
                else:
                    self.plots[state][mask_state].set_data([], [])
        
        stats = self.population.values_over_time[-1] if self.population.values_over_time else [0, 0, 0, 0, 0, 0]
        self.ax.set_title(
            f"Susceptible: {stats[0]}   |   "
            f"Exposed: {stats[3]}   |   "
            f"Infected: {stats[1]}   |   "
            f"Recovered: {stats[2]}   |   "
            f"Dead: {stats[4]}   |   "
            f"Days: {int(stats[5])}"
        )
    
    def _handle_stop(self, event):
        """Handle stop button click."""
        self._write_logs()
        plt.close()
        sys.exit(0)
    
    def _write_logs(self):
        """Write simulation logs to file."""
        with open("files\\logs.txt", "a") as f:
            for values in self.population.values_over_time:
                f.write(f"{values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}\n")
    
    def show(self):
        """Start the visualization."""
        def update_frame(frame):
            if self.population.update():
                self._write_logs()
                plt.close()
                sys.exit(0)
            self.update(frame)
            
        anim = FuncAnimation(
            self.fig,
            update_frame,
            frames=60,
            interval=0
        )
        plt.show()

def main():
    """Main simulation function."""
    config = SimulationConfig(sys.argv[1])
    population = Population(config)
    
    if config.visual:
        visualizer = Visualizer(population, config)
        visualizer.show()
    else:
        while True:
            if population.update():
                # In non‐visual mode, write logs and exit.
                with open("files\\logs.txt", "a") as f:
                    for values in population.values_over_time:
                        f.write(f"{values[0]}, {values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}\n")
                break

if __name__ == "__main__":
    main()
