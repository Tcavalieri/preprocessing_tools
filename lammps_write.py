import pandas as pd
import numpy as np

class LammpsData:
    
    def __init__(self):
        
        self.Nmasses = 0
        self.Natoms = 0
        self.Nbonds = 0
        self.Nangles = 0
        self.Ndihedrals = 0
        self.Nimpropers = 0

        self.Tmasses = 0
        self.Tatoms = 0
        self.Tbonds = 0
        self.Tangles = 0
        self.Tdihedrals = 0
        self.Timpropers = 0

        #self.atoms = {}
        #self.bonds = {}
        #self.angles = {}
        #self.dihedrals = {}
        #self.impropers = {}

    def charges_parse(self,filename,keys_array):
        '''
        This function read a Lammps data file line by line and parse the information inside it based on key_words provided by the user and return a dict of dataframe.
        Parameters:
        filename (string): the name of the file object of the parsing procedure. is a string.
        keys_array (array): is a matrix 2*n (or n*2 make no difference) to store multiple init and fin keywords if the document as multiple different section to be extracted.
        Return:
        tables_dict (dict): dictionary of dataframe.

        '''
        # keys array is a matrix 2*n (or n*2 make no difference)
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
                    
                    index = 'None'
                    for t in range(len(readfile)):
            
                        if readfile[t] == '#':
                            index = t
                    
                    if index != 'None':
                        supp = '-'.join(readfile[index:])
                        del readfile[index:]
                        readfile.append(supp)
                    
                    # this can handle problems if the line is empty
                    if len(readfile) == 0:
                        readfile = 'hellow'

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
                        file.append(readfile)

        #normalisation for the next slicing procedure
        file.append('hellow')
        file.append('End Table')
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
            'Charges', # from RESP/REPEAT method from CP2K file
            ]
        # creations of the headers for each different section of the data file
        headers_array = [
            ['resp','id','symbol','charge'],
        ]

        for i in range(len(init)):
            string_list = file[init[i]+1:fin[i]] # slicing of main file (i+1 and i-1 are needed to exclude the key sentences)
            #print(string_list)
            #tables_dict[tables_keys[i]] =  pd.DataFrame(string_list, columns=headers_array[i])
            intermidiate = pd.DataFrame(string_list, columns=headers_array[i]) 
            tables_dict[tables_keys[i]] = intermidiate.astype(float, errors='ignore') # this is used to convert data from string to float

        return tables_dict

    def init_parse(self,filename,keys_array):
        '''
        This function read a Lammps data file line by line and parse the information inside it based on key_words provided by the user and return a dict of dataframe.
        Parameters:
        filename (string): the name of the file object of the parsing procedure. is a string.
        keys_array (array): is a matrix 2*n (or n*2 make no difference) to store multiple init and fin keywords if the document as multiple different section to be extracted.
        Return:
        tables_dict (dict): dictionary of dataframe.

        '''
        # keys array is a matrix 2*n (or n*2 make no difference)
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
                    
                    index = 'None'
                    for t in range(len(readfile)):
            
                        if readfile[t] == '#':
                            index = t
                    
                    if index != 'None':
                        supp = '-'.join(readfile[index:])
                        del readfile[index:]
                        readfile.append(supp)
                    
                    # this can handle problems if the line is empty
                    if len(readfile) == 0:
                        readfile = 'hellow'

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
                        file.append(readfile)

        #normalisation for the next slicing procedure
        file.append('hellow')
        file.append('End Table')
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
            'Header', # to extract this part thefirst word of the first line is used 'LAMMPS'
            'Summary', # to extract this part the keyword 'Summary' needs to be introduce (see zif8_ms.data in this folder)
            'Box', # to extract this part the keyword 'Box' needs to be introduce the (see zif8_ms.data in this folder)
            'Masses',
            'Pair Coeffs',
            'Bond Coeffs',
            'Angle Coeffs',
            'Dihedral Coeffs',
            'Improper Coeffs',
            'BondBond Coeffs',
            'BondAngle Coeffs',
            'AngleAngle Coeffs',
            'AngleAngleTorsion Coeffs',
            'EndBondTorsion Coeffs',
            'MiddleBondTorsion Coeffs',
            'BondBond13 Coeffs',
            'AngleTorsion Coeffs',
            'Atoms',
            'Bonds',
            'Angles',
            'Dihedrals',
            'Impropers'
            ]
        # creations of the headers for each different section of the data file
        headers_array = [
            ['counts','ff_part'],
            ['counts','word1','word2'],
            ['xlo','xhi','word1','word2'],
            ['id','mass','type_name'],
            ['type','eps','sigma','name'], # pairs
            ['type','r0','K2','K3','K4','name'], # bonds
            ['type','theta0','K2','K3','K4','name'], # angles
            ['type','K1','phi1','K2','phi2','K3','phi3','name'], # dihedrals
            ['type','K','xi0','name'], # impropers
            ['type','M','r1','r2'], # bondbond
            ['type','N1','N2','r1','r2'], # bondangle
            ['type','M1','M2','M3','theta1','theta2','theta3'], #angleangle
            ['type','M','theta1','theta2'], # angleangletorsion
            ['type','B1','B2','B3','C1','C2','C3','r1','r3'], #endbondtorsion
            ['type','A1','A2','A3','r2'], #middlebondtorsion
            ['type','N','r1','r3'], #bondbond13
            ['type','D1','D2','D3','E1','E2','E3','theta1','theta2'], # angletorsion
            ['id','mol_id','type_id','q','x','y','z','unknown1','unknown2','unknown3','name'],
            ['id','type_id','atom1','atom2'],
            ['id','type_id','atom1','atom2','atom3'],
            ['id','type_id','atom1','atom2','atom3','atom4'],
            ['id','type_id','atom1','atom2','atom3','atom4']
        ]

        for i in range(len(init)):
            string_list = file[init[i]+2:fin[i]-1] # slicing of main file (i+2 and i-1 are needed to exclude the key sentences and the 'hellow' replacer for empty lines)
            #print(string_list)
            #tables_dict[tables_keys[i]] =  pd.DataFrame(string_list, columns=headers_array[i])
            intermidiate = pd.DataFrame(string_list, columns=headers_array[i]) 
            tables_dict[tables_keys[i]] = intermidiate.astype(float, errors='ignore') # this is used to convert data from string to float

        return tables_dict
    
    def refined_parse(self,data_dict):
        
        masses = data_dict['Masses']
        atoms = data_dict['Atoms']
        bonds = data_dict['Bonds']
        angles = data_dict['Angles']
        dihedrals = data_dict['Dihedrals']
        impropers = data_dict['Impropers']

        cbonds = data_dict['Bond Coeffs']
        cangles = data_dict['Angle Coeffs']
        cdihedrals = data_dict['Dihedral Coeffs']
        cimpropers = data_dict['Improper Coeffs']

        self.Nmasses = len(masses['id'])
        self.Natoms = len(atoms['id'])
        self.Nbonds = len(bonds['id'])
        self.Nangles = len(angles['id'])
        self.Ndihedrals = len(dihedrals['id'])
        self.Nimpropers = len(impropers['id'])

        uniques_masses = masses['id'].unique()
        uniques_atoms = atoms['type_id'].unique() # !? unsure to leave this or delete it
        uniques_bonds = cbonds['type'].unique()
        uniques_angles = cangles['type'].unique()
        uniques_dihedrals = cdihedrals['type'].unique()
        uniques_impropers = cimpropers['type'].unique()

        self.Tmasses = len(uniques_masses)
        self.Tatoms = len(uniques_atoms) # !? unsure to leave this or delete it
        self.Tbonds = len(uniques_bonds)
        self.Tangles = len(uniques_angles)
        self.Tdihedrals = len(uniques_dihedrals)
        self.Timpropers = len(uniques_impropers)

        counting = {}

        counting['Masses'] = masses['id'].value_counts()
        counting['Atoms'] = atoms['type_id'].value_counts()
        counting['Bonds'] = bonds['type_id'].value_counts()
        counting['Angles'] = angles['type_id'].value_counts()
        counting['Dihedrals'] = dihedrals['type_id'].value_counts()
        counting['Impropers'] = impropers['type_id'].value_counts()

        return counting

    def index_retrieve(self,data,selection,property):
        
        df = data[selection] # select the part of the data file of interest
        column = property[0] # the first element of property is a str with the name of property
        value = property[1] # the value of the property

        index_list = []

        for n in range(len(df[column])):
            #print(value, df.iloc[n][column])
            if df.iloc[n][column] == value:
                
                index_list.append(n + 1) # +1 because the index in python start from 0 while in the data file from 1
        return index_list

