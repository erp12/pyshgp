from mrjob.job import MRJob

class Map_Reduce_Evaluation(MRJob):

	def __init__(population, eval_function):
		self.population = population
		self.eval_function

    def eval_mapper(self):
    	for ind in self.population:
    		yield eval_function(ind)

    def steps(self):
		return [MRStep(mapper=eval_mapper)]