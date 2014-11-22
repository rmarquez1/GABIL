import sys
import random
import numpy as np


# Para cada individual calculamos la propabilidad de que este sea escogido
def prob_selection_population(population):
    pop_aux = []
    # Calculamos la suma de todos fitness de la poblacion
    sum_fitness_total = 0.0
    for individual in population:
        sum_fitness_total += individual["fitness"]
    #print "Sum fitness: ", sum_fitness_total

    for individual in population:
    	if sum_fitness_total != 0.0:
        	individual["propability"] = individual["fitness"] / sum_fitness_total
        else: 
        	print "DIVISION POR CERO"
        	exit()
        pop_aux.append(individual)

    population = pop_aux
    return population


# Realizamos la seleccion de los padres
def selection(population, num_hyp):
	population = prob_selection_population(population)
	prob = np.random.uniform(0,1)
	pop_aux = []
	k = 0
	for individual in population:
		if prob >= 0 and prob <= individual["probability"]:
			pop_aux.append(individual)
			k += 1
		if k == num_hyp:
			break
	return pop_aux


def selection_random_hyp(population, n):
	type1 = []
	type2 = []
	type3 = []
	pop_aux = []
	maxi = n/3

	for i in range(maxi):
		rd = np.random.uniform(0,1)
		if rd >= 0 and rd <= 0.33:
			k = np.random.random_integers(0,15)
			pop_aux.append(population[k])
		elif rd > 0.33 and rd <= 0.66:
			k = np.random.random_integers(16,31)
			pop_aux.append(population[k])
		elif rd > 0.66:
			k = np.random.random_integers(32,49)
			pop_aux.append(population[k])

	for i in range(maxi):
		rd = np.random.uniform(0,1)
		if rd <= 0.33:
			k = np.random.random_integers(50,65)
			pop_aux.append(population[k])
		elif rd > 0.33 and rd <= 0.66:
			k = np.random.random_integers(66,81)
			pop_aux.append(population[k])
		elif rd > 0.66:
			k = np.random.random_integers(82,99)
			pop_aux.append(population[k])

	for i in range(maxi):
		rd = np.random.uniform(0,1)
		if rd <= 0.33:
			k = np.random.random_integers(100,115)
			pop_aux.append(population[k])
		elif rd > 0.33 and rd <= 0.66:
			k = np.random.random_integers(116,131)
			pop_aux.append(population[k])
		elif rd > 0.66:
			k = np.random.random_integers(132,149)
			pop_aux.append(population[k])

	return pop_aux


# Generamos 100 individuals aleatoriamente
def generating_individuals():
	individuals = []
	# Generamos 100 individuals
	for i in range(100):
		child = []
		while True:
			# Generamos un numero del 1 al 100. VERIFICAR ESTO!!!!!!!
			# Lanzamos dos veces el dado
			for x in range(2): 
				n = np.random.random_integers(1,100)
			if n % 30 == 0:
				for x in range(n):
					bit = np.random.random_integers(0,1)
					child.append(bit)
				break
		individuals.append({"individual": child, "fitness": 0.0, "probability": 0.0})
	return individuals


# Operados de cruce
def crossover_aux(parent_1, parent_2, pc):
    cross = np.random.uniform(0,1)
    if cross >= 0 and cross <= pc:
    	# VERIFICAR ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!!!!!!!!!!!!
        while True:
            crossover_index1_p1 = np.random.random_integers(1, len(parent_1))
            crossover_index2_p1 = np.random.random_integers(1, len(parent_2))
            if crossover_index2_p1 > crossover_index1_p1:
                break
         
        child_1 = parent_1
        child_2 = parent_2
        child_1["individual"] = parent_1["individual"][:crossover_index1_p1] + parent_2["individual"][crossover_index1_p1:crossover_index2_p1]+ parent_1["individual"][crossover_index2_p1:]
        child_2["individual"] = parent_2["individual"][:crossover_index1_p1] + parent_1["individual"][crossover_index1_p1:crossover_index2_p1]+ parent_2["individual"][crossover_index2_p1:]
        #print crossover_index1_p1
        #print crossover_index2_p1
    else:
        child_1 = parent_1
        child_2 = parent_2

   
    #print "padre1: ", parent_1
    #print "padre2: ", parent_2
    #print "hijo1:  ", child_1
    #print "hijo2:  ", child_2
    return [child_1, child_2]

