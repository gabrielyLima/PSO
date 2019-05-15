from __future__ import division
import time
from particle import Particle


class PSO:
    def __init__(self, func_fitness, dimensions, num_particles, max_iterations, inertia, topology=None):
        self.convergence_time = -1
        self.best_position = []
        self.best_error = -1
        self.error_history = []
        self.dimensions = dimensions
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.particle_positions = []
        self.best_position_history = []
        self.inertia = inertia
        self.topology = topology

        err_best_g = -1  # best error for group
        pos_best_g = []  # best position for group
        err_best_g_list = []

        start_time = time.time()

        self.fitness_assessment = 0

        for i in range(self.max_iterations):
            self.particle_positions.append([])

        # establish the swarm
        swarm = []
        for i in range(0, num_particles):
            swarm.append(Particle(self.dimensions, self.inertia))
        # begin optimization loop
        i = 0
        while i < self.max_iterations:
            # cycle through particles in swarm and evaluate fitness
            #if self.fitness_assessment < 500000:
            for j in range(0, self.num_particles):
                swarm[j].evaluate(func_fitness)
                self.fitness_assessment +=1

                # determine if current particle is the best (globally)
                if swarm[j].err < err_best_g or err_best_g == -1:
                    pos_best_g = list(swarm[j].position)
                    err_best_g = float(swarm[j].err)

            # Saving the best error values
            err_best_g_list.append(err_best_g)
            self.error_history.append(err_best_g)

            # cycle through swarm and update velocities and position
            lbest = []
            for j in range(0, self.num_particles):
                new_pos = swarm[j].position
                self.particle_positions[i].append(new_pos)
                if self.topology is None: # Global topology
                    #swarm[j].update_velocity_intertia(pos_best_g)
                    #swarm[j].update_velocity_clerc(pos_best_g)
                    swarm[j].update_velocity_linear_decreasing(pos_best_g, self.max_iterations, i)

                elif self.topology is "FOCAL":
                    if j is 0:
                        #swarm[0].update_velocity_intertia(pos_best_g)
                        swarm[0].update_velocity_clerc(pos_best_g)
                        #swarm[0].update_velocity_linear_decreasing(pos_best_g, self.max_iterations, i)
                    else:
                        #swarm[j].update_velocity_intertia(swarm[0].pos_best)
                        swarm[j].update_velocity_clerc(swarm[0].pos_best)
                        #swarm[j].update_velocity_linear_decreasing(swarm[0].pos_best, self.max_iterations, i)

                elif self.topology is "LOCAL":
                    neighbors = [swarm[(j-1) % num_particles].err_best, swarm[(j + 1) % num_particles].err_best, swarm[j].err_best]
                    aux = neighbors.index(min([x for x in neighbors if x!=None]))
                    if aux == 0:
                        #swarm[j].update_velocity_intertia(swarm[(j-1) % num_particles].pos_best)
                        #swarm[j].update_velocity_clerc(swarm[(j - 1) % num_particles].pos_best)
                        swarm[j].update_velocity_linear_decreasing(swarm[(j - 1) % num_particles].pos_best, self.max_iterations, i)
                    elif aux == 1:
                        #swarm[j].update_velocity_intertia(swarm[(j+1) % num_particles].pos_best)
                        #swarm[j].update_velocity_clerc(swarm[(j + 1) % num_particles].pos_best)
                        swarm[j].update_velocity_linear_decreasing(swarm[(j + 1) % num_particles].pos_best, self.max_iterations, i)
                    else:
                        #swarm[j].update_velocity_intertia(swarm[j].pos_best)
                        #swarm[j].update_velocity_clerc(swarm[j].pos_best)
                        swarm[j].update_velocity_linear_decreasing(swarm[j].pos_best, self.max_iterations, i)
                swarm[j].update_position()

            i += 1
            b_pos = pos_best_g
            self.best_position_history.append(b_pos)

            #else:
             #   break

        self.convergence_time = time.time() - start_time
        self.best_error = err_best_g

        # update final results squared_error
        self.best_position = pos_best_g