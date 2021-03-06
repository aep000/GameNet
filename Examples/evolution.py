import numpy as np
import random
from sklearn.datasets import load_digits
from operator import itemgetter
import math
#model Object
class evModel:
	def __init__(self,inputSize, outputSize, hiddenLayers, seed=None, activation=0, ):
		'''initialize weights of model with
		inputSize= amount of inputs
		outputSize= amount of outputs
		maxSize = max number of layers
		seed= structure of prexisisting model [ie change structure array into model object]
		tanh= Choose between logistic and tanh funcitons as activation functions
		'''
		self.structure=[]
		self.outputSize=outputSize
		self.inputSize=inputSize
		self.activation=activation
		if(seed==None):
			c=0
			while c<len(hiddenLayers)-1:
				self.structure.append([[1]*hiddenLayers[0]]*inputSize)
				#print self.structure
				c+=1;
			self.structure.append([[1]*outputSize]*hiddenLayers[-1])
		else:
			self.structure=seed
	def mutate(self,rate,frequency):
		'''randomly change wieghts between a certain amount
		(weight+randomInRange(rate,-rate),
		weights are adjusted at a certain frequency ((1/frequency)*weightCount) weights are adjusted
		'''
		outStructure=[]
		for row in self.structure:
			add=[]
			for vertex in row:
				semiAdd=[]
				for val in vertex:
					change = 0
					if (random.randint(0,frequency)==0):
						change = random.uniform(-rate,rate)
					semiAdd.append(val+change)
				add.append(semiAdd)
			outStructure.append(add)
			self.structure=outStructure
	def run(self,inputs, v=False):
		lastNodeOut=inputs
		if(v):
			print inputs
		for row in self.structure:
			tempNodeOut=[]
			c=0
			while(c<len(row)):
				out=0
				for vertex in row:
					#print lastNodeOut
					out+=vertex[c]*lastNodeOut[c]
				if(self.activation==0):
					tempNodeOut.append(np.tanh(out))
				elif(self.activation==1):
					if(out>0):
						tempNodeOut.append(out)
					else:
						tempNodeOut.append(0)
				else:
					tempNodeOut.append(1.0 / (1 + math.exp(-out)))
				c+=1
			lastNodeOut=tempNodeOut
		if(v):
			print lastNodeOut
		return lastNodeOut


'''def generateAverages(models):
	c=0
	output=[]
	isnode=False
	while c<len(models[0]):
		if(isnode):
			row=[0]*len(models[0][c])
		else:
			row=[[0]*len(models[0][c][0])]*len(models[0][c])
		for model in models:
			if(isnode):
				k=0
				for entry in model[c]:
					row[k]+=entry
					k+=1
			else:
				semirow=[]'''
def generateAverages(models):
	c=0
	print models
	output=[]
	isnode=False
	if len(models)==0:
		return None
	while c<len(models[0].structure):
		row=[]
		for model in models:
			row.append(model.structure[c])
		output.append(np.mean(row,axis=0).tolist())
		c+=1
	return output
def genomicBreed(models,scores,genSize, scoreIncreasing=True):
	scoreProb= []
	total = sum(scores)*1.0
	for score in scores:
		if(not scoreIncreasing):
			scoreProb.append(1-(score/total))
		else:
			scoreProb.append(score/total)
	print scoreProb
	nextGen=[]
	for c in xrange(genSize):
		individual=[]
		r1=0
		for k1 in models[0].structure:
			row=[]
			r2=0
			for k2 in k1:
				row2=[]
				r3=0
				for k3 in k2:
					row2.append(models[np.random.choice(len(models), 1, p=scoreProb)[0]].structure[r1][r2][r3])
					r3+=1
				row.append(row2)
				r2+=1
			individual.append(row)
			r1+=1
		nextGen.append(individual)
	return nextGen
