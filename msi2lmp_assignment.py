import pandas as pd
from msi2lmp_stderr_read import msi2lmp_stderr_read
from pcff_frc_read import pcff_frc_read

# reading msi2lmp stderr file
stderr_keys = [
    ['Get'],
    ['Check']
]

stderr_dict = msi2lmp_stderr_read('output_msi2lmp_matrimid.txt',stderr_keys)

# reading pcff.frc file
keys_array = [
    [['#auto_equivalence','cff91_auto'],['#quadratic_bond','cff91_auto'],['#quartic_bond','cff91'],['#quadratic_angle','cff91_auto'],['#quartic_angle','cff91'],['#torsion_1','cff91_auto'],['#torsion_3','cff91'],['#wilson_out_of_plane','cff91'],['#wilson_out_of_plane','cff91_auto']],
    [['#bond_increments','cff91_auto'],['#quartic_bond','cff91'],['#quadratic_angle','cff91_auto'],['#quartic_angle','cff91'],['#torsion_1','cff91_auto'],['#torsion_3','cff91'],['#wilson_out_of_plane','cff91'],['#wilson_out_of_plane','cff91_auto'],['#nonbond(9-6)','cff91']]
]

pcff_dict = pcff_frc_read('pcff.frc',keys_array)

equil_df = pcff_dict['Auto_equivalence']

# bond search

new_bonds = {}
for element in stderr_dict['bond']:

    new_bonds[element] = []
    a = element.split('-')
    
    for item in a:
        mask_b = equil_df.loc[equil_df['type']==item]
        new_bonds[element].append(mask_b.iloc[0]['bond'])

# angle search       

new_angles = {}
for element in stderr_dict['angle']:

    new_angles[element] = []
    a = element.split('-')
    for i in range(len(a)):
        mask_a = equil_df.loc[equil_df['type']==a[i]]
        if i == 0 or i == 2:
            new_angles[element].append(mask_a.iloc[0]['angle_end'])
        elif i == 1:
            new_angles[element].append(mask_a.iloc[0]['angle_apex'])
#print(new_angles)

# Torsion search

new_torsions = {}
for element in stderr_dict['torsion']:

    new_torsions[element] = []
    a = element.split('-')
    for i in range(len(a)):
        mask_t = equil_df.loc[equil_df['type']==a[i]]
        if i == 0 or i == 3:
            new_torsions[element].append(mask_t.iloc[0]['torsion_end'])
        elif i == 1 or i == 2:
            new_torsions[element].append(mask_t.iloc[0]['torsion_center'])

#print(new_torsions)

# OOP search

new_OOPs = {}
for element in stderr_dict['oop']:

    new_OOPs[element] = []
    a = element.split('-')
    for i in range(len(a)):
        mask_o = equil_df.loc[equil_df['type']==a[i]]
        if i == 0 or i == 3:
            new_OOPs[element].append(mask_o.iloc[0]['OOP_end'])
        elif i == 1 or i == 2:
            new_OOPs[element].append(mask_o.iloc[0]['OOP_center'])
#print(new_OOPs)

# new bond assignment
quadratic_bond = pcff_dict['Quadratic_bond']
bond_parameters = {}
for key in new_bonds.keys():
    item = new_bonds[key]
    mask = quadratic_bond[quadratic_bond['I'] == item[0]]
    mask_2 = mask[mask['J']==item[1]]
    try:
        bond_parameters[key] = [mask_2.iloc[0]['R0'],mask_2.iloc[0]['K2']]
    except:
        try:
            mask = quadratic_bond[quadratic_bond['I'] == item[1]]
            mask_2 = mask[mask['J']==item[0]]
            bond_parameters[key] = [mask_2.iloc[0]['R0'],mask_2.iloc[0]['K2']]
        except:
            print(f'Unable to assign {key}')

    #bond_parameters[key] = [mask_2.iloc[0]['R0'],mask_2.iloc[0]['K2']]
#print(bond_parameters)

# new angle assignment
quadratic_angle = pcff_dict['Quadratic_angle']
angle_parameters = {}

