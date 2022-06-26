from input import Input
from BOX import BOX
from space import space
from Solution import Solution
from numpy.random import choice
import time
import math
from tabu import Tabu_search

Data=Input(3,2)
MaxRunTime=5

alpha , beta , gamma = 0.8 , 0.2 , 0.3
tabulist_size=int(math.ceil(float(Data.ntype)/2))
max_solutions=100

Initial_sol= Solution(range(Data.ntype)) # gave a starting solution 
# Initial_sol.generate_children(10)
# Initial_sol.Score_Calc(Data, alpha, beta, gamma)
# print('Volume Utilization = %f ' %Initial_sol.VU) 
# Apply the Tabu

(Best_Sol,Runtime )=Tabu_search(Data, Initial_sol ,alpha , beta , gamma,
                                    tabulist_size, max_solutions=max_solutions ,MaxRunTime=4 )
print('Volume Utilization = %f ' %Best_Sol.VU)   
print(len(Best_Sol.Loading_Results))       