def df_to_txt(dict,file_name):
    """
    This function write the pandas dataframes in a dictionary to a txt file.
    parameters:
    dict (dict): dictionary of dataframes.
    file_name (str): name of the txt file which will be created ('name.extension').
    """   
    with open(file_name, 'w') as f:
        for key in dict.keys():
            f.write('\n'+'='*40 +'\n')
            f.write(key)
            f.write('\n'+'='*40 +'\n')
            f.write(dict[key].to_string(header=True, index=True))
        f.close()



keys_array = [
    ['LAMMPS','Summary','Box','Masses','Pair','Bond','Angle','Dihedral','Improper','BondBond','BondAngle','AngleAngle','AngleAngleTorsion','EndBondTorsion','MiddleBondTorsion','BondBond13','AngleTorsion','Atoms','Bonds','Angles','Dihedrals','Impropers'],
    ['Summary','Box','Masses','Pair','Bond','Angle','Dihedral','Improper','BondBond','BondAngle','AngleAngle','AngleAngleTorsion','EndBondTorsion','MiddleBondTorsion','BondBond13','AngleTorsion','Atoms','Bonds','Angles','Dihedrals','Impropers','End']
]

keys_array_charge = [
    ['Type'],
    ['Total']
]

read = LammpsData()
charge_unit_cell = read.charges_parse('charge_template_RESP-REPEAT_zif8.txt',keys_array_charge)
n = 1
limit = 7
charge_template = pd.concat([charge_unit_cell['Charges'],charge_unit_cell['Charges']],ignore_index=True)
while n < limit:
    charge_template = pd.concat([charge_template,charge_unit_cell['Charges']],ignore_index=True)
    n = n + 1
