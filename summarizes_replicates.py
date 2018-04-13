#This script is useful to calculate bootstrap support for groups suggested by population assignment methods.
#After running the methods on bootstrapped data sets, this script takes the set of outputs and compares it to the main result that is being evaluated
#THIS RESULT NEEDS TO BE IN THE SAME FOLDER OF THE SCRIPT AND CONSISTS OF A TXT FILE IN THE FOLLOWING FORMAT:
##1	3
##2	3
##3	NA
##4	3
##5	3
##6	3
##7	2
##8	3
##9	3
##10	5
##....
#Below you add the name of this file.
filename="yourfilename"
#The first column is the individual index, the second column is the group assignment, separated by a tab. "NA" is acceptable in the second column.
#The number of individuals in the analyses needs to be the same as the individuals in the list.

#This was designed for two types of tables: the "R" write.table output and the structure output.
#Choose the format for your data here by uncommenting the correct file format:
meth="R"
#meth="structure"
#R format: In this case the script goes through a series of files in which K is already assumed to have been selected. The script needs to be placed in the same folder as these outputs.
#structure format: in this case the script will be placed in a directory containing as many folders as data sets, each folder with all the runs (different Ks and different replicates per K) for each dataset
#In the structure case the script will first go through all the runs contained in a folder, select the run with the highest lnprob and then use it as the result of that particular dataset

#the outputs will be the result per individual and also a summary across groups. These will be on different files.
import os
def cria_lista_assign_r(fich):
    fil=file(fich,"r")
    lin=fil.read()
    u=lin.split("\n")
    k=int(u[0].split('"')[-2].replace("V",""))
    ass=[]
    for ind in u[1:]:
        if ind!="":
            pa=[]
            x=ind.split(" ")[1:]
            for w in x:
                    pa.append(float(w))
            if max(pa)>0.75:
                ass.append(pa.index(max(pa))+1)
            else:
                ass.append("NA")
    return [ass,k]
def cria_lista_assign_str(folder):
    os.chdir(folder)
    lnsks=[]
    c=os.getcwd()
    di=os.listdir(c)
    for fil in di:
        if "_f" in fil:
            x=file(fil,"r")
            y=x.read()
            lnprob=float(y.split("Estimated Ln Prob of Data   = ")[1].split("\n")[0])
            k=int(y.split(" populations assumed")[0].split(" ")[-1])
            var=float(y.split("Variance of ln likelihood   = ")[1].split("\n")[0])
            lnsks.append([k,lnprob,var,fil])
    ln=[]
    for u in lnsks:
        ln.append(u[1])
    var2=[]
    for f in lnsks:
        if f[1]==max(ln):
            var2.append(f[2])
    bestfile=""
    for f2 in lnsks:
        if f2[1]==max(ln):
            if f2[2]==min(var2):
                bestk=f2[0]
                bestfile=f2[3]
    fich=file(bestfile,"r")
    linhas=fich.read()
    imp=linhas.split("Inferred clusters (and 90% probability intervals)")[1].split("Estimated Allele Frequencies in each cluster")[0].split("\n")
    propmemb=[]
    for ind in imp:
        if ind not in [""," ","\n"]:
            pm=[]
            t=ind.split(":")[1].split("(")[0].split(" ")
            for p in t:
                try:
                    pm.append(float(p))
                except ValueError:
                    pass
            propmemb.append(pm)
    ass=[]
    for indiv in propmemb:
        if max(indiv)>0.75:
            ass.append(indiv.index(max(indiv))+1)
        else:
            ass.append("NA")
    return [ass,k]

def le_lista_ref(fich):
    a=[]
    u=file(fich,"r")
    t=u.read()
    w=t.split("\n")
    for ind in w:
        if ind not in [""," ","\n"]:
            a.append(ind.split("\t")[1])
    return a

def media(lista):
    return sum(lista)*1.0/len(lista)

def companheiros(x,listaref):
    a=[]
    for i in range(len(listaref)):
        if listaref[i]==listaref[x]:
            a.append(i)
    return a
