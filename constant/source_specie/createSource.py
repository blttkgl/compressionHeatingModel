import subprocess
import pdb

mechName = 'GRI'
# File name you want to give for the specie source term script
specieSource1= 'specieSource1_'+mechName+'.foam'
specieSource2= 'specieSource2_'+mechName+'.foam'

try:
    os.remove(specieSource1)
    os.remove(specieSource2)  
except:
    None

search = open("../thermo.compressibleGasGRI")
species_names = []
for line in search:
    if  'species' in line:
        nSpecies = int(search.readline())
        search.readline()
        for x in range(nSpecies):
            species_names.append(search.readline().split()[0])

for sp_i in species_names:
    print('Specie name is : %s' % sp_i)   
    with open(specieSource1,'a') as output1:
        output1.write('%s \n' % sp_i)
    with open(specieSource2,'a') as output2:
        output2.write('motored_pressure_specie_%s \n' % sp_i)
        output2.write('{\n\n')
        output2.write('\ttype \t scalarCodedSource;\n')
        output2.write('\tactive \t true;\n')
        output2.write('\tname \t sourceTime_%s;\n\n' % sp_i)
        output2.write('\tscalarCodedSourceCoeffs\n\t{\n')
        output2.write('\t\tselectionMode \t all;\n')
        output2.write('\t\tfields \t (%s);\n\n' % sp_i)
        output2.write('\t\tcodeInclude\n\t\t#{\n\n\t\t#};\n\n')
        output2.write('\t\tcodeCorrect\n\t\t#{\n\n\t\t#};\n\n')
        output2.write('\t\tcodeAddSup\n\t\t#{\n\n')
        output2.write('\t\t\tconst vectorField& C = mesh_.C();\n')
        output2.write('\t\t\tconst volScalarField& %s_sys =  mesh_.lookupObject<volScalarField>("%s"); \n' % (sp_i, sp_i))
        output2.write('\t\t\tscalarField& specieSource = eqn.source(); \n')
        output2.write('\t\t\tforAll(C, i)\n\t\t\t{\n\t\t\t\tspecieSource[i] *= %s_sys[i];\n\t\t\t}' % sp_i)
        output2.write('\n\t\t\tPout << "***codeAddSup***" << endl;')
        output2.write('\n\t\t#};\n\n')
        output2.write('\t\tcodeSetValue\n\t\t#{\n\n\t\t#};\n\n')
        output2.write('\t\tcode\n\t\t#{\n\t\t\t$codeInclude\n\t\t\t$codeCorrect\n\t\t\t$codeAddSup\n\t\t\t$codeSetValue\n\t\t#};')
        output2.write('\n\t}\n')
        output2.write('\n\tsourceTime_%sCoeffs\n\t{\n'% sp_i)
        output2.write('\t\t$scalarCodedSourceCoeffs;\n')
        output2.write('\t}\n')
        output2.write('}\n')



