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
    print sum_fitness_total

    for individual in population:
        individual["propability"] = individual["fitness"] / sum_fitness_total
        pop_aux.append(individual)

    population = pop_aux
    return population


# Realizamos la seleccion de los padres
def selection(population, num_hyp):
    prob = np.random.uniform(0,1)
    pop_aux = []
    k = 0
    for individual in population:
        if prob >= 0 and prob <= individual["propability"]:
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
def individual_selection(population):
	parents = []
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
		parents.append(child)
	return parents


# Operados de cruce
def crossover_aux(parent_1, parent_2, pc):
    cross = np.random.uniform(0,1)
    print cross
    if cross >= 0 and cross <= pc:
    	# VERIFICAR ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!!!!!!!!!!!!
        while True:
            crossover_index1_p1 = np.random.random_integers(1, len(parent_1))
            crossover_index2_p1 = np.random.random_integers(1, len(parent_2))
            if crossover_index2_p1 > crossover_index1_p1:
                break
                
        child_1 = parent_1[:crossover_index1_p1] + parent_2[crossover_index1_p1:crossover_index2_p1]+ parent_1[crossover_index2_p1:]
        child_2 = parent_2[:crossover_index1_p1] + parent_1[crossover_index1_p1:crossover_index2_p1]+ parent_2[crossover_index2_p1:]
        print crossover_index1_p1
        print crossover_index2_p1
    else:
        child_1 = parent_1
        child_2 = parent_2

   
    print "padre1: ", parent_1
    print "padre2: ", parent_2
    print "hijo1:  ", child_1
    print "hijo2:  ", child_2
    return [child_1, child_2]

def crossover(population, num_cross, pc):
	offsprings = []
	for x in range(num_cross*2):
		index1 = np.random.random_integers(0,len(population)-1)
		index2 = np.random.random_integers(0,len(population)-1)
		parent_1 = population[index1]
		parent_2 = population[index2]
		childs = crossover_aux(parent_1,parent_2, pc)
		offsprings.append(childs)
	return offsprings



# Operacion de mutacion
def mutate(individual, pm):
    for i in range(len(individual)):
    	muta = np.random.uniform(0,1)
    	print "muta: ",muta
    	print "index: ", i
    	if muta >= 0 and muta <= pm:  
	        if individual[i] == 0:
	            individual[i] = 1
	        else:
	            individual[i] = 0

	print individual

# Operacion de match
def match(example, individual):
	for x in range(len(example)):
		if (example[x] == 1) and (example[x] != individual[x]):
			return False

	return True

# Funcion de adaptacion (fitness)
def fitness(hypothesis, num_ex, parents):
	well = 0
	for individual in parents:
		check =  match(hypothesis["individual"],individual)
		if check == True:
			well += 1.0
	correct = well / num_ex	
	print "well: ", well
	hypothesis["fitness"] = correct*correct


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
	# Seleccionamos las muestras del conjunto de datos
	pop_aux = selection_random_hyp(population, 60)
	# Generamos los individuals aleatorios
	parents = individual_selection(population)
	# Calculamos los fitness iniciales
	for individual in pop_aux:
		fitness(individual, 60, parents)
		print individual["fitness"]

	maxi = max_fitness(pop_aux)
	while maxi < umbral:
		pop_aux1 = selection(pop_aux, (1-r)*p)
		pop_aux1 = pop_aux1 + crossover


		pass
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

        individual = tmp + tmp1 + tmp2 + tmp3 + tmp4
        population.append({"individual":individual, "fitness":0.0, "probability":0.0})
    
    
    #population = prob_selection_population(population)
    #print population
    print crossover_aux(population[0]["individual"], population[100]["individual"],0.6)
    #mutate(population[0][0], 0.2)
    #individual_selection(population)
    #parents = individual_selection(population)
    #pop_aux = selection_random_hyp(population, 60)
    #GABIL(population, 2,2,2,2)
    #fitness(([1,0,0,1],0.0,0.1), 3, [[1,0,0,1,1], [1,0,0,0]])
    

if __name__=="__main__":main()