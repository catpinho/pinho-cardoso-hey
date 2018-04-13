#this function compares 2 classifications, corresponding to 2 lists with the same number of individuals, and calculates Rand Index for each comparison
#the lists need to have the individual classifications in the same order
def rand_index(list1,list2):
    #a: number of pairs of items classified in the same group in list1 and list2
    #b: number of pairs of items classified in different groups for list1 and list2
    #c: number of item pairs that are classified in the same group in list one and in a different group in list two
    #d: number of item pairs that are classified in the same group in list two and in a different group in list one
    a=0
    b=0
    c=0
    d=0

    tot=0
    for i in range(len(lista1)-1):
    
        for j in range(i+1,len(lista1)):
            
            if lista1[i]==lista1[j]:
                if lista2[i]==lista2[j]:
                    a+=1
                
                else:
                    c+=1

            else:
                if lista2[i]==lista2[j]:
                    d+=1
                else:
                    b+=1
    return (a+b)*1.0/(a+b+c+d)
