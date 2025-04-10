import pandas as pd

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
                    supp = '-'.join(readfile[6:])
                    del readfile[6:]
                    readfile.append(supp)
                    
                    # this can handle problems if the line is empty
                    if len(readfile) == 0:
                        readfile = ['hellow','hellow']
                    
                    if len(readfile) == 1:
                        readfile.append('hellow')

                    if readfile[0] == init_key[p]: # key sentence or word for finding the start of a table from log.lammps files
                        file.append('Begin Table')
                        k = n
                        a = False
        
                    if readfile[0] == fin_key[p]: # key sentence or word for finding the end of a table from log.lammps files
                        file.append('End Table')
                        a = True
        
                    if a == True:
                        k = n + 1
        
                    if k == 0:
                        continue
                    elif k >= n:
                        continue
                    elif k < n:
                        supp = '-'.join(readfile[6:])
                        del readfile[6:]
                        readfile.append(supp)
                        file.append(readfile)

        #normalisation slicing

        file = file[:-2]
        # initialization of the dictionary that stores every table of data
        
        tables_dict = {}
        tables_keys = [
            'bond', 
            'angle', 
            'torsion', 
            'oop'
            ]
        
        for key in tables_keys:
            tables_dict[key] = []

        for item in file:
            print(item)
            if item[3] == 'bond':
                tables_dict['bond'].append(item[6])
            elif item[3] == 'angle':
                tables_dict['angle'].append(item[6])
            elif item[3] == 'torsion':
                tables_dict['torsion'].append(item[6])
            elif item[3] == 'oop':
                tables_dict['oop'].append(item[6])

        return tables_dict

keys_array = [
    ['Get'],
    ['Check']
]

a = init_parse('output_msi2lmp_matrimid.txt',keys_array)

print(a)
