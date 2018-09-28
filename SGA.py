# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:22:04 2018

@author: zmddzf
"""

import random

class GA(object):
    """
    This is a class of GA algorithm
    """
    def __init__(self, parameters, low, up, objectFuction):
        """
        Initialize the object and set the parameters
        ___dict___
        The data structure of parameters is a list:
        [populationSize, maxGeneration, Pc, Pm, L]
        
        low is the low boundary of variables
        up is the up boundary of variables
        
        objectFunction is the function of the optimization problem
        We suggest objectFuction should be the fitness function 
        because not all the object function can be used as the fitness function
        """
        self.popSize = parameters[0]
        self.maxGeneration = parameters[1]
        self.Pc = parameters[2]
        self.Pm = parameters[3]
        self.L = parameters[4]
        self.low = low
        self.up = up
        self.fitnessFuction = objectFuction
    
    #define an encoder
    def __encoder(self, beforeEncoding):
        """
        We use binary method to encode the Gene
        This is a private attribute
        args:
            beforeEncoding: an integer number which need to be encoded
        return:
            afterEncoding: a string like '00000011'
        """
        L = str(self.L)
        afterEncoding = ('{:0%sb}'%L).format(beforeEncoding)
        return afterEncoding
    
    #define a decoder
    def __decoder(self, beforeDecoding):
        """
        This is a decoder to decode the binary encoding number
        args:
            beforeDecoding: a string which is like '0000010'
        return:
            afterDecoding: an integer
        """
        afterDecoding = eval('0b' + beforeDecoding)
        return afterDecoding
    
    #generate population
    def generatePop(self):
        """
        This is a attribute to generate population
        return:
            initPop: a list contented initial population
        """
        initPop = []
        for i in range(self.popSize):
            pop = []
            for l, u in zip(self.low, self.up):
                pop.append(random.randint(l, u))
            initPop.append(pop)
            
        return initPop
    
    #selection individuals
    def select(self, population):
        """
        This is a method of Roulette Wheel Selection
        
        args:
            population: a list variable like [[], [], ..., []]
        return:
            afterSelect: a list variable like [[], [], ..., []]
        """
        #compute fitness
        fitness = []
        for individual in population:
            fitness.append(self.fitnessFuction(individual))
        
        #compute likelihood
        likelihood = []
        for fit in fitness:
            likelihood.append(fit / sum(fitness))
            
        #start choosing
        afterSelect = []
        for i in range(len(fitness)):
            rand = random.random()        
            lk = 0
            for index, like in enumerate(likelihood):
                lk += like
                if rand <= lk:
                    afterSelect.append(population[index])
                    break
        return afterSelect
    
    #Crossover operation
    def crossover(self, population):
        """
        This is a method to crossover the chromosome
        args:
            population: a list variable like [[], [], ..., []]
        return:
            newPop: a list variable like [[], [], ..., []]
        """
        randomNum = random.random()
        
        newPop = []
        if randomNum < self.Pc:
            for decFather in population:
                decMother = random.choice(population)
                binMother = [self.__encoder(item) for item in decMother]
                binMother = ''.join(binMother)
                
                binFather = [self.__encoder(item) for item in decFather]
                binFather = ''.join(binFather)
                
                randomPosition = random.choice(range(len(binFather)))
                
                newParent = binFather[:randomPosition] + binMother[randomPosition:]
                
                newParent = [self.__decoder(newParent[i:i + self.L]) for i in range(0, len(decMother)*self.L, self.L)]
                newPop.append(newParent)
            return newPop
        else:
            return population
    
    #Mutation operation
    def mutation(self, population):
        """
        This is a method to do mutation operating
        args:
            population
        return:
            afterMutate
        """
        newPop = []
        for pop in population:
            newIndividual = []
            for item in pop:
                randomNum  = random.random()
                if randomNum < self.Pm:
                    newGene = list(self.__encoder(item))
                    newGene[random.choice(range(len(newGene)))] = str(abs(int(newGene[random.choice(range(len(newGene)))])-1))
                    newGene = ''.join(newGene)
                    newIndividual.append(self.__decoder(newGene))
                else:
                    newIndividual.append(item)
            newPop.append(newIndividual)
        return newPop
                    
    
    #run
    def runGA(self):
        pop = self.generatePop()
        for generation in range(self.maxGeneration):
            pop = self.select(pop)
            pop = self.crossover(pop)
            pop = self.mutation(pop)
            fitness = []
            for i in pop:
                fitness.append(self.fitnessFuction(i))
            individual = fitness.index(max(fitness))
            
            print('==========================================================')
            print('This is the %s generation'%generation)
            print('The highest fitness value is %s, the individual is %s'%(max(fitness), str(pop[individual])))
            print('==========================================================')
            

#define a fitness fuction
def objFun(para):
    return abs(para[0]*4 - para[1]**3 + para[1]**2)

value = []
xy = []
for i in range(1023):
    for j in range(1023):
        xy.append([i, j])
        value.append(objFun([i, j]))
        
        
low = [0, 0]
up = [1023, 1023]
parameters = [200, 10000, 0.8, 0.3, 10]
ga = GA(parameters, low, up, objFun)
ga.runGA()
        
                
                
                
            
        
        
    
            
    
    
    
    
    