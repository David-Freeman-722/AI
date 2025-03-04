import pygame
import random
import math
import numpy
from laser_tower import LaserTower

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize Pygame mixer for sound

# Constants
WIDTH, HEIGHT = 400, 600
TOWER_X, TOWER_Y = WIDTH // 2, HEIGHT - 50

# Recreate the screen with the new size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
METEOR_RADIUS = 2
TOWER_TURN_SPEED = 0.1
ARROW_LENGTH = 20  # Length of the arrow representing the LaserTower

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Defense")
clock = pygame.time.Clock()

class MeteorTestCase:
    def __init__(
        self,
        noise_x,
        noise_y,
        x_max_vel,
        y_max_vel,
        accel,
        number_of_meteors,
        tower_health,
        scenario,
        max_shots=10,
    ):
        self.scenario = scenario  # "tracking" or "defending"
        self.noise_x = noise_x
        self.noise_y = noise_y
        self.x_max_vel = x_max_vel
        self.y_max_vel = y_max_vel
        self.accel = accel
        self.number_of_meteors = number_of_meteors
        self.tower_health = tower_health
        self.max_shots = max_shots

class Meteor:
    meteor_counter = 0  # Class variable to assign unique IDs

    def __init__(self, x_cor, y_cor, x_vel, y_vel, accel, accel_factor, spawn_time):
        # This Meteor uses a simple ballistic equation with separate acceleration factors.
        # x(t)= x0 + vx0*(t - spawn_time) + 0.5 * accel*(accel_factor)*(t - spawn_time)^2
        # y(t)= y0 + vy0*(t - spawn_time) + 0.5 * accel*(t - spawn_time)^2
        self.id = Meteor.meteor_counter
        Meteor.meteor_counter += 1
        # Initial positions & velocities
        self.x_init = x_cor
        self.y_init = y_cor
        self.init_x_vel = x_vel
        self.init_y_vel = y_vel
        # Acceleration & time shift
        self.accel = accel  # y-accel
        self.accel_factor = accel_factor  # fraction for x-accel
        self.t_shift = spawn_time
        # We'll track the current position for rendering
        self.x_coordinate = x_cor
        self.y_coordinate = y_cor

    def update_position(self, current_time):
        # time here is in seconds since start
        t = current_time - self.t_shift
        if t < 0:
            # Meteor not yet spawned, so do nothing
            return
        # x(t)
        self.x_coordinate = (
            self.x_init
            + self.init_x_vel * t
            + 0.5 * (self.accel * self.accel_factor) * (t**2)
        )
        # y(t)
        self.y_coordinate = (
            self.y_init
            + self.init_y_vel * t
            + 0.5 * self.accel * (t**2)
        )

