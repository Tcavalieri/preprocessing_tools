import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def init_parse(filename,keys_array):
        '''
        This function read a Lammps data file line by line and parse the information inside it based on key_words provided by the user and return a dict of dataframe.
        Parameters:
        filename (string): the name of the file object of the parsing procedure. is a string.
        keys_array (array): is a matrix 2*n (or n*2 make no difference) to store multiple init and fin keywords if the document as multiple different section to be extracted.
        Return:
        tables_dict (dict): dictionary of dataframe.

        '''
        # keys array is an array with 2 columns and each element is a list of len 2
        # initialisation
        init_key = keys_array[0]
        fin_key = keys_array[1]
        i = 0
        file = []

        # main loop 
        for p in range(len(init_key)):
            n = 0
            k = 0
            a = False
            with open(filename,'r',encoding='utf8') as f:
                while True:
        
                    readfile = f.readline()
                    if not readfile:
                        break

                    readfile = readfile.strip()
                    readfile = readfile.split()
                    n = n + 1
                    
                    #index = 'None'
                    #for t in range(len(readfile)):
            
                    #    if readfile[t] == '#':
                    #        index = t
                    
                    #if index != 'None':
                    #    supp = '-'.join(readfile[index:])
                    #    del readfile[index:]
                    #    readfile.append(supp)
                    
                    # this can handle problems if the line is empty
                    if len(readfile) == 0:
                        readfile = ['hellow','hellow']
                    
                    if len(readfile) == 1:
                        readfile.append('hellow')

                    if readfile[0:2] == init_key[p]: # key sentence or word for finding the start of a table from log.lammps files
                        file.append('Begin Table')
                        k = n
                        a = False
        
                    if readfile[0:2] == fin_key[p]: # key sentence or word for finding the end of a table from log.lammps files
                        file.append('End Table')
                        a = True
        
                    if a == True:
                        k = n + 1
        
                    if k == 0:
                        continue
                    elif k >= n:
                        continue
                    elif k < n:
                        file.append(readfile)

        #normalisation for the next slicing procedure
        #file.append('hellow')
        #file.append('End Table')
        #print(file)
        init = []
        fin = []

        for i in range(len(file)):
            if file[i] == 'Begin Table':
                nn = i
                init.append(nn)
            if file[i] == 'End Table':
                kk = i
                fin.append(kk)
    
        # this if statement is to handle cases in witch the last table is incomplete because of a crash of the programm
        #if len(init)-1 == len(fin):
        #    fin.append(len(file))
    
        # initialization of the dictionary that stores every table of data
        
        tables_dict = {}
        tables_keys = [
            'Auto_equivalence', 
            'Quadratic_bond', 
            'Quartic_bond', 
            'Quadratic_angle',
            'Quartic_angle',
            'Torsion_1',
            'Torsion_3',
            'Wilson_OOP',
            'Wilson_OOP_auto'
            ]
        # creations of the headers for each different section of the data file
        headers_array = [
            ['ver','ref','type','nonB','bond_inct','bond','angle_end','angle_apex','torsion_end','torsion_centre','OOP_end','OOP_center'], # autoequivalence
            ['ver','ref','I','J','R0','K2'], # quadratic bond E = K2 * (R - R0)^2
            ['ver','ref','I','J','R0','K2','K3','K4'], # quartic bond E = K2 * (R - R0)^2  +  K3 * (R - R0)^3  +  K4 * (R - R0)^4
            ['ver','ref','I','J','K','Theta0','K2'], # quadratic angle E = K2 * (Theta - Theta0)^2
            ['ver','ref','I','J','K','Theta0','K2','K3','K4'], # quartic bond Delta = Theta - Theta0 , E = K2 * Delta^2  +  K3 * Delta^3  +  K4 * Delta^4
            ['ver','ref','I','J','K','L','KPhi','n','Phi0'], # torsion_1 E = Kphi * [ 1 + cos(n*Phi - Phi0) ]
            ['ver','ref','I','J','K','L','V(1)','Phi1(0)','V(2)','Phi2(0)','V(3)','Phi3(0)'], # torsion_3 E = SUM(n=1,3) { V(n) * [ 1 + cos(n*Phi - Phi0(n)) ] }
            ['ver','ref','I','J','K','L','KChi','Chi0'], # wilson_OOP E = K * (Chi - Chi0)^2
            ['ver','ref','I','J','K','L','KChi','Chi0'] # wilson_OOP_auto E = K * (Chi - Chi0)^2
        ]
        #print(file)
        for i in range(len(init)):
            if i == 0 or i == 4:
                string_list = file[init[i]+7:fin[i]-2] # slicing of main file (i+6 and i-2 are needed to exclude the key sentences and the 'hellow' replacer for empty lines)
            else:
                string_list = file[init[i]+6:fin[i]-2] # slicing of main file (i+6 and i-2 are needed to exclude the key sentences and the 'hellow' replacer for empty lines) 
            #print(string_list)
            #tables_dict[tables_keys[i]] =  pd.DataFrame(string_list, columns=headers_array[i])
            intermidiate = pd.DataFrame(string_list, columns=headers_array[i]) 
            tables_dict[tables_keys[i]] = intermidiate.astype(float, errors='ignore') # this is used to convert data from string to float

        return tables_dict


keys_array = [
    [['#auto_equivalence','cff91_auto'],['#quadratic_bond','cff91_auto'],['#quartic_bond','cff91'],['#quadratic_angle','cff91_auto'],['#quartic_angle','cff91'],['#torsion_1','cff91_auto'],['#torsion_3','cff91'],['#wilson_out_of_plane','cff91'],['#wilson_out_of_plane','cff91_auto']],
    [['#bond_increments','cff91_auto'],['#quartic_bond','cff91'],['#quadratic_angle','cff91_auto'],['#quartic_angle','cff91'],['#torsion_1','cff91_auto'],['#torsion_3','cff91'],['#wilson_out_of_plane','cff91'],['#wilson_out_of_plane','cff91_auto'],['#nonbond(9-6)','cff91']]
]

a = init_parse('pcff.frc',keys_array)
