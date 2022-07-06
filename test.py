from input import Input
from BOX import BOX
from space import space
from Solution import Solution
from numpy.random import choice
import time
import math
from tabu import Tabu_search
import pandas as pd

def Write2Excel(results):
    writer = pd.ExcelWriter('loading hurestic results (Tabu).xlsx') 
    solution=pd.DataFrame(results, columns=['Box Type','Box Oriantation in Blok','Quantity of box in Blok','Box priority','Blok Starting point','lenght','Width','Height'])
    solution.to_excel(writer, sheet_name='sheet_1')
    for column in solution:
        column_width = max(solution[column].astype(str).map(len).max(), len(column))
        col_idx = solution.columns.get_loc(column)
        writer.sheets['sheet_1'].set_column(col_idx, col_idx, column_width)
    writer.save()
    return

Data=Input(7,2)
MaxRunTime=5

alpha , beta , gamma = 1 , 0 , 0
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
print(Best_Sol.totalBoxNumbers) 
print(len(Best_Sol.Loading_Results))  
Write2Excel(Best_Sol.Loading_Results)     