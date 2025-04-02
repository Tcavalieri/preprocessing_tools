# preprocessing_tools

This repository contains some Python scripts for the preprocessing of LAMMPS input files and other files useful as input of MD and GCMC simulations

This Python script contain a class able to store informations about the connectivity of a structure in the form of a *.data LAMMPS file.
Some of the methods included are used to rewrite the original *.data file in a *.data file with only the connectiviti informations, the Atoms attributes and the Box informations and an additional file called parm.lammps that stores all the force field parameters.
There is also a method that, given a CP2K file containing partial charges of the structure, can read the charges and assign them to the structure in the *.data file overwriting the original ones.