def crossover(population, num_cross, pc):
	offsprings = []
	for x in range(int(num_cross*2)):
		index1 = np.random.random_integers(0,len(population)-1)
		index2 = np.random.random_integers(0,len(population)-1)
		parent_1 = population[index1]
		parent_2 = population[index2]
		childs = crossover_aux(parent_1,parent_2, pc)
		for x in childs:
			offsprings.append(x)
	return offsprings



# Operacion de mutacion
def mutate(population, pm):
	for individual in population:
		#print "Antes: ",  individual
		i = 0
		while i < len(individual["individual"]):
			muta = np.random.uniform(0,1)
			if muta >= 0 and muta <= pm:
				if individual["individual"][i] == 0:
					individual["individual"][i] = 1
				else:
					individual["individual"][i] = 0
			i += 1
	return population

# Operacion de match
def match(example, individual):
	k = 0
	i = 0
	ver = []
	while k < len(individual):
		while i < len(example):
			if (example[i] == 0) and (example[i] != individual[k]):
				ver.append(0)
				i = 0
				break
			else:
				ver.append(1)
				i += 1

		

# Funcion de adaptacion (fitness)
def fitness(individual, num_ex, parents):
	well = 0.0
	#print "Fitness anterior: ", individual["fitness"]
	for parent in parents:
		check =  match(parent,individual["individual"])
		#print check
		if check == True:
			well += 1.0
	correct = well / num_ex	
	#print "well: ", well
	individual["fitness"] = individual["fitness"] + (correct*correct)
	#print "Fitness Final: ", individual["fitness"]


def max_fitness(population):
	# Almacenamos todos los valores de los fitness
	val_fitness = []
	for individual in population:
		val_fitness.append(individual["fitness"])
	# Ordenamos de menos a mayor
	val_fitness.sort()
	# Ordenamos el diccionario de poblaciones de acuerdo al val_fitness
	population.sort(key = lambda x:val_fitness.index(x["fitness"]))
	return population[-1]

def GABIL(population, umbral, p,r,m):
	# Generamos los individuals aleatorios
	individuals = generating_individuals()
	# Seleccionamos las muestras del conjunto de datos
	#examples = selection_random_hyp(population, 60)
	examples = population
	# Calculamos los fitness iniciales
	for individual in individuals:
		fitness(individual, 150, examples)
		#print individual["fitness"]
	
	# Calculamos probabilidades iniciales
	#individuals = prob_selection_population(individuals)
	
	iterations = 0
	while iterations < 1000:
		#print "ITERATION: ", iterations
		pop_aux1 = selection(individuals, (1-r)*p)
		pop_aux1 = pop_aux1 + crossover(individuals, (r*p)/2,0.6)
		pop_aux1 = mutate(pop_aux1, m)
		individuals = pop_aux1
		#print "Individuals: ", individuals
		for individual in individuals:
			fitness(individual,150,examples)
		iterations += 1
	maxi = max_fitness(individuals)
	print maxi
	#print individuals
	suma = 0.0
	for ex in examples:
		ver = match(ex, maxi["individual"])
		print ver
		if ver == True:
			suma += 1.0
			print suma
	print "TAM: ", len(examples)
	print "SUMA: ", suma
	porcentaje = suma/float(len(examples))
	print "porcentaje: ", porcentaje
	return max_fitness(individuals)
		#print "TAM: ", len(pop_aux)
	#while max()
	#for x in pop_aux:
		#print x["fitness"]

def main():

    population = []

	#Verificamos que el pase de argumentos sea correcto
    if (len(sys.argv)<= 1):
        print "Utilice:"
        print "python nombrePrograma nombreArchivo"
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
    
    
    #population = prob_selection_population(population)
    #print population
    #print crossover_aux(population[0]["individual"], population[100]["individual"],0.6)
    #mutate(population, 0.2)
    #generating_individuals(population)
    #parents = generating_individuals(population)
    #pop_aux = selection_random_hyp(population, 60)
    GABIL(population, 0.05,150,0.6,0.2)
    #fitness(([1,0,0,1],0.0,0.1), 3, [[1,0,0,1,1], [1,0,0,0]])
    

if __name__=="__main__":main()