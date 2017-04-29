#!/usr/bin/python2.5
print("..::Yan's lazy chemist gaussian input creator::..")
#this program is inteded as another excercise in python and attempt to create comfort and usefull script for creating gaussian input file.

import argparse
import os




#defining of CLI arguments input according to documentation: https://docs.python.org/2/library/sys.html

clinput = argparse.ArgumentParser()
#we want file as geometry input
clinput.add_argument('-i', '--input', '--inputgeom', required=True,
        help='input geometry in gaussian format (for example Molden ZMat output), when in batch mode it must be folder containing files of type mentioned above', type=str)
#we want filename to which we will write
clinput.add_argument('-o', '--outfile',
        help="""output file in which complete g09 input is fully defined and ready to be calculated. It's requied to be in correct format (*.gjf or *.com). If no file is defined it will automatically create file with same name to input file with .gjf suffix in current working directory, if running in batch-mode this argument will be ignored and input filename with gjf suffix will be used instead""", type=str)
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
clinput.add_argument('-b', '--batch', action='store_true', help='run command in a batch mode (you must cast it on folder which contains files instead on file, for easiness of operation outfile command would be ignored and INPUT.gjf format for output files will be used instead)')
args = clinput.parse_args()



#predefined route card list 
predefrc = [
          "#AM1 opt freq pop=full"
        , "#B3LYP/def2-SVP opt pop=full"
        , "#B3LYP/def2-SVP opt freq pop=full"
        ]


jobname = []
inputgeom = []
outfile = []


#processing arguments:
#read input geometry to memory and close it (https://docs.python.org/2/tutorial/inputoutput.html and for details https://docs.python.org/2/library/stdtypes.html#file-objects )
if args.batch == False:
    filepath="."
    try:
        inputfile = open(args.input,'r')
        inputgeom.append(inputfile.read())
        inputfile.close()
        jobname.append(args.input)
    except:
        print """\n\n\n Input %s is not file, exiting...""" %((args.input))
        exit(0)
else:
    #if it's batch input we generate all what looks save to generate and skip wierdnesses
    try:
        inputfiles = os.listdir(args.input)
        print """\n\n\n"""
    except:
        print """\n\n\n Input %s is not folder, exiting..."""%((args.input))
        exit(0)
    for i in inputfiles:
        filepath = args.input + "/" + i
        #need to process .xyz geometry exception..
        insuffix = i[-4:]
        if (insuffix == ".gjf" or insuffix == ".com"):
            print """Skipping %s - looks like output file..."""%((filepath))
        elif os.path.isdir(filepath):
            print """Skipping %s - looks like directory..."""%((filepath))
        elif os.path.exists(filepath + ".gjf"):
            print """Skipping %s - looks like already have it's counterpart %s.gjf..."""%((filepath, filepath))
        elif insuffix == ".xyz" and os.path.exists(filepath[:-4] + ".gjf"):
            print """Skipping %s.xyz - looks like already have it's counterpart %s.gjf..."""%((filepath[:-4],filepath[:-4]))
        else:
            try:
                # END OF HERE WORKING ...
                inputfile = open(filepath,'r')
                inputgeom.append(inputfile.read())
                inputfile.close()
                jobname.append(i)
                print """Adding %s to input array..."""%((filepath))
            except:
                print """%s is not proper file, skipping..."""%((filepath))
    jobnames = """%s"""%((filepath))
    print """listing DONE, will process files %s from directory %s"""%((jobnames[1:-1], filepath))

#if input is in .xyz format, remove suffix in case of jobname
for i,j in enumerate(jobname):
    name = j
    insuffix = j[-4:]
    if insuffix == ".xyz":
        jobname[i] = name[:-4]