class Environment:
    def __init__(self, test_case: MeteorTestCase, sound_enabled=True):
        self.survived = False  # Will be True if the player survives 45 seconds
        self.sound_enabled = sound_enabled  # store the flag
        # Load a laser sound (replace 'laser_sound.wav' with your sound file path)
        try:
            self.laser_sound = pygame.mixer.Sound("laser_sound.wav")
        except pygame.error:
            self.laser_sound = None
            print("Could not load laser sound. Please ensure 'laser_sound.wav' is available.")
        self.game_over = False  # Track if the game is over
        # Use a fixed timestep for the model instead
        self.dt = 1.0 / 30.0  # each update is 1/30th of a second in model time
        self.model_time = 0.0
        self.health = test_case.tower_health
        self.noise_x = test_case.noise_x
        self.noise_y = test_case.noise_y
        self.meteors_hit_ground = 0
        self.laser_tower = LaserTower(
            angle=math.pi / 2,
            firing_radius=int(0.6 * WIDTH),
            shots_remaining=test_case.max_shots,  # pass from test case
            max_turning_capacity=0.1
        )
        self.tower_angle = math.pi / 2
        self.meteors_destroyed = 0
        self.noisy_meteors = None
        self.predictions = None
        self.accel = test_case.accel
        # We'll keep a list of active meteors
        self.meteors = []
        # We'll schedule spawns
        max_spawn_time = 15  # arbitrary, can be changed
        self.spawn_list = []
        for _ in range(test_case.number_of_meteors):
            spawn_time = random.uniform(0, max_spawn_time)
            x_position = random.uniform(0, WIDTH)
            x_vel = random.uniform(0, test_case.x_max_vel)
            y_vel = random.uniform(0, test_case.y_max_vel)
            meteor_accel = random.uniform(0, test_case.accel)
            # We'll create a placeholder to spawn later
            self.spawn_list.append((spawn_time, x_position, x_vel, y_vel, meteor_accel))
        # sort by spawn_time so we can spawn in the correct order
        self.spawn_list.sort(key=lambda tup: tup[0])
        self.sound_enabled = sound_enabled  # store the flag
        # Load a laser sound (replace 'laser_sound.wav' with your sound file path)
        try:
            self.laser_sound = pygame.mixer.Sound("laser_sound.wav")
        except pygame.error:
            self.laser_sound = None
            print("Could not load laser sound. Please ensure 'laser_sound.wav' is available.")
        self.game_over = False  # Track if the game is over
        self.start_time = pygame.time.get_ticks()  # in ms
        self.health = test_case.tower_health
        self.noise_x = test_case.noise_x
        self.noise_y = test_case.noise_y
        self.meteors_hit_ground = 0
        self.laser_tower = LaserTower(
            angle=math.pi / 2,
            firing_radius=int(0.6 * WIDTH),
            shots_remaining=test_case.max_shots,  # pass from test case
            max_turning_capacity=0.1
        )
        self.tower_angle = math.pi / 2
        self.meteors_destroyed = 0
        self.noisy_meteors = None
        self.predictions = None
        self.accel = test_case.accel
        # We'll keep a list of active meteors
        self.meteors = []
        # We'll schedule spawns
        max_spawn_time = 15  # arbitrary, can be changed
        self.spawn_list = []
        for _ in range(test_case.number_of_meteors):
            spawn_time = random.uniform(0, max_spawn_time)
            x_position = random.uniform(0, WIDTH)
            x_vel = random.uniform(0, test_case.x_max_vel)
            y_vel = random.uniform(0, test_case.y_max_vel)
            meteor_accel = random.uniform(0, test_case.accel)
            # We'll create a placeholder to spawn later
            self.spawn_list.append((spawn_time, x_position, x_vel, y_vel, meteor_accel))
        # sort by spawn_time so we can spawn in the correct order
        self.spawn_list.sort(key=lambda tup: tup[0])

    def add_sensor_noise(self):
        noisy_meteors = []
        for meteor in self.meteors:
            # if meteor hasn't spawned yet (time < 0), skip
            noisy_x = meteor.x_coordinate + random.gauss(0, self.noise_x)
            noisy_y = meteor.y_coordinate + random.gauss(0, self.noise_y)
            noisy_meteors.append((meteor.id, noisy_x, noisy_y))
        return noisy_meteors

    def compute_new_tower_angle(self, rotation_angle):
        # Limit the change in angle to at most TOWER_TURN_SPEED
        limited_rotation = max(-TOWER_TURN_SPEED, min(TOWER_TURN_SPEED, rotation_angle))
        new_angle = self.tower_angle + limited_rotation
        if new_angle > math.pi:
            return math.pi
        elif new_angle < 0:
            return 0
        return new_angle

    def spawn_meteors(self, current_seconds):
        # spawn any meteors whose spawn_time <= current_seconds
        newly_spawned = []
        while self.spawn_list and self.spawn_list[0][0] <= current_seconds:
            spawn_time, x_position, x_vel, y_vel, meteor_accel = self.spawn_list.pop(0)
            # create the new meteor
            m = Meteor(
                x_cor=x_position,
                y_cor=0,  # top of screen
                x_vel=x_vel,
                y_vel=y_vel,
                accel=meteor_accel,
                accel_factor=1/3,
                spawn_time=spawn_time
            )
            newly_spawned.append(m)
        # add them to active meteors
        self.meteors.extend(newly_spawned)

    def update(self):
        # If already over, skip updates
        if self.game_over:
            return

        # Instead of wall-clock time, increment model_time by dt each update
        self.model_time += self.dt
        elapsed_time_s = self.model_time
        # spawn new meteors if their spawn_time has passed
        self.spawn_meteors(self.model_time)

        # Remove meteors that are hit or have left the screen / ground
        self.meteors = [m for m in self.meteors if not (
            self.laser_hits_meteor(m) or
            self.meteor_hits_ground(m) or
            self.meteor_exits_screen(m)
        )]

        # Update positions of meteors
        for m in self.meteors:
            m.update_position(elapsed_time_s)

        # Obtain noisy measurements and predictions
        self.noisy_meteors = self.add_sensor_noise()
        self.predictions = self.laser_tower.predict_from_observations(self.noisy_meteors)

        # Laser tower logic
        decision_to_fire, rotation_angle = self.laser_tower.laser_action()
        self.tower_angle = self.compute_new_tower_angle(rotation_angle)

        if decision_to_fire:
            if self.laser_tower.shots_remaining > 0:
                self.laser_tower.decision_to_fire = True
                self.laser_tower.shots_remaining -= 1
                # Play the laser sound if loaded
                if self.laser_sound and self.sound_enabled:
                    self.laser_sound.play()
            else:
                self.laser_tower.decision_to_fire = False  # No shots left
        else:
            self.laser_tower.decision_to_fire = False

    def meteor_hits_ground(self, meteor):
        # If meteor has spawned but is below the tower
        if meteor.y_coordinate >= TOWER_Y:
            self.meteors_hit_ground += 1
            self.health -= 1
            if self.health <= 0:
                self.game_over = True
            return True  # Decrease health when a meteor hits the ground
        return False

    def meteor_exits_screen(self, meteor):
        # remove if it goes out left/right
        if meteor.x_coordinate < 0 or meteor.x_coordinate > WIDTH:
            return True
        return False

    def laser_hits_meteor(self, meteor):
        if not self.laser_tower.decision_to_fire:
            return False
        # We'll do line-segment logic
        laser_x1, laser_y1 = TOWER_X, TOWER_Y
        # Use the firing_radius from the tower
        laser_x2 = TOWER_X + int(self.laser_tower.firing_radius * math.cos(self.tower_angle))
        laser_y2 = TOWER_Y - int(self.laser_tower.firing_radius * math.sin(self.tower_angle))
        
        # if meteor not spawned yet, skip
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        elapsed_time_s = elapsed_ms / 1000.0
        if self.model_time < meteor.t_shift:
            return False

        dx, dy = laser_x2 - laser_x1, laser_y2 - laser_y1
        denom = (dx**2 + dy**2)
        if denom == 0:
            return False
        t = ((meteor.x_coordinate - laser_x1) * dx + (meteor.y_coordinate - laser_y1) * dy) / denom
        if t < 0: t = 0
        if t > 1: t = 1
        closest_x = laser_x1 + t * dx
        closest_y = laser_y1 + t * dy
        dist = math.hypot(meteor.x_coordinate - closest_x, meteor.y_coordinate - closest_y)
        if dist < METEOR_RADIUS:
            self.meteors_destroyed += 1
            return True
        return False

    def draw_game_over(self):
        #screen.fill(BLACK)
        big_font = pygame.font.Font(None, 72)
        text = big_font.render("YOU LOSE!", True, RED)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

    def draw_survived(self):
        #screen.fill(BLACK)
        big_font = pygame.font.Font(None, 72)
        text = big_font.render("YOU SURVIVED!", True, GREEN)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

    def draw(self):
        elapsed_time = int(self.model_time)  # Convert ms to seconds
        screen.fill(BLACK)

        font = pygame.font.Font(None, 28)  # Smaller font size
        
        # First line: meteors hit ground & health
        line1_text = font.render(
            f"Meteors Hit Ground: {self.meteors_hit_ground}  "
            f"Health: {self.health}",
            True,
            WHITE
        )
        screen.blit(line1_text, (10, 10))
        
        # Second line: time & meteors remaining
        line2_text = font.render(
            f"Time: {elapsed_time}s  "
            f"Shots Remaining: {self.laser_tower.shots_remaining}",
            True,
            WHITE
        )
        screen.blit(line2_text, (10, 10 + line1_text.get_height()))

        # Draw real meteors
        for meteor in self.meteors:
            pygame.draw.circle(screen, WHITE, (int(meteor.x_coordinate), int(meteor.y_coordinate)), METEOR_RADIUS)

        # Draw predicted positions
        if self.predictions:
            for meteor_id, predicted_x, predicted_y in self.predictions:
                actual_meteor = next((m for m in self.meteors if m.id == meteor_id), None)
                if actual_meteor:
                    distance = math.hypot(predicted_x - actual_meteor.x_coordinate, predicted_y - actual_meteor.y_coordinate)
                    color = GREEN if distance < 2 * METEOR_RADIUS else RED
                else:
                    color = RED
                pygame.draw.circle(screen, color, (int(predicted_x), int(predicted_y)), METEOR_RADIUS)

        # Draw tower
        arrow_end_x = TOWER_X + int(ARROW_LENGTH * math.cos(self.tower_angle))
        arrow_end_y = TOWER_Y - int(ARROW_LENGTH * math.sin(self.tower_angle))
        pygame.draw.line(screen, RED, (TOWER_X, TOWER_Y), (arrow_end_x, arrow_end_y), 3)

        # Draw laser beam if firing
        if self.laser_tower.decision_to_fire:
            laser_end_x = TOWER_X + int(self.laser_tower.firing_radius * math.cos(self.tower_angle))
            laser_end_y = TOWER_Y - int(self.laser_tower.firing_radius * math.sin(self.tower_angle))
            pygame.draw.line(screen, RED, (TOWER_X, TOWER_Y), (laser_end_x, laser_end_y), 2)

# Runner function



def run_simulation(test_case: MeteorTestCase, SOUND=True,SPEED=30):
    env = Environment(test_case, sound_enabled=SOUND)
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    # toggle pause state
                    paused = not paused
        
        if not paused:
            env.update()

        # Check if the player has survived 45 seconds.
        # If so, end the game in a victory state.
        if not env.game_over:
            if env.model_time >= 45:
                env.survived = True  # Flag that the player survived.
                env.game_over = True

        if env.game_over:
            # Display final screen
            if env.survived:
                env.draw_survived()
            else:
                env.draw_game_over()
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        else:
            if not paused:
                env.draw()
            else:
                env.draw()
                font = pygame.font.Font(None, 72)
                pause_text = font.render("PAUSED", True, (255, 215, 0))
                rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(pause_text, rect)
            pygame.display.flip()

        clock.tick(SPEED)
    pygame.quit()

# Example test case
if __name__ == "__main__":
    test_case = MeteorTestCase(
        noise_x=5,
        noise_y=5,
        x_max_vel=3,
        y_max_vel=12,
        accel=2.5,
        number_of_meteors=30,
        tower_health=10,
        scenario="defending",
        max_shots=30
    )
    run_simulation(test_case)
