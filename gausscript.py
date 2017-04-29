#!/usr/bin/env python2
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
        print """\n\n\n Input {} is not file, exiting...""".format(args.input)
        exit(0)
else:
    #if it's batch input we generate all what looks save to generate and skip wierdnesses
    try:
        inputfiles = os.listdir(args.input)
        print """\n\n\n"""
    except:
        print """\n\n\n Input {} is not folder, exiting...""".format(args.input)
        exit(0)
    for i in inputfiles:
        filepath = args.input + "/" + i
        #need to process .xyz geometry exception..
        insuffix = i[-4:]
        if (insuffix == ".gjf" or insuffix == ".com"):
            print """Skipping {} - looks like output file...""".format(filepath)
        elif os.path.isdir(filepath):
            print """Skipping {} - looks like directory...""".format(filepath)
        elif os.path.exists(filepath + ".gjf"):
            print """Skipping {0} - looks like already have it's counterpart {0}.gjf...""".format(filepath)
        elif insuffix == ".xyz" and os.path.exists(filepath[:-4] + ".gjf"):
            print """Skipping {0}.xyz - looks like already have it's counterpart {0}.gjf...""".format(filepath[:-4])
        else:
            try:
                # END OF HERE WORKING ...
                inputfile = open(filepath,'r')
                inputgeom.append(inputfile.read())
                inputfile.close()
                jobname.append(i)
                print """Adding {} to input array...""".format(filepath)
            except:
                print """{} is not proper file, skipping...""".format(filepath)
    jobnames = """{}""".format(jobname)
    print """listing DONE, will process files {} from directory {}""".format(jobnames[1:-1], args.input)

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
        owerwrite = raw_input("""Output file '{}' already exists in filesystem, overwrite it? [y/N]: """.format(outfile[0]))
        if owerwrite != 'y':
            print "\n\n\nNot overwriting already existing gaussian input file, exiting..."
            exit(0)

#generate output file names if running in batch mode
else:
    for i in jobname:
        outfile.append(os.path.basename(i) + ".gjf")


#if charge, multiplicity or number of cpus is not defined, define them (and restrict input to integer)
for i in ["charge", "multiplicity", "nproc"]:
    if getattr(args, i) == None:
        #https://docs.python.org/3/reference/compound_stmts.html#try
        infiniteloop = True
        while infiniteloop:
            rawinput = (raw_input("\n\n\n Please define {} (or x to exit): ".format(i)))
            if rawinput == 'x' :
                print("x pressed, exiting...")
                exit(0)
            try:
                setattr(args, i, int(rawinput))
                infiniteloop = False
            except:
                print("excepted integer, please try to concentrate and write some nice integer when trying to set {}".format(i))
        #https://docs.python.org/2/library/stdtypes.html#str.title
    print ("""{} is set to {}\n""".format(i.title(),getattr(args, i)))

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
print ("""Memory is set to {} MB\n""".format(args.memory))

#if head file is defined read it, if not, just show our predefined heads..
if not (args.routecard == None):
    routecard = args.routecard.readline()
    if routecard[-1:] == """\n""":
        routecard = routecard[:-1]
    args.routecard.close()

#enumerate predefined heads (https://docs.python.org/2/library/functions.html#enumerate) and list them
else:
    print("No route card defined, please select one of predefined")
    for enumeratednum, enumeratedvalue in enumerate(predefrc, 1):
        print """{0}: {1}""".format(enumeratednum, enumeratedvalue)
    headnum = int(raw_input("\n Please select number of route card: "))-1
    print("")
    routecard = predefrc[headnum]
print ("""Route card is set to:\n'{}'""".format(routecard))






#we've everything what we need, so it's time to roll a dice
outfilelist = """{}""".format(outfile)
writeit = str(raw_input("""\n\n\n    All criterias was defined, write gaussian input into file(s) {} ? [Y/n]""".format(outfilelist[1:-1])))

if (writeit == 'n' or writeit == 'N' or writeit == 'No' or writeit == 'no'):
    print ("""\n\n\ncreation of configuration file(s) {} canceled, exiting...""".format(outfilelist[1:-1]))
    exit(0)

print ("""creating/rewriting configuration file(s) {} """.format(outfilelist[1:-1]))

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
"""%chk={}
%mem={}MB
%nproc={}
{}


{} {}
{}""".format(j[:-4] + ".chk", args.memory, args.nproc, routecard, args.charge, args.multiplicity, geometry))
    outfile.close

exit(0)