#print(charge_template)
data = read.init_parse('zif8_2x2x2.data',keys_array)
data_c = read.refined_parse(data)

#print(read.Nmasses, read.Tbonds)
#temp = charge_unit_cell['Charges']
#charges replacement

for k in range(0,len(charge_template['charge'])):
    data['Atoms'].iloc[k]['q'] = charge_template['charge'][k]
    
# writing of the data file

with open('zif82x2x2_ms.data','w') as f:

    f.write('LAMMPS test data file' + '\n\n')
    f.write(data['Header'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write(data['Summary'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write(data['Box'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Masses' + '\n\n')
    f.write(data['Masses'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Atoms' + '\n\n')
    f.write(data['Atoms'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Bonds' + '\n\n')
    f.write(data['Bonds'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Angles' + '\n\n')
    f.write(data['Angles'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Dihedrals' + '\n\n')
    f.write(data['Dihedrals'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.write('\n\n')
    f.write('Impropers' + '\n\n')
    f.write(data['Impropers'].astype(int, errors='ignore').to_string(header=False, index=False))
    f.close()

# refinements of improper comments

for k in range(read.Timpropers):
    if data['Improper Coeffs'].iloc[k]['name'] == None:
        data['Improper Coeffs'].iloc[k]['name'] = '#None'
# writing of the parm file class 2

pair = {}
bond = {}
angle = {}
bondbond = {}
bondangle = {}
dihedral = {}
mbt = {}
ebt = {}
anglet = {}
aat = {}
bondbond13 = {}
improper = {}
angleangle = {}

pair['keyword'] = ['pair_coeff']*read.Tmasses
bond['keyword'] = ['bond_coeff']*read.Tbonds
angle['keyword'] = ['angle_coeff']*read.Tangles
bondbond['keyword'] = ['angle_coeff']*read.Tangles
bondangle['keyword'] = ['angle_coeff']*read.Tangles
dihedral['keyword'] = ['dihedral_coeff']*read.Tdihedrals
mbt['keyword'] = ['dihedral_coeff']*read.Tdihedrals
ebt['keyword'] = ['dihedral_coeff']*read.Tdihedrals
anglet['keyword'] = ['dihedral_coeff']*read.Tdihedrals
aat['keyword'] = ['dihedral_coeff']*read.Tdihedrals
bondbond13['keyword'] = ['dihedral_coeff']*read.Tdihedrals
improper['keyword'] = ['improper_coeff']*read.Timpropers
angleangle['keyword'] = ['improper_coeff']*read.Timpropers

pair['index'] = []
ind = 0
for i in range(read.Tmasses):
    ind = ind + 1
    pair['index'].append(ind)
bondbond['parm'] = ['bb']*read.Tangles
bondangle['parm'] = ['ba']*read.Tangles
mbt['parm'] = ['mbt']*read.Tdihedrals
ebt['parm'] = ['ebt']*read.Tdihedrals
anglet['parm'] = ['at']*read.Tdihedrals
aat['parm'] = ['aat']*read.Tdihedrals
bondbond13['parm'] = ['bb13']*read.Tdihedrals
angleangle['parm'] = ['aa']*read.Timpropers

# Pair Coeffs lj/class2/coul/long
data['Pair Coeffs'].insert(loc=0,column ='keyword',value=pair['keyword'])
data['Pair Coeffs'].insert(loc=2,column ='type2',value=pair['index'])

data['Pair Coeffs']['type'] = data['Pair Coeffs']['type'].apply(int)

# Bonds class2
data['Bond Coeffs'].insert(loc=0,column ='keyword',value=bond['keyword'])

data['Bond Coeffs']['type'] = data['Bond Coeffs']['type'].apply(int)

# Angles class2
data['Angle Coeffs'].insert(loc=0,column ='keyword',value=angle['keyword'])
data['BondBond Coeffs'].insert(loc=0,column ='keyword',value=bondbond['keyword'])
data['BondBond Coeffs'].insert(loc=2,column ='parm',value=bondbond['parm'])
data['BondAngle Coeffs'].insert(loc=0,column ='keyword',value=bondangle['keyword'])
data['BondAngle Coeffs'].insert(loc=2,column ='parm',value=bondangle['parm'])

data['Angle Coeffs']['type'] = data['Angle Coeffs']['type'].apply(int)
data['BondBond Coeffs']['type'] = data['BondBond Coeffs']['type'].apply(int)
data['BondAngle Coeffs']['type'] = data['BondAngle Coeffs']['type'].apply(int)


# Dihedrals class2
data['Dihedral Coeffs'].insert(loc=0,column ='keyword',value=dihedral['keyword'])
data['MiddleBondTorsion Coeffs'].insert(loc=0,column ='keyword',value=mbt['keyword'])
data['MiddleBondTorsion Coeffs'].insert(loc=2,column ='parm',value=mbt['parm'])
data['EndBondTorsion Coeffs'].insert(loc=0,column ='keyword',value=ebt['keyword'])
data['EndBondTorsion Coeffs'].insert(loc=2,column ='parm',value=ebt['parm'])
data['AngleTorsion Coeffs'].insert(loc=0,column ='keyword',value=anglet['keyword'])
data['AngleTorsion Coeffs'].insert(loc=2,column ='parm',value=anglet['parm'])
data['AngleAngleTorsion Coeffs'].insert(loc=0,column ='keyword',value=aat['keyword'])
data['AngleAngleTorsion Coeffs'].insert(loc=2,column ='parm',value=aat['parm'])
data['BondBond13 Coeffs'].insert(loc=0,column ='keyword',value=bondbond13['keyword'])
data['BondBond13 Coeffs'].insert(loc=2,column ='parm',value=bondbond13['parm'])

data['Dihedral Coeffs']['type'] = data['Dihedral Coeffs']['type'].apply(int)
data['MiddleBondTorsion Coeffs']['type'] = data['MiddleBondTorsion Coeffs']['type'].apply(int)
data['EndBondTorsion Coeffs']['type'] = data['EndBondTorsion Coeffs']['type'].apply(int)
data['AngleTorsion Coeffs']['type'] = data['AngleTorsion Coeffs']['type'].apply(int)
data['AngleAngleTorsion Coeffs']['type'] = data['AngleAngleTorsion Coeffs']['type'].apply(int)
data['BondBond13 Coeffs']['type'] = data['BondBond13 Coeffs']['type'].apply(int)

# Impropers class2
data['Improper Coeffs'].insert(loc=0,column ='keyword',value=improper['keyword'])
data['AngleAngle Coeffs'].insert(loc=0,column ='keyword',value=angleangle['keyword'])
data['AngleAngle Coeffs'].insert(loc=2,column ='parm',value=angleangle['parm'])

data['Improper Coeffs']['type'] = data['Improper Coeffs']['type'].apply(int)
data['AngleAngle Coeffs']['type'] = data['AngleAngle Coeffs']['type'].apply(int)

#print(data['AngleAngleTorsion Coeffs'])

with open('parm.lammps','w') as f:

    f.write('#LAMMPS test parm file' + '\n\n')
    f.write('# Pair Coeffs (and charges) \n\n')
    f.write(data['Pair Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#Bonds Coeffs \n\n')
    f.write(data['Bond Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#Angle Coeffs \n\n')
    f.write(data['Angle Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#BondBond Coeffs \n\n')
    f.write(data['BondBond Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#BondAngle Coeffs \n\n')
    f.write(data['BondAngle Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#Dihedral Coeffs \n\n')
    f.write(data['Dihedral Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#MiddleBondTorsion Coeffs \n\n')
    f.write(data['MiddleBondTorsion Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#EndBondTorsion Coeffs \n\n')
    f.write(data['EndBondTorsion Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#AngleTorsion Coeffs \n\n')
    f.write(data['AngleTorsion Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#AngleAngleTorsion Coeffs \n\n')
    f.write(data['AngleAngleTorsion Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#BondBond13 Coeffs \n\n')
    f.write(data['BondBond13 Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#Improper Coeffs \n\n')
    f.write(data['Improper Coeffs'].to_string(header=False, index=False))
    f.write('\n\n')
    f.write('#AngleAngle Coeffs \n\n')
    f.write(data['AngleAngle Coeffs'].to_string(header=False, index=False))
    f.close()
