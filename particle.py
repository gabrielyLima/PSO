import random


class Particle:
    def __init__(self, dimensions, inertia):
        self.dimensions = dimensions
        self.position = []  # particle position
        self.velocity = []  # particle velocity
        self.pos_best = []  # best position individual
        self.err_best = -1  # best error individual
        self.err = -1  # error individual
        self.inertia = inertia

        global num_dimensions
        # num_dimensions = len(x0)
        num_dimensions = len(self.dimensions)

        for i in range(0, num_dimensions):
            self.velocity.append(random.uniform(-1, 1))
            self.position.append(random.uniform(min(self.dimensions[i]),
                                                max(self.dimensions[i])))

    # evaluate current fitness
    def evaluate(self, func_fitness):
        self.err = func_fitness(self.position)

        # check to see if the current position is an individual best
        if self.err < self.err_best or self.err_best == -1:
            self.pos_best = self.position
            self.err_best = self.err

    # update new particle velocity - inertia
    def update_velocity_intertia(self, pos_best_g):
        w = self.inertia #+ (random.random()/2) # constant inertia weight (how much to weigh the previous velocity)
        c1 = 2.05  # cognative constant
        c2 = 2.05  # social constant

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best[i] - self.position[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social

    # update new particle velocity - clerc
    def update_velocity_clerc(self, pos_best_g):
        c_fac = 0.7298

        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel = c_fac * (
                    (self.velocity[i] + r1) * (self.pos_best[i] - self.position[i]) + (
                    r2 * (pos_best_g[i] - self.position[i])))
            self.velocity[i] = vel

    # update new particle velocity - Linear Decreasing Inertia Weight
    def update_velocity_linear_decreasing(self, pos_best_g, max_iterations, iteration):
        w_max = 0.3
        w_min = 0.05
        c1 = 2.05  # cognative constant
        c2 = 2.05  # social constant
        w = (w_max - (((w_max - w_min) / max_iterations) * iteration))


        for i in range(0, num_dimensions):
            r1 = random.random()
            r2 = random.random()

            vel_cognitive = c1 * r1 * (self.pos_best[i] - self.position[i])
            vel_social = c2 * r2 * (pos_best_g[i] - self.position[i])
            self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social
            #print(w)


    # update the particle position based off new velocity updates
    def update_position(self):
        for i in range(0, num_dimensions):
            self.position[i] = self.position[i] + self.velocity[i]

            # adjust maximum position if necessary
            if self.position[i] > max(self.dimensions[i]):
                self.position[i] = max(self.dimensions[i])

            # adjust minimum position if neseccary
            if self.position[i] < min(self.dimensions[i]):
                self.position[i] = min(self.dimensions[i])

    def get_position(self):
        return self.position
