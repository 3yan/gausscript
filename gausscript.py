#!/usr/bin/env python2
print("..::Yan's lazy chemist gaussian input creator::..")
#this program is inteded as another excercise in python and attempt to create comfort and usefull script for creating gaussian input file.

import argparse
import os




#defining of CLI arguments input according to documentation: https://docs.python.org/2/library/sys.html

clinput = argparse.ArgumentParser()
#we want file as geometry input
clinput.add_argument('-i', '--input', '--inputgeom', required=True,
        help='input geometry in gaussian format (for example Molden ZMat output)', type=file)
#we want filename to which we will write
clinput.add_argument('-o', '--outfile',
        help="""output file in which complete g09 input is fully defined and ready to be calculated. It's requied to be in correct format (*.gjf or *.com). If no file is defined it will automatically create file with same name to input file with .gjf suffix in current working directory""", type=str)
clinput.add_argument('-c', '--charge',
        help='charge of structure', type=int)
clinput.add_argument('-m', '--multiplicity',
        help='mutliplicity of structure', type=int)
clinput.add_argument('-r', '--routecard', type=file,
        help='file in which route card of calculation is stored (file content example: #QCISD(T) Opt Freq gfprint pop=full)')
clinput.add_argument('-M', '--memory', type=int,
        help='amount of ram (MB)')
clinput.add_argument('-N', '--nproc', type=int,
        help='number of processor')
args = clinput.parse_args()



#predefined route card list 
predefrc = [
          "#AM1 opt freq pop=full"
        , "#B3LYP/cc-pVDZ opt freq pop=full"
        ]





#processing arguments:
#read input geometry to memory and close it (https://docs.python.org/2/tutorial/inputoutput.html and for details https://docs.python.org/2/library/stdtypes.html#file-objects )
inputgeom = args.input.read()
args.input.close()

#check that outputfile is in a good format
if args.outfile == None:
    args.outfile = (os.path.basename(args.input.name) + ".gjf")
else:
    outsuffix = args.outfile[-4:]
    if not (outsuffix == ".gjf" or outsuffix == ".com"):
        print "\n\n\n          !!!ERROR!!! INCORRECT FORMAT OF OUTPUT FILE USED PLEASE SEE HELP FOR DETAILS\n\n\n\n"
        clinput.print_help()
        exit(1)

#if outputfile already exists ask if we should overwrite it (https://docs.python.org/2/library/os.path.html#os.path.exists, https://docs.python.org/2/library/stdtypes.html#str.format)
if os.path.exists(args.outfile):
    owerwrite = raw_input("""Output file {} already exists in filesystem, overwrite it? [y/N]: """.format(args.outfile))
    if owerwrite != 'y':
            print "\n\n\nNot overwriting already existing gaussian input file, exiting..."
            exit(0)

#if charge, multiplicity or number of cpus is not defined, define them (and restrict input to integer)
for i in ["charge", "multiplicity", "nproc"]:
    if getattr(args, i) == None:
        #https://docs.python.org/3/reference/compound_stmts.html#try
        infiniteloop = True
        while infiniteloop:
            try:
                setattr(args, i, int(raw_input("\n\n\n Please define {}: ".format(i))))
                infiniteloop = False
            except:
                print("excepted integer, please try to concentrate and write some nice integer when trying to set {}".format(i))
        #https://docs.python.org/2/library/stdtypes.html#str.title
    print ("""{} is set to {}\n""".format(i.title(),getattr(args, i)))

#same for memory, but it has unit so formatting is slightly different
if args.memory == None:
    infiniteloop = True
    while infiniteloop:
        try:
            args.memory = int(raw_input("\n\n\n Please define memory (MB): "))
            infiniteloop = False
        except:
            print("excepted integer, please try to concentrate and write some nice integer when trying to set Memory")
print ("""Memory is set to {} MB\n""".format(args.memory))

#if head file is defined read it, if not, just show our predefined heads..
if not (args.routecard == None):
    routecard = args.routecard.read()
    args.routecard.close()

#enumerate predefined heads (https://docs.python.org/2/library/functions.html#enumerate) and list them
else:
    print("No route card defined, please select one of predefined")
    for enumeratednum, enumeratedvalue in enumerate(predefrc, 1):
        print """{0}: {1}""".format(enumeratednum, enumeratedvalue)
    headnum = int(raw_input("\n Please select number of route card: "))-1
    print("")
    routecard = predefrc[headnum]
print ("""Route card is set to:\n{}""".format(routecard))






#we've everything what we need, so it's time to roll a dice
writeit = str(raw_input("""\n\n\n    All criterias was defined, write gaussian input into file "{}" ? [Y/n]""".format(args.outfile)))

if (writeit == 'n' or writeit == 'N' or writeit == 'No' or writeit == 'no'):
    print ("""\n\n\ncreation of configuration file "{}" canceled, exiting...""".format(args.outfile))
    exit(0)

print ("""creating/rewriting configuration file "{}" """.format(args.outfile))

outfile = open(args.outfile, 'w')
outfile.write("""%chk={}
%mem={}MB
%nproc={}
{}

{} {}
{}""".format((os.path.basename(args.outfile))[:-4] + ".chk", args.memory, args.nproc, routecard, args.charge, args.multiplicity, inputgeom))
outfile.close

exit(0)