for key in new_angles.keys():
    item = new_angles[key]
    
    mask = quadratic_angle[quadratic_angle['I'] == item[0]]
    mask_2 = mask[mask['J']==item[1]]
    mask_3 = mask_2[mask_2['K']==item[2]]
    try:
        angle_parameters[key] = [mask_3.iloc[0]['Theta0'],mask_3.iloc[0]['K2']]
    except:
        try:
            mask = quadratic_angle[quadratic_angle['I'] == item[2]]
            mask_2 = mask[mask['J']==item[1]]
            mask_3 = mask_2[mask_2['K']==item[0]]
            angle_parameters[key] = [mask_3.iloc[0]['Theta0'],mask_3.iloc[0]['K2']]
        except:
            try:
                mask = quadratic_angle[quadratic_angle['I'] == '*']
                mask_2 = mask[mask['J']==item[1]]
                mask_3 = mask_2[mask_2['K']=='*'] 
                angle_parameters[key] = [mask_3.iloc[0]['Theta0'],mask_3.iloc[0]['K2']]
            except:
                print(f'Unable to assign {key}')
    #print(mask_3)
    #angle_parameters[key] = [mask_3.iloc[0]['Theta0'],mask_3.iloc[0]['K2']]
#print(angle_parameters)

# new torsion assignment

torsion_1 = pcff_dict['Torsion_1']
torsion_parameters = {}

for key in new_torsions.keys():
    item = new_torsions[key]
    
    mask = torsion_1[torsion_1['I'] == item[0]]
    mask_2 = mask[mask['J']==item[1]]
    mask_3 = mask_2[mask_2['K']==item[2]]
    mask_4 = mask_3[mask_3['L']=='*']
    try:
        torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
    except:
        try:
            mask = torsion_1[torsion_1['I'] == '*']
            mask_2 = mask[mask['J']==item[2]]
            mask_3 = mask_2[mask_2['K']==item[1]]
            mask_4 = mask_3[mask_3['L']==item[0]]
            torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
        except:
            try:
                mask = torsion_1[torsion_1['I'] == '*']
                mask_2 = mask[mask['J']==item[1]]
                mask_3 = mask_2[mask_2['K']==item[2]]
                mask_4 = mask_3[mask_3['L']==item[3]]
                torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
            except:
                try:
                    mask = torsion_1[torsion_1['I'] == item[3]]
                    mask_2 = mask[mask['J']==item[2]]
                    mask_3 = mask_2[mask_2['K']==item[1]]
                    mask_4 = mask_3[mask_3['L']=='*']
                    torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
                except:
                    try:
                        mask = torsion_1[torsion_1['I'] == '*']
                        mask_2 = mask[mask['J']==item[2]]
                        mask_3 = mask_2[mask_2['K']==item[1]]
                        mask_4 = mask_3[mask_3['L']=='*']
                        torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
                    except:
                        try:
                            mask = torsion_1[torsion_1['I'] == '*']
                            mask_2 = mask[mask['J']==item[1]]
                            mask_3 = mask_2[mask_2['K']==item[2]]
                            mask_4 = mask_3[mask_3['L']=='*']
                            torsion_parameters[key] = [mask_4.iloc[0]['KPhi'],mask_4.iloc[0]['n'],mask_4.iloc[0]['Phi0']]
                        except:
                            print(f'Unable to assign {key}')
#print(torsion_parameters)   

# new OOP assignment

wilson_oop_auto = pcff_dict['Wilson_OOP_auto']
oop_parameters = {}

for key in new_OOPs.keys():
    item = new_OOPs[key]
    
    mask = wilson_oop_auto[wilson_oop_auto['I'] == '*']
    mask_2 = mask[mask['J']==item[1]]
    mask_3 = mask_2[mask_2['K']=='*']
    mask_4 = mask_3[mask_3['L']=='*']
    oop_parameters[key] = [mask_4.iloc[0]['KChi'],mask_4.iloc[0]['Chi0']]
#print(oop_parameters)
