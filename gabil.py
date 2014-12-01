from pyevolve import G1DList, G1DBinaryString
from pyevolve import Mutators, Initializators, Crossovers
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import DBAdapters

import sys
import pyevolve.Consts
import pyevolve.Util
import random
import numpy as np


population = []

def match(genome,parent):
    tam_genome = len(genome)
    num_rules = tam_genome / 30
    rules = []
    well = 0.0
    for x in range(num_rules):
        rule = []
        cont = x * 30
        while cont < tam_genome:
            rule.append(genome[cont])
            cont += 1
            if cont % 30 ==0 :
                break
        rules.append(rule)
    ver = 0
    for rule in rules:
        for x in range(len(rule)):
            if (parent[x] == 1) and (rule[x] != 1):
                ver += 1
                break
            else:
                if (rule[len(rule)-2] == 1) and (rule[len(rule)-1] == 0):
                    ver+=1

    if ver != num_rules:
        well += 1.0
    return well


def eval_func(genome):
    well = 0.0
    num_ex = len(population)
    tam_genome = len(genome)
    num_rules = tam_genome / 30 
    for parent in population:
        
        rules = []
        for x in range(num_rules):
            rule = []
            cont = x * 30
            while cont < tam_genome:
                rule.append(genome[cont])
                cont += 1
                if cont % 30 ==0 :
                    break
            rules.append(rule)
        ver = 0
        for rule in rules:
            for x in range(len(rule)):
                if (parent[x] == 1) and (rule[x] != 1):
                    ver += 1
                    break

        if ver != num_rules:
            well += 1.0
    correct = well / num_ex
    score = correct * correct
    return score

def eval_func_1(genome):
    well = 0.0
    num_ex = len(population)
    tam_genome = len(genome)
    num_rules = tam_genome / 30 
    for parent in population:
        
        rules = []
        for x in range(num_rules):
            rule = []
            cont = x * 30
            while cont < tam_genome:
                rule.append(genome[cont])
                cont += 1
                if cont % 30 ==0 :
                    break
            rules.append(rule)
        ver = 0
        for rule in rules:
            for x in range(len(rule)):
                if (parent[x] == 1) and (rule[x] != 1):
                    ver += 1
                    break

        if ver != num_rules:
            well += 1.0
    correct = well / num_ex
    score = correct * correct
    return score/float(tam_genome)

def crossoverGabil(genome, **args):
    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]
    tamReglas = 30


    cuts = [random.randint(0, (len(gMom)-1)/ tamReglas) , random.randint(0, (len(gMom)-1)/tamReglas)]

    if cuts[0] > cuts[1]:
        pyevolve.Util.listSwapElement(cuts, 0, 1)

    restos = [random.randint(0, tamReglas-1), random.randint(0, tamReglas-1)]

    if restos[0] > restos[1]:
        pyevolve.Util.listSwapElement(restos, 0, 1)

    cuts2 = [random.randint(0, (len(gDad)-1) / tamReglas), random.randint(0, (len(gDad)-1)/tamReglas)]

    if cuts2[0] > cuts2[1]:
        pyevolve.Util.listSwapElement(cuts2, 0, 1)


    if args["count"] >= 1:
        sister = gMom.clone()
        sister.resetStats()
        sister[cuts[0]*tamReglas+restos[0]:cuts[1]*tamReglas+restos[1]] = \
        gDad[cuts2[0]*tamReglas+restos[0]:cuts2[1]*tamReglas+restos[1]]
        sister.stringLength = len(sister.genomeString)

    if args["count"] == 2:
        brother = gDad.clone()
        brother.resetStats()
        brother[cuts2[0]*tamReglas+restos[0]:cuts2[1]*tamReglas+restos[1]] = \
        gMom[cuts[0]*tamReglas+restos[0]:cuts[1]*tamReglas+restos[1]]
        brother.stringLength = len(brother.genomeString)

    return (sister, brother)