#check that outputfile is in a good format If not running in batch mode
if args.batch == False:
    if args.outfile == None:
        outfile.append(os.path.basename(jobname[0]) + ".gjf")
    else:
        outsuffix = args.outfile[-4:]
        if not (outsuffix == ".gjf" or outsuffix == ".com"):
            print "\n\n\n          !!!ERROR!!! INCORRECT FORMAT OF OUTPUT FILE USED PLEASE SEE HELP FOR DETAILS\n\n\n\n"
            clinput.print_help()
            exit(1)
        outfile.append(outfile[0])
    #if outputfile already exists ask if we should overwrite it (https://docs.python.org/2/library/os.path.html#os.path.exists, https://docs.python.org/2/library/stdtypes.html#str.format)
    if os.path.exists(outfile[0]):
        owerwrite = raw_input("""Output file %s already exists in filesystem, overwrite it? [y/N]: """ %((outfile[0])))
        if owerwrite != 'y':
            print "\n\n\nNot overwriting already existing gaussian input file, exiting..."
            exit(0)

#generate output file names if running in batch mode
else:
    for i in jobname:
        outfile.append(os.path.basename(i) + ".gjf")


#if charge.format(jobnames[1:-1], args.input), multiplicity or number of cpus is not defined, define them (and restrict input to integer)
for i in ["charge", "multiplicity", "nproc"]:
    if getattr(args, i) == None:
        #https://docs.python.org/3/reference/compound_stmts.html#try
        infiniteloop = True
        while infiniteloop:
            rawinput = (raw_input("\n\n\n Please define %s (or x to exit): " %((i))))
            if rawinput == 'x' :
                print("x pressed, exiting...")
                exit(0)
            try:
                setattr(args, i, int(rawinput))
                infiniteloop = False
            except:
                print("excepted integer, please try to concentrate and write some nice integer when trying to set %s"%((i)))
        #https://docs.python.org/2/library/stdtypes.html#str.title
    print ("""%s is set to %d\n"""%((i.title(),getattr(args, i))))

#same for memory, but it has unit so formatting is slightly different
if args.memory == None:
    infiniteloop = True
    while infiniteloop:
        rawinput = (raw_input("\n\n\n Please define memory (MB) (or x to exit): "))
        if rawinput == 'x' :
            print("x pressed, exiting...")
            exit(0)
        try:
            args.memory = int(rawinput)
            infiniteloop = False
        except:
            print("excepted integer, please try to concentrate and write some nice integer when trying to set Memory")
print ("""Memory is set to %d MB\n"""%((args.memory)))

#if head file is defined read it, if not, just show our predefined heads..
if not (args.routecard == None):
    routecard = args.routecard.readline()
    if routecard[-1:] == """\n""":
        routecard = routecard[:-1]
    args.routecard.close()

#enumerate predefined heads (https://docs.python.org/2/library/functions.html#enumerate) and list them
else:
    print("No route card defined, please select one of predefined")
    for enumeratednum, enumeratedvalue in enumerate(predefrc):
        print """%d: %s"""%(((enumeratednum + 1), enumeratedvalue))
    headnum = int(raw_input("\n Please select number of route card: "))-1
    print("")
    routecard = predefrc[headnum]
print ("""Route card is set to:\n'%s'"""%((routecard)))






#we've everything what we need, so it's time to roll a dice
outfilelist = """%s"""%((outfile))
writeit = str(raw_input("""\n\n\n    All criterias was defined, write gaussian input into file(s) %s ? [Y/n]"""%((outfilelist[1:-1]))))

if (writeit == 'n' or writeit == 'N' or writeit == 'No' or writeit == 'no'):
    print ("""\n\n\ncreation of configuration file(s) %s canceled, exiting..."""%((outfilelist[1:-1])))
    exit(0)

print ("""creating/rewriting configuration file(s) %s"""%((outfilelist[1:-1])))

for i,j in enumerate(outfile):
    if args.batch == False:
        setattr(args,"input",".") 
    filepath = args.input + "/" + j
    outfile = open(filepath,'w')
    geometry = inputgeom[i]
    #need empty line on end of gjf file, otherwise gaussian is likely to fail
    if geometry[-2:] != """\n\n""":
        geometry = geometry + """\n"""
    outfile.write(
"""%%chk=%s
%%mem=%dMB
%%nproc=%d
%s


%d %d
%s"""%((j[:-4] + ".chk", args.memory, args.nproc, routecard, args.charge, args.multiplicity, geometry)))
    outfile.close

exit(0)
