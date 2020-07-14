import neat
import gym 
import os


env = gym.make('CartPole-v0')
env.reset()

def evaluate(genomes, config):
    for _, genome in genomes:
        observation = [0, 0, 0, 0]
        test_net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        done = False
        while not done: 
            env.render()
            output = test_net.activate(observation)
            action = max(output)
            if output[0] == action:
                action = 1
            else:
                action = 0                              
            
            observation, reward, done, info = env.step(action)
            if (observation[3] < -0.48 or observation[3] > 0.48): 
                done = True
                reward = -5
                env.reset()

            genome.fitness += reward
        env.reset()
    env.close()


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    final_genome = p.run(evaluate, n=100)

    print(f"The best genome is {final_genome}")

    winner_net = neat.nn.FeedForwardNetwork.create(final_genome, config)
    test_final(winner_net)

def test_final(final_network):
    observation = [0, 0, 0, 0]
    points = 0
    reward=0
    for i in range(100):
        observation = [0, 0, 0, 0]
        done = False
        while not done: 
            env.render()
            output = final_network.activate(observation)
            action = max(output)
            if output[0] == action:
                action = 1
            else:
                action = 0
            observation, reward, done, info = env.step(action)
            if (observation[3] < -0.48 or observation[3] > 0.48): 
                done = True
                env.reset()
            points += reward
        env.reset()
    env.close()
    
    score = points/100
    print(f"Score over 100 tries is {score}")



if __name__ == '__main__':

    config_path = "path to the config-feedforward.txt file"
    run(config_path)
    

    

        
