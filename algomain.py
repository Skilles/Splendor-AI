import os

import neat

import game
from game import main, Game

gen = 0


def eval_genomes(config, genomes):
    global gen
    gen += 1
    nets = []
    ge = []
    genome_pair = []
    games = []
    for i, g in genomes:
        net = neat.nn.RecurrentNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        genome_pair.append(g)
        games.append(Game(genome_pair))
        if len(genome_pair) == 2:
            genome_pair.clear()
    game.main(games)


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play blackjack.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(1, 30))

    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    # pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), main)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    winner = p.run(main, 1)
    # stats.save()
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    print(f'Win percentage: {winner.fitness * 100}%')
    # Show output of the most fit genome against training data.
    print('\nOutput:')

    node_names = {-1: 'A', -2: 'B', -3: 'C', 0: 'Output'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
