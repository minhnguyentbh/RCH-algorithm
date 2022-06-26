import heapq # Libarary for array sorting  https://docs.python.org/2/library/heapq.html
import time
import numpy as np
import math
import pandas as pd
from Solution import Solution
from input import Input


  
def Write2Excel(results):
    solution=pd.DataFrame(results, columns=['Box Type','Box Oriantation in Blok','Box quantity in Blok','Box priority','Blok Starting point','lenght','Width','Hight'])
    solution.to_excel('loading hurestic results (Tabu).xlsx')
    return

def Tabu_search(Data, Initial_Sol,alpha , beta , gamma ,tabu_size, max_iterations=1000, max_solutions=100 , MaxRunTime=60):
    start=time.time()   # start the timer
    Solution_list = [ (-1*Initial_Sol.Score_Calc(Data, alpha , beta , gamma)[0], Initial_Sol) ]
    current_Sol= Solution(None) #init for while loop
    Best_Sol=Initial_Sol
    tabu_set = []
    it=1
    # Main Loop
    print('Volume Utilization = %f ' %Initial_Sol.VU) 
    while it<= max_iterations and time.time() <= start+MaxRunTime:
        # Select the solution with max score
        _  , current_Sol = heapq.heappop( Solution_list )
        # print('Volume Utilization of current solution = %f ' %current_Sol.VU) 
        # print('Volume Utilization = %f ' %current_Sol.VU) 
        # if the current solution is better than best solution so far change the best solution
        if current_Sol.h_score>Best_Sol.h_score:
            Best_Sol=current_Sol
            Best_Sol.Score_Calc(Data, alpha , beta , gamma)
            # print('Volume best Utilization = %f ' %Best_Sol.VU) 
        #print current_Sol.VU, len(Solution_list)
        # genearting new solutions
        for Sol,rep in current_Sol.generate_children(10):
            # Check if the move is in Tabu list or not
            if rep not in tabu_set:
                tabu_set = [rep] + tabu_set[:tabu_size-1]
                heapq.heappush( Solution_list, (-1*Sol.Score_Calc(Data, alpha , beta , gamma)[0],Sol)) # Add the new solution into the solution list
        
        # Maintain a fix lenght for the solution list
        Solution_list = Solution_list[:max_solutions]
        it+=1
        
    return (Best_Sol, time.time()-start)






# alpha , beta , gamma = 1 , 0 , 0 
# times=[3,5,10,15,30,60]
# filenumbers=[1,2,3,4,5,6,7]
# instances=[2,10,15,22,33,45,52,63,78,84]
# Final_results=np.zeros((6,7))
# for t,T in enumerate(times):
    
#     for f,FN in enumerate(filenumbers):
#         VU=[]
#         for PN in instances:
#             Data=Input(FN,PN)
#             #Data.RandomData(40)
#             MaxRunTime=T
            
            
#             tabulist_size=int(math.ceil(float(Data.ntype)/2))
#             max_solutions=2*Data.ntype
            
#             Initial_sol= Solution(range(Data.ntype)) # gave a starting solution 
#             # Apply the Tabu
            
#             (Best_Sol,Runtime )=Tabu_search( Initial_sol ,alpha , beta , gamma,
#                                                 tabulist_size, max_solutions=max_solutions ,MaxRunTime=MaxRunTime )
#             print('Volume Utilization = %f ' %Best_Sol.VU)    
#         VU.append(Best_Sol.VU)    
#         Final_results[t,f]=np.mean(VU)        
        

#print'Best Solution= ' ,Best_Sol.value #,100-Best_Sol.h_score)
#print('Volume Utilization = %f ' %Best_Sol.VU)
#print('Wieght distrbution measure= %f' %Best_Sol.WCG)
#print('Distance from back measure= %f where the maximum is %f' %(Best_Sol.DFF,Solution.max_DFF()))
#print('Run Time = %f sec' %Runtime)
#print('Total number of loaded boxes = %f' %Best_Sol.Total_Box_Number(Data))
#Write2Excel(Best_Sol.Loading_Results)
