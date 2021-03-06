from numpy.random import choice
from space import space
from BOX import BOX
from Blok import Blok

class Solution:
    DisFromFront=[]
    def __init__(self, value ):
        self.value = value
        self.h_score = None
        self.VU=None
        self.WCG=None
        self.DFF=None #ignore
        self.totalBoxNumbers = None
        self.summary = [self.VU, self.WCG, self.totalBoxNumbers]
        self.Loading_Results=None
    
    def generate_children(self,numberOfRandomSwap):
        children=[]
        newValues = []
        for  _ in xrange(numberOfRandomSwap):
            newValue = []
            rep=choice(len(self.value),2,replace=False)
            rep.sort()
            newValue.extend(self.value[:rep[0]]+[self.value[rep[1]]]
            +self.value[rep[0]+1:rep[1]]
            +[self.value[rep[0]]]+self.value[rep[1]+1:])
            if(newValue not in newValues):
                newValues.append(newValue)
                children.append((Solution(newValue),tuple(rep)))
        return children
    

    def Total_Box_Number(self,Data):
        self.loading(Data)
        TotalNumberBox=sum([a.quantity for a in Blok.AllBloks ])   
        return int(TotalNumberBox)
        
        
        
    def loading(self,Data):
    #### loading hurestic ###
        space.reset()
        BOX.reset()
        Blok.reset()
        (L,W,H)=Data.contdim
        S=space(0,0,0,L,W,H)
        BOXS=[]
        for j in self.value:
            BOXS.append(BOX(Data,j))
        TotalInitialNumberBox=sum([a.quantity for a in BOXS ]) 
        while len(space.remainlist)!=0 and BOX.Is_unloaded_BOX():
            S=S.merge()
            j=0
            while(j<Data.ntype and len(space.remainlist)!=0):
                currentbox=BOXS[j]
                
                if (currentbox.quantity>0 and currentbox.Can_Load(S)):
                    BBlok=currentbox.Best_Blok(S)
                    BBlok.partition(S)
                    if len(space.remainlist)!=0:
                        S=space.curentspace()
                        j=0
                    else:
                        break
                        
                    S=S.merge()
                    #j+=1
                else:
                    j+=1
                    
            S.waste()
            if len(space.remainlist)!=0:
                S=space.curentspace()
            else:
                break
        TotalNumberBoxAfterLoad=sum([a.quantity for a in Blok.AllBloks ])
        self.totalBoxNumbers = (TotalNumberBoxAfterLoad,TotalInitialNumberBox)
            

    
    def Score_Calc(self, Data, alpha, beta, gamma ) :
        (L,W,H)=Data.contdim
        self.loading(Data)
        results=[]
        con_volume=L*W*H
        Utilized_volume=0
        CGX,CGY,CGZ = 0, 0, 0
        Totalweight=0
        DisX,Totalpriority=0,0
        Blok.blokweights(Data) # assign weights and priorities to Best Blockes
        for a in Blok.AllBloks:
            results.append((a.boxtype,a.boxori,a.quantity,a.priority,a.pos,a.L,a.W,a.H))
            Utilized_volume+=a.volume
            #Calculating the weight distrbution
            CGX += a.weight*(a.pos[0]+a.L/2)
            CGY += a.weight*(a.pos[1]+a.W/2)
            CGZ += a.weight*(a.pos[2]+a.H/2)
            Totalweight += a.weight
            
        CGX=CGX/Totalweight
        CGY=CGY/Totalweight
        CGZ=CGZ/Totalweight
        He=Utilized_volume/(L*W)
        Dist=max(abs(CGX-L/2)/(L/2),abs(CGY-W/2)/(W/2),abs(CGZ-He/2)/(He/2))
        WCG=(1-Dist)*100
        #Calculating the Volume utilisation
        VU=(Utilized_volume/con_volume)*100
        # Calcualting the distance from front
        
        DFF=((DisX)/L)*100
        self.summary = [VU, WCG, self.totalBoxNumbers[0],self.totalBoxNumbers[1]]
        results.append([""])
        results.append(["VOLUME Utilization","WCG", "Number of loaded boxes", "Initial number of boxes"])
        results.append(self.summary)
        self.h_score=alpha*VU+beta*WCG
        self.Loading_Results=results
        self.VU=VU
        self.DFF=DFF
        self.WCG=WCG
        Solution.DisFromFront.append(self.DFF)
        return (self.h_score,self)
        
        
    @classmethod
    def max_DFF(cls):
        return max(cls.DisFromFront)