def main():


	#Verificamos que el pase de argumentos sea correcto
    if (len(sys.argv)<= 5):
        print "Utilice:"
        print "python nombrePrograma nombreArchivo tasaMutacion tasaCrossover tipoSeleccion penalizacion"
        print "Donde: "
        print " tipoSeleccion: 1- Rueda de Ruleta"
        print "                2- Otro"
        print " penalizacion:  1- Sin penalizacion"
        print "                2- Con penalizacion"
        sys.exit()

    # Verificamos la existencia del archivo
    try:
        with open(sys.argv[1]): pass
    except IOError:
        print "Error - El archivo especificado no existe."
        sys.exit()

    archivo = open(sys.argv[1], 'r')
    for line in archivo:
        a = line.split()
        s_length = float(a[0])
        s_width = float(a[1])
        p_length = float(a[2])
        p_width = float(a[3])
        tipo = a[4]
        if s_length >= 4.3 and s_length < 4.9:
            tmp = [1,0,0,0,0,0,0]
        elif s_length >= 4.9 and s_length < 5.5:
            tmp = [0,1,0,0,0,0,0]
        elif s_length >= 5.5 and s_length < 6.1:
            tmp = [0,0,1,0,0,0,0]
        elif s_length >= 6.1 and s_length < 6.7:
            tmp = [0,0,0,1,0,0,0]
        elif s_length >= 6.7 and s_length < 7.3:
            tmp = [0,0,0,0,1,0,0]
        elif s_length >= 7.3 and s_length < 7.9:
            tmp = [0,0,0,0,0,1,0]
        else:
            tmp = [0,0,0,0,0,0,1]

        if s_width >= 2.0 and s_width < 2.4:
            tmp1 = [1,0,0,0,0,0,0]
        elif s_width >= 2.4 and s_width < 2.8:
            tmp1 = [0,1,0,0,0,0,0]
        elif s_width >= 2.8 and s_width < 3.2:
            tmp1 = [0,0,1,0,0,0,0]
        elif s_width >= 3.2 and s_width < 3.6:
            tmp1 = [0,0,0,1,0,0,0]
        elif s_width >= 3.6 and s_width < 4.0:
            tmp1 = [0,0,0,0,1,0,0]
        elif s_width >= 4.0 and s_width < 4.4:
            tmp1 = [0,0,0,0,0,1,0]
        else:
            tmp1 = [0,0,0,0,0,0,1]

        if p_length >= 1.0 and p_length < 1.9:
            tmp2 = [1,0,0,0,0,0,0]
        elif p_length >= 1.9 and p_length < 2.8:
            tmp2 = [0,1,0,0,0,0,0]
        elif p_length >= 2.8 and p_length < 3.7:
            tmp2 = [0,0,1,0,0,0,0]
        elif p_length >= 3.7 and p_length < 4.6:
            tmp2 = [0,0,0,1,0,0,0]
        elif p_length >= 4.6 and p_length < 5.5:
            tmo2 = [0,0,0,0,1,0,0]
        elif p_length >= 5.5 and p_length < 6.4:
            tmp2 = [0,0,0,0,0,1,0]
        elif p_length >= 6.4 and p_length < 7.2:
            tmp2 = [0,0,0,0,0,0,1]

        if p_width >= 0.1 and p_width < 0.5:
            tmp3 = [1,0,0,0,0,0,0]
        elif p_width >= 0.5 and p_width < 0.9:
            tmp3 = [0,1,0,0,0,0,0]
        elif p_width >= 0.9 and p_width < 1.3:
            tmp3 = [0,0,1,0,0,0,0]
        elif p_width >= 1.3 and p_width < 1.7:
            tmp3 = [0,0,0,1,0,0,0]
        elif p_width >= 1.7 and p_width < 2.1:
            tmp3 = [0,0,0,0,1,0,0]
        elif p_width >= 2.1 and p_width < 2.5:
            tmp3 = [0,0,0,0,0,1,0]
        else:
            tmp3 = [0,0,0,0,0,0,1]

        if tipo == "Iris-setosa":
            tmp4 = [0,0]
        elif tipo == "Iris-versicolor":
            tmp4 = [0,1]
        elif tipo == "Iris-virginica":
            tmp4 = [1,0]
        else:
            tmp4 = [1,1]

        hypothesis = tmp + tmp1 + tmp2 + tmp3 + tmp4
        population.append(hypothesis)
    
    mutationRate = float(sys.argv[2])
    crossoverRate = float(sys.argv[3])
    typeSelector = int(sys.argv[4])
    penalization = int(sys.argv[5])


    genome = G1DBinaryString.G1DBinaryString(30)
    genome.setParams(rangemin=0, rangemax=1)
    if penalization == 1:
        genome.evaluator.set(eval_func)
    else:
        genome.evaluator.set(eval_func_1)
    genome.mutator.set(Mutators.G1DBinaryStringMutatorSwap)
    genome.crossover.set(crossoverGabil)
    
    ga = GSimpleGA.GSimpleGA(genome)

    if typeSelector == 1:
        ga.selector.set(Selectors.GRouletteWheel)
    else:
        ga.selector.set(Selectors.GRankSelector)
    ga.setGenerations(200)
    ga.setMutationRate(mutationRate)
    ga.setCrossoverRate(crossoverRate)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)


    ga.evolve(freq_stats=20)
    best = ga.bestIndividual()
    print best

    #print FitnessGabilAux(best)
    #print match([0,1,1,0,1,1], [0,1,0])
    suma = 0.0
    for ex in population:

        suma +=  match(best,ex)
    porcentaje = suma/float(len(population))
    print "Porcentaje correctamente clasificados: ", porcentaje

if __name__=="__main__":main()