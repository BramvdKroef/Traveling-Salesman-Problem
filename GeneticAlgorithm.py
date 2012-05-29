import random

class SolutionCandidate:
    def crossover(self, other):
        """Swaps or shares random parts of the solution 'other' to
        create two new solutions. """
        
        raise NotImplementedError("This class has not implemented crossover()")
    
    def mutate(self):
        """Tweaks a random bit of this solution."""

        raise NotImplementedError("This class has not implemented mutate()")

    def getFitness(self):
        """Returns a non-negative number that determines how well this
        solution scores relative to other instances of the same
        implementation. The higher the score the more likely this
        solution is selected for the next generation. """
        
        raise NotImplementedError("This class has not implemented getFitness()")

    def copy(self):
        """Returns a copy of this solution that can be modified
        independantly."""
        
        raise NotImplementedError("This class has not implemented copy()")

class SolutionCandidateFactory:
    """GeneticAlgorithm uses this factory to generate (possibly
    random) solutions for its first generation."""
    def generate():
        """Returns an instance of a class that implements SolutionCandidate."""
        pass
    
class GeneticAlgorithm:
    def __init__(self, solutionGenerator, crossoverChance, mutationChance, population):
        self.crossoverChance = crossoverChance
        self.mutationChance = mutationChance
        self.population = population
        self.generation = self.createInitialPopulation(solutionGenerator)

    def createInitialPopulation(self, solutionGenerator):
        solutions = [solutionGenerator.generate() \
                      for i in range(self.population)]
        return solutions

    def getSolutions(self):
        return self.generation

    def getBestSolution(self):
        fitnesses = [solution.getFitness() for solution in self.generation]
        return self.generation[fitnesses.index(max(fitnesses))]

    def select (self, fitnesses):
        """Select a value from the array fitnesses on a random number
        based on the fitness values."""
        selection = random.random() * sum(fitnesses)

        index = 0;
        while selection > 0:
            selection -= fitnesses[index]
            index += 1

        return self.generation[index - 1]
    
    def evolve(self):
    
        # Fitness calculation
        fitnesses = [solution.getFitness() for solution in self.generation]
        floor = min(fitnesses)
        fitnesses = [fitness - floor for fitness in fitnesses]
        
	newGeneration = []
	while len(newGeneration) < len(self.generation):
            # Select two parents.
            parents = [self.select(fitnesses).copy(),
                       self.select(fitnesses).copy()]

            # Randomly run them through crossover()
            if random.random() < self.crossoverChance:
                parents[0].crossover(parents[1])

            # Randomly run them through mutate()
            for parent in parents:
                if random.random() <= self.mutationChance:
                    parent.mutate()
                
            # Add them to the new batch of routes.
            newGeneration.extend(parents)

        self.generation = newGeneration