#"comp" is a list of the indexes of individuals that in the real analyses have the same assignment; "lista1" is a list of assignments (e.g. bootstrap replicates) that will be compared to "comp"
def grupo_modal_comp(comp, lista1):
    #"u" is the list  of different groups to which members of lista1 appear assigned to
    u=[]
    #"ass" is the list with all the assignments of individuals of interest in the replicate in question
    ass=[]
    for i in comp:
        ass.append(lista1[i])
    for e in ass:
        if e not in u:
            u.append(e)
    #"conta" is a list with the absolute frequency of each group in lista1, in the order they appear in "u"
    conta=[]
    for t in u:
        cou=ass.count(t)
        conta.append(cou)
    #maximum frequency
    x=max(conta)
    #number of modal groups
    ngmod=conta.count(x)
    t=1
    o=conta.index(x)
    #indexes in "conta" and "u" of the modal groups. first just the first group and later on of the others
    lista=[o]
    while t<ngmod:
        o=conta[(o+1):].index(x)+o+1
        t+=1
        lista.append(o)
    grmod=[]
    for a in lista:
        grmod.append(u[a])
    #"grmod" is a list of names (=numbers) of the modal groups
    return grmod



u=os.getcwd()
w=os.listdir(u)
listaass=[]
typ="boot"



listaref=le_lista_ref(filename)
kfile=file("k_values_"+typ+"_"+meth+".txt","w")
outtot=file("individual_scores_rep_"+typ+"_"+meth+".txt","w")
outind=file("individual_summary_"+typ+"_"+meth+".txt","w")
outgroups=file("group_summary_"+typ+"_"+meth+".txt","w")
w.remove(filename)

if meth =="R":
    for i in w:
        if ".out" in i:
            listaass.append(cria_lista_assign_r(i)[0])
            kfile.write(str(cria_lista_assign_r(i)[1])+"\n")
elif meth=="structure":
    for i in w:
        if "." not in i:
            listaass.append(cria_lista_assign_str(a+"\\"+i)[0])
            kfile.write(str(cria_lista_assign_str(a+"\\"+i)[1])+"\n")

indivscores=[]
for ind in range(len(listaref)):
    outtot.write(str(ind+1))
    indscores=[]
    #for each replicate
    for rep in range(len(listaass)):
    
        #if an individual is in the same group in real and replicate analyses:
        if listaref[ind]!="NA":
            if listaass[rep][ind]!="NA":
                if len(companheiros(ind,listaref))==1:
                    if listaass[rep].count(listaref[ind])==1:
                        x=1
                        #if the group has a single element the results are consisten (x=1), otherwise they are not
                    else:
                        x=0
                else:
                    a=grupo_modal_comp(companheiros(ind,listaref),listaass[rep])
                    b=len(a)
                    #if there is only one modal group, either the result is consistent (x=1) or not (x=0)
                    if b==1:
                        if a[0]==listaass[rep][ind]:
                            x=1
                        else:
                            x=0
                    else:
                        #if there is more than one modal group in the replicate
                        t=0
                        for u in a:
                            if u==listaass[rep][ind]:
                                t+=1
                        #if the individual does not belong to any of the modal groups, the result is inconsistent
                        if t==0:
                            x=0
                        #if it does, the score is 1/(number of modal groups)
                        else:
                            x=1.0/len(a)                
            else:
                x=0
        else:
            x="NA"
        indscores.append(x)
        outtot.write("\t"+str(x))
    indivscores.append(indscores)
    outtot.write("\n")
gruposfeitos=[]
for f in range(len(indivscores)):
    if "NA" not in indivscores[f]:
        outind.write(str(f+1)+"\t"+str(media(indivscores[f]))+"\n")
    else:
        outind.write(str(f+1)+"\tNA\n")  
    if listaref[f] not in gruposfeitos:
        if listaref[f]!="NA":
            medias=[]
            gruposfeitos.append(listaref[f])
            amigos=companheiros(f,listaref)
            for am in amigos:
                medias.append(media(indivscores[am]))
            outgroups.write(str(listaref[f])+"\t"+str(media(medias))+"\n")
outgroups.close()
outind.close()
kfile.close()
