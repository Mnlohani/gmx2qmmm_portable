# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

#this will read prepared fields and files for a qmmm job based on gmx.
#will not work alone!

__author__ = "jangoetze"
__date__ = "$06-Feb-2018 12:45:17$"

def logger(log,logstring):
	from datetime import datetime
	with open(log,"a") as ofile:
		ofile.write(str(datetime.now()) + " " + logstring)

def get_full_coords_nm(gro):
	import re
	fullcoords=[]
	with open(gro) as ifile:#read ALL atom coordinates
		count=0
		for line in ifile:#skip four lines
			if count==4:
				break
			count+=1
		for line in ifile:
			match=re.search(r'^(.{5})\s(.{5})\s(.{5})\s(.{6})\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)', line,flags=re.MULTILINE)
			if not match:
				break
			full_coord_line=[float(match.group(5)),float(match.group(6)),float(match.group(7))]
			fullcoords.append(full_coord_line)
	return fullcoords

def get_full_coords_angstrom(gro):
	import re
	fullcoords=[]
	with open(gro) as ifile:#read ALL atom coordinates
		count=0
		for line in ifile:#skip four lines
                        count+=1
			if count==4:
				break
		count=0
		for line in ifile:
			count+=1
			match=re.search(r'^(.{5})\s(.{5})\s(.{5})\s(.{6})\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)', line,flags=re.MULTILINE)
			if not match:
				break
			full_coord_line=[float(match.group(5))*10.,float(match.group(6))*10.,float(match.group(7))*10.]
			fullcoords.append(full_coord_line)
	return fullcoords

def get_atoms(qmmmtop,logfile):
	import re
	import math
	atoms=[]
	mass_map = {"H" : "1.008", "He" : "4.0026", "Li" : "6.94", "Be" : "9.0122", "B" : "10.81", "C" : "12.011", "N" : "14.007", "O" : "15.999", "F" : "18.998", "Ne" : "20.180", "Na" : "22.990", "Mg" : "24.305", "Al" : "26.982", "Si" : "28.085", "P" : "30.974", "S" : "32.06", "Cl" : "35.45", "Ar" : "39.948", "K" : "39.098", "Ca" : "40.0784", "Sc" : "44.956", "Ti" : "47.867", "V" : "50.942", "Cr" : "51.996", "Mn" : "54.938", "Fe" : "55.8452", "Co" : "58.933", "Ni" : "58.693", "Cu" : "63.5463", "Zn" : "65.382", "Ga" : "69.723", "Ge" : "72.6308", "As" : "74.922", "Se" : "78.9718", "Br" : "79.904", "Kr" : "83.7982", "Rb" : "85.468", "Sr" : "87.62", "Y" : "88.906", "Zr" : "91.2242", "Nb" : "92.906", "Mo" : "95.95", "Tc" : "98.906254721", "Ru" : "101.072", "Rh" : "102.91", "Pd" : "106.42", "Ag" : "107.87", "Cd" : "112.41", "In" : "114.82", "Sn" : "118.71", "Sb" : "121.76", "Te" : "127.603", "I" : "126.90", "Xe" : "131.29", "Cs" : "132.91", "Ba" : "137.33", "La" : "138.91", "Ce" : "140.12", "Pr" : "140.91", "Nd" : "144.24", "Pm" : "144.9127493", "Sm" : "150.362", "Eu" : "151.96", "Gd" : "157.253", "Tb" : "158.93", "Dy" : "162.50", "Ho" : "164.93", "Er" : "167.26", "Tm" : "168.93", "Yb" : "173.05", "Lu" : "174.97", "Hf" : "178.492", "Ta" : "180.95", "W" : "183.84", "Re" : "186.21", "Os" : "190.233", "Ir" : "192.22", "Pt" : "195.08", "Au" : "196.97", "Hg" : "200.59", "Tl" : "204.38", "Pb" : "207.2", "Bi" : "208.98", "Po" : "208.982430420", "At" : "209.9871488", "Rn" : "222.017577725", "Fr" : "223.019735926", "Ra" : "226.025409825", "Ac" : "227.027752126", "Th" : "232.04", "Pa" : "231.04", "U" : "238.03", "Np" : "237.04817342", "Pu" : "244.0642045", "Am" : "243.061381125", "Cm" : "247.0703545", "Bk" : "247.0703076", "Cf" : "251.0795875", "Es" : "252.082985", "Fm" : "257.0951067", "Md" : "258.0984315", "No" : "259.1010311", "Lr" : "266.1198356", "Rf" : "267.1217962", "Db" : "268.1256757", "Sg" : "269.1286339", "Bh" : "270.1333631", "Hs" : "277.1519058", "Mt" : "278.1563168", "Ds" : "281.1645159", "Rg" : "282.1691272", "Cn" : "285.177126", "Nh" : "286.1822172", "Fl" : "289.190426", "Mc" : "289.1936389", "Lv" : "293.204496", "Ts" : "294.2104674", "Og" : "295.2162469"}
	name_map = {value: key for key, value in mass_map.items()}
	#name_list = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
	with open(qmmmtop) as ifile:
		for line in ifile:
			match=re.search(r'\[\s+moleculetype\s*\]', line,flags=re.MULTILINE)
			if match:
				break
		for line in ifile:
			match=re.search(r'\[\s+atoms\s*\]', line,flags=re.MULTILINE)
			if match:
				break
		for line in ifile:
			match=re.search(r'^\s*\[', line,flags=re.MULTILINE)
			if match:
				break
			match=re.search(r'^\s*(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+([-]*\d+[\.]*[\d+]*)\s+(\d+[\.]*[\d+]*)', line,flags=re.MULTILINE)
			if match:
				atomtype=str(match.group(2))
				atommass=float(match.group(8))
				foundname=""
				#obsolete: atom identification based on type. using mass now (see below)
#				testname=str(atomtype[0]).upper()
#				if testname in name_list:
#					foundname=testname
#					if len(atomtype)>1:
#						testname+=str(atomtype[1]).lower()
#						if testname in name_list:
#							foundname=testname
#				else:
#					if len(atomtype)>1:
#						testname+=str(atomtype[1]).lower()
#						if testname in name_list:
#							foundname=testname
				#find atom type based on mass
				for key in name_map.items():
					foundmass=key[0]
					massdiff=math.sqrt((float(atommass)-float(foundmass))*(float(atommass)-float(foundmass)))
					if massdiff<0.05:
						foundname=name_map[foundmass]
						break
				if foundname!="":
					testmass=mass_map[foundname]
					massdiff=math.sqrt((float(atommass)-float(foundmass))*(float(atommass)-float(foundmass)))
					if massdiff>0.01:
						logger(logfile,str("Found a mass of " + str(atommass) + " for atom type " + str(atomtype) + " (identified as atom name \"" + str(foundname) + "\"), which is more than 0.01 different from the expected mass of " + str(testmass) + ". Atom index was " + str(match.group(1)) + ". This has no effect except unless the atom was identified wrongly or dynamics are intended. Clean your ffnonbonded.itp to avoid these messages!\n"))
					atoms.append(foundname)
				else:
					logger(logfile,str("Atom type " + str(atomtype) + " could not be translated to a regular atom name. Exiting. Last line:\n"))
					logger(logfile,line)
					exit(1)
	return atoms

def write_mdp(mdpname,nbradius):
	with open(mdpname,"w") as ofile:
		ofile.write("title               =  Yo\ncpp                 =  /usr/bin/cpp\nconstraints         =  none\nintegrator          =  md\ndt                  =  0.001 ; ps !\nnsteps              =  1\nnstcomm             =  0\nnstxout             =  1\nnstvout             =  1\nnstfout             =   1\nnstlog              =  1\nnstenergy           =  1\nnstlist             =  1\nns_type             =  grid\nrlist               =  ")
		ofile.write(str(float(nbradius)))
		ofile.write("\ncutoff-scheme = group\ncoulombtype    =  cut-off\nrcoulomb            =  ")
		ofile.write(str(float(nbradius)))
		ofile.write("\nrvdw                =  ")
		ofile.write(str(float(nbradius)))
		ofile.write("\nTcoupl              =  no\nenergygrps          =  QM\nenergygrp-excl = QM QM\nPcoupl              =  no\ngen_vel             =  no\n")
		#ofile.write("\nTcoupl              =  no\nenergygrps          =  QM M1\nenergygrp-excl = QM QM QM M1\nPcoupl              =  no\ngen_vel             =  no\n")
	#	ofile.write("\nTcoupl              =  no\nenergygrps          =  QM\nPcoupl              =  no\ngen_vel             =  no\n")
		#ofile.write("\nTcoupl              =  no\nPcoupl              =  no\ngen_vel             =  no\n")

def get_nbradius(gro):
	from numpy import array as arr
	from numpy import linalg as LA
	fullcoords=arr(get_full_coords_nm(gro))
	mindist=fullcoords[0]
	maxdist=fullcoords[1]
	for element in fullcoords:
		for i in range(0,3):
			if float(mindist[i])>float(element[i]):
				mindist[i]=element[i]
			if float(maxdist[i])<float(element[i]):
				maxdist[i]=element[i]
	maxcoords=arr(maxdist)-arr(mindist)
	return LA.norm(maxcoords)

def update_gro_box(gro,groname,nbradius,logfile):
	import re
	with open(groname,"w") as ofile:
		with open(gro) as ifile:
			logger(logfile,str("Finding a larger .gro box size to avoid problems with .mdp input..."))
			for line in ifile:
				ofile.write(line)
                                match=re.search(r'^BOX\s*\n', line,flags=re.MULTILINE)
                                if match:
                                    for line in ifile:
                                        match=re.search(r'^\s*(\d*\.\d+)\s+(\d*\.\d+)\s+(\d*\.\d+)', line,flags=re.MULTILINE)
                                        if not match:
                                            logger(logfile,"\n\nError: In " + str(gro) + " box vectors were expected but not found. Exiting. Line was:\n")
                                            logger(logfile,line)
                                            exit(1)
                                        else:
    					    bv=[float(match.group(1))+10.*nbradius,float(match.group(2))+10.*nbradius,float(match.group(3))+10.*nbradius]
					    ofile.write(" {:>15.9f} {:>15.9f} {:>15.9f}\nEND\n".format(float(bv[0]),float(bv[1]),float(bv[2])))
                                        break
                                    break
	logger(logfile,str("done.\n"))

def make_gmx_inp(jobname,gro,qmmmtop,qmatomlist,curr_step,logfile,basedir,realprefix):
	from subprocess import call
	insert=""
	if int(curr_step)!=0:
		insert=str("." + str(int(curr_step)))
	mdpname=str(jobname +".mdp")
	groname=str(jobname + ".boxlarge.g96")
	ndxname=str(qmmmtop + ".ndx")
	#ndx2name=str(jobname+".m1.ndx")
	#totalndx=str(jobname+".ndx")
#	with open(totalndx,"w") as ofile:
#		with open(ndxname) as ifile:
#			for line in ifile:
#				ofile.write(str(line)+"\n")
#		with open(ndx2name) as ifile:
#			for line in ifile:
#				ofile.write(str(line)+"\n")
	tprname=str(jobname + insert +".tpr")
	nbradius=get_nbradius(gro)
	write_mdp(mdpname,nbradius)
	update_gro_box(gro,groname,nbradius,logfile)
	call([realprefix, "grompp", "-p", str(qmmmtop), "-c", str(groname), "-n", str(ndxname), "-f", str(mdpname), "-o", str(tprname), "-backup", "no"])
	call(["rm", "mdout.mdp"])
	#call(["grompp", "-p", str(qmmmtop), "-c", str(groname), "-f", str(mdpname), "-o", str(tprname)])
	return tprname

def make_g16_inp(jobname,gro,qmmmtop,qmatomlist,qminfo,qmmminfo,pcffile,curr_step,linkatoms,logfile,nmaflag):
	import re
	from numpy import array as arr
	insert=""
	oldinsert=""
	if int(curr_step)!=0:
		insert=str("." + str(int(curr_step)))
		if int(curr_step)>1:
			oldinsert=str("." + str(int(curr_step)-1))
	gaufile=str(jobname+insert+".gjf")
	chkfile=str(jobname+insert+".chk")
	oldchkfile=str(jobname+oldinsert+".chk")
	if nmaflag==1:
		oldchkfile=str(qmmminfo[0]+".chk")
	with open(gaufile,"w") as ofile:
		fullcoords=get_full_coords_angstrom(gro)
		atoms=get_atoms(qmmmtop,logfile)
		ofile.write("%NPROCSHARED="+str(qminfo[5])+"\n")
		ofile.write("%MEM="+str(qminfo[6])+"MB\n")
		ofile.write("%CHK="+chkfile+"\n")
		if int(curr_step)!=0 or nmaflag==1:
			ofile.write("%OLDCHK="+oldchkfile+"\n")
		ofile.write("#P "+str(qminfo[1]))
		if str(qminfo[2])!="NONE":
			ofile.write("/"+str(qminfo[2]))
		if str(qminfo[7])!="NONE":
			ofile.write(" "+str(qminfo[7]))
		if int(curr_step)!=0 or nmaflag==1:
			ofile.write(" guess=read")
		ofile.write(" nosymm gfinput gfprint force charge punch=derivatives iop(3/33=1) prop(field,read) pop=esp\n")
		ofile.write("\nQMMM Calc QM part\n\n"+str(int(qminfo[3])) + " " +str(int(qminfo[4]))+"\n")
		count=0
		for element in fullcoords:
			if int(count+1) in arr(qmatomlist).astype(int):
				ofile.write("{:<2s} {:>12.6f} {:>12.6f} {:>12.6f}\n".format(str(atoms[count]),float(element[0]),float(element[1]),float(element[2])))
			count+=1
		for element in linkatoms:
			#links are already in angstrom
			ofile.write("{:<2s} {:>12.6f} {:>12.6f} {:>12.6f}\n".format(str("H"),float(element[0]),float(element[1]),float(element[2])))
		ofile.write("\n")
		with open(pcffile) as ifile:
			for line in ifile:
				match=re.search(r'^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line,flags=re.MULTILINE)
				if match:
					ofile.write("{:>12.6f} {:>12.6f} {:>12.6f} {:>12.6f}\n".format(float(match.group(1)),float(match.group(2)),float(match.group(3)),float(match.group(4))))
		ofile.write("\n")
		with open(pcffile) as ifile:
			for line in ifile:
				match=re.search(r'^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line,flags=re.MULTILINE)
				if match:
					ofile.write("{:>12.6f} {:>12.6f} {:>12.6f}\n".format(float(match.group(1)),float(match.group(2)),float(match.group(3))))
		ofile.write("\n\n")
	return gaufile

def get_qmforces_au(qmatomlist,m1list,qmmmtop,qminfo,jobname,curr_step,logfile):
	import re
	from numpy import array as arr
	qmforces=[]
	qmonlyforcelist=[]
	pcf_grad=[]
	if (qminfo[0]=="G16"):
		insert=""
		if int(curr_step)!=0:
			insert=str("." + str(curr_step))
		qmlogfile=str(jobname + insert + ".gjf.log")
		fortfile=str(jobname + insert + ".fort.7")
		with open(fortfile) as ifile:
			for line in ifile:
				match=re.search(r'^\s*(\S*)\s*(\S*)\s*(\S*)', line,flags=re.MULTILINE)
				if match:
					qmline=[float(str(match.group(1)).replace("D","e"))*-1.,float(str(match.group(2)).replace("D","e"))*-1.,float(str(match.group(3)).replace("D","e"))*-1.]
					qmonlyforcelist.append(qmline)
		with open(qmlogfile) as i2file:
			for line in i2file:
				match=re.search(r'^\s*Electrostatic\s*Properties\s*\(Atomic\s*Units\)', line,flags=re.MULTILINE)
				if match:
					for line in i2file:
						match=re.search(r'^\s*\S+\s*[-]*\d+\.\d+\s*([-]*\d+\.\d+)\s*([-]*\d+\.\d+)\s*([-]*\d+\.\d+)', line,flags=re.MULTILINE)
						if match:
							pcf_grad_line=[float(match.group(1)),float(match.group(2)),float(match.group(3))]
							pcf_grad.append(pcf_grad_line)
						match=re.search(r'^\s*Leave Link', line,flags=re.MULTILINE)
						if match:
							break
					break
	with open(qmmmtop) as ifile:
		for line in ifile:
			match=re.search(r'\[\s+moleculetype\s*\]', line)
			if match:
				for line in ifile:
					match=re.search(r'\[\s+atoms\s*\]', line)
					if match:
						count=0
						qmcount=0
						m1count=0
						for line in ifile:
							match=re.search(r'^\s*(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+([-]*\d+\.*\d*)\s+(\d+\.*\d*)', line,flags=re.MULTILINE)
							if match and (int(match.group(1)) not in arr(qmatomlist).astype(int)) and (int(match.group(1)) not in arr(m1list).astype(int)):
								curr_charge=float(match.group(7))
								qmforces.append([pcf_grad[count][0]*curr_charge,pcf_grad[count][1]*curr_charge,pcf_grad[count][2]*curr_charge])
								count+=1
							elif match and int(match.group(1)) in arr(qmatomlist).astype(int):
								qmforces.append(qmonlyforcelist[qmcount])
								qmcount+=1
							elif match and int(match.group(1)) in arr(m1list).astype(int):
								qmforces.append(qmonlyforcelist[m1count+len(qmatomlist)])
								m1count+=1
							match=re.search(r'^\s*\n', line,flags=re.MULTILINE)
							if match:
								break
						break
				break
	#logger(logfile,str("\nQM FORCE:"+str(qmforces[106][0])+" "+str(qmforces[106][1])+" "+str(qmforces[106][2])+" "+"\n"))
	return qmforces

def get_mmforces_au(jobname,curr_step,logfile):
	import re
	from subprocess import Popen, PIPE, STDOUT#, call
	prefix="/usr/bin/"
	realprefix=prefix+"gmx"
	mmforces=[]
	insert=""
	if int(curr_step)!=0:
		insert=str("." + str(curr_step))
	trrname=str(jobname + insert + ".trr")
	tprname=str(jobname + insert + ".tpr")
	xvgname=str(jobname + insert + ".xvg")
	p = Popen([realprefix, "traj", "-fp" , "-f", trrname, "-s", tprname, "-of", xvgname, "-xvg", "none", "-backup", "no"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	p.communicate(input=b'0\n')
	with open(xvgname) as ifile:
		for line in ifile:
			forcelist=re.findall('\S+', line)
			count=0
			mmforceline=[]
			for i in range(1,len(forcelist)):
				mmforceline.append(float(forcelist[i])*2.0155295e-05)
				count+=1
				if count>2:
					count=0
					mmforces.append(mmforceline)
					mmforceline=[]
			break#read only one line
	#logger(logfile,str("\nMM FORCE:"+str(mmforces[106][0])+" "+str(mmforces[106][1])+" "+str(mmforces[106][2])+" "+"\n"))
	return mmforces

def get_linkforces_au(linkcorrlist,qmatomlist,xyzq,pcffile,qm_corrdata,m1list,m2list,q1list,linkatoms,logfile,basedir):
	from compiler.ast import flatten
	from numpy import array as arr
	from numpy import linalg as LA
	import imp
	rot = imp.load_source("operations", str(basedir+"/operations/expansion_check.py"))
	linkforces=[]
	#Force Coulomb: z1*z2*(distance along coord)/(distance between charges)**3
	for element in xyzq:#this is just to count an entry for each atom!
		linkforces.append([0.0,0.0,0.0])
	m2charges=get_m2charges(xyzq,m1list,m2list)
	for element in linkcorrlist:
		z1=0.0
		v1=[]
		v2=[]
		if int(element[0]) in flatten(m2list):
			for i in range(0,len(m2list)):
				for j in range(0,len(m2list[i])):
					if int(m2list[i][j])==int(element[0]):
						z1=float(m2charges[i][j])
						v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
						break
				if z1!=0.0:
					break
		elif int(element[0]) in arr(qmatomlist).astype(int):
			for i in range(0,len(qmatomlist)):
				if int(qmatomlist[i])==int(element[0]):
					z1=float(qm_corrdata[i][2])
					v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
					break
		elif int(element[0]) in arr(m1list).astype(int):
			for i in range(0,len(m1list)):
				if int(m1list[i])==int(element[0]):
					z1=float(qm_corrdata[i+len(qmatomlist)][2])
					v1=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
					break
		else:
			z1=float(xyzq[int(element[0])-1][3])
			v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
		z2=0.0
		if int(element[1]) in flatten(m2list):
			for i in range(0,len(m2list)):
				for j in range(0,len(m2list[i])):
					if int(m2list[i][j])==int(element[1]):
						z2=float(m2charges[i][j])
						v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
						break
				if z2!=0.0:
					break
		elif int(element[1]) in arr(qmatomlist).astype(int):
			for i in range(0,len(qmatomlist)):
				if int(qmatomlist[i])==int(element[1]):
					z2=float(qm_corrdata[i][2])
					v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
					break
		elif int(element[1]) in arr(m1list).astype(int):
			for i in range(0,len(m1list)):
				if int(m1list[i])==int(element[1]):
					z2=float(qm_corrdata[i+len(qmatomlist)][2])
					v2=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
					break
		else:
			z2=float(xyzq[int(element[1])-1][3])
			v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
		v12=arr(v1)-arr(v2)
		dist=LA.norm(v12)
		#print str(z1*z2/dist)
		for i in range(0,3):
			linkforces[int(element[0])-1][i]+=z1*z2*v12[i]/(dist*dist*dist)
			linkforces[int(element[1])-1][i]-=z1*z2*v12[i]/(dist*dist*dist)
	#logger(logfile,str("\n"+str(linkforces[1974][0])+" "+str(linkforces[1974][1])+" "+str(linkforces[1974][2])+" "+"\n"))
	#now also all atoms in the corrdata list with the mod and linkcorr point charges
	#mod first. mod is charge in pcffile minus m2charge
	#logger(logfile,str("\nLINK FORCE PRE MOD PRE SHIFT:"+str(linkforces[106][0])+" "+str(linkforces[106][1])+" "+str(linkforces[106][2])+" "+"\n"))
	pcf=read_pcffile(pcffile)
	for i in range(0,len(m2list)):
		for j in range(0,len(m2list[i])):
			curr_mod=[]
			for k in range(0,3):
				curr_mod.append(float(pcf[int(m2list[i][j])-1][k])/0.52917721)
			curr_mod_charge=float(float(pcf[int(m2list[i][j])-1][3]))-m2charges[i][j]
			for k in range(0,len(qmatomlist)):
				v1=[xyzq[int(qmatomlist[k])-1][0]/0.52917721,xyzq[int(qmatomlist[k])-1][1]/0.52917721,xyzq[int(qmatomlist[k])-1][2]/0.52917721]
				z1=float(qm_corrdata[k][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				for l in range(0,3):
					linkforces[int(qmatomlist[k])-1][l]+=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
					linkforces[int(m2list[i][j])-1][l]-=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
			for k in range(0,len(linkatoms)):
				v1=[linkatoms[k][0]/0.52917721,linkatoms[k][1]/0.52917721,linkatoms[k][2]/0.52917721]
				z1=float(qm_corrdata[k+len(qmatomlist)][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
#				if k==0:
#					logger(logfile,str("\n"+str(curr_mod_charge)+" "+str(z1)+" "+str(dist)+"\n"))
				for l in range(0,3):
					linkforces[int(m1list[k])-1][l]+=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
					linkforces[int(m2list[i][j])-1][l]-=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
	#logger(logfile,str("\nLINK FORCE AFTER MOD PRE SHIFT:"+str(linkforces[106][0])+" "+str(linkforces[106][1])+" "+str(linkforces[106][2])+" "+"\n"))
	m2count=0
	linkstart=len(pcf)-2*len(flatten(m2list))
	for i in range(0,len(m2list)):
		for j in range(0,len(m2list[i])*2):
			curr_mod=[]
			for k in range(0,3):
				curr_mod.append(float(pcf[int(linkstart)+m2count][k])/0.52917721)
			curr_mod_charge=float(float(pcf[int(linkstart)+m2count][3]))
			m2count+=1
			for k in range(0,len(qmatomlist)):
				v1=[xyzq[int(qmatomlist[k])-1][0]/0.52917721,xyzq[int(qmatomlist[k])-1][1]/0.52917721,xyzq[int(qmatomlist[k])-1][2]/0.52917721]
				z1=float(qm_corrdata[k][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				for l in range(0,3):
					linkforces[int(qmatomlist[k])-1][l]+=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
#				if int(qmatomlist[k])==1973:
#					logger(logfile,str("\nLINK FORCES CHANGE:"+str(linkforces[1973][0])+" "+str(linkforces[1973][1])+" "+str(linkforces[1973][2])+" "+"\n"))
			for k in range(0,len(linkatoms)):
				v1=[linkatoms[k][0]/0.52917721,linkatoms[k][1]/0.52917721,linkatoms[k][2]/0.52917721]
				z1=float(qm_corrdata[k+len(qmatomlist)][2])
#				if k==0:
#					logger(logfile,str("\n"+str(curr_mod_charge)+" "+str(z1)+" "+str(dist)+"\n"))
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				for l in range(0,3):
					linkforces[int(m1list[k])-1][l]+=z1*curr_mod_charge*v12[l]/(dist*dist*dist)
	#logger(logfile,str("\nLINK FORCE AFTER MOD AFTER SHIFT (PRE RESCALE):"+str(linkforces[106][0])+" "+str(linkforces[106][1])+" "+str(linkforces[106][2])+" "+"\n"))
	for i in range(0,len(linkatoms)):
		v1=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
		v2=[xyzq[int(flatten(q1list)[i])-1][0]/0.52917721,xyzq[int(flatten(q1list)[i])-1][1]/0.52917721,xyzq[int(flatten(q1list)[i])-1][2]/0.52917721]
		v12=arr(v2)-arr(v1)
		dist=LA.norm(v12)/0.71290813568205
		u_v12=rot.uvec(v12)
		forcecorr_q1=float(-0.121651604903312*dist*dist*dist+1.14556934991042*dist*dist-3.56253304170678*dist+3.65070551432821)
		forcecorr_link=float(0.127346797162536*dist*dist*dist-1.21401609958205*dist*dist+3.84474060507329*dist-4.04529918786635)
		q1corrvec=[]
		linkcorrvec=[]
		for j in range(0,3):
			q1corrvec.append(u_v12[j]*forcecorr_q1)
			linkcorrvec.append(u_v12[j]*forcecorr_link)
		#must have their sign reverted as we subtract these forces, but they are defined as additively correcting
		for j in range(0,3):
			linkforces[int(flatten(q1list)[i])-1][j]+=q1corrvec[j]
			linkforces[int(m1list[i])-1][j]+=linkcorrvec[j]
	#logger(logfile,str("\nLINK FORCE FULL:"+str(linkforces[106][0])+" "+str(linkforces[106][1])+" "+str(linkforces[106][2])+" "+"\n"))
	return linkforces

def make_clean_force(total_force):
	from numpy import array as arr
	clean_force=[]
	for element in arr(total_force):
		forceline=[]
		for entry in arr(element):
			forceline.append(float(entry))
		clean_force.append(forceline)
	return clean_force

def make_new_g96(propagator,total_force,last_forces,gro,new_gro,initstep,logfile):
	from compiler.ast import flatten
	from numpy import array as arr
	import re
	dispvec=[]
	maxforce=0.0
	clean_force=make_clean_force(total_force)
	old_clean_force=make_clean_force(last_forces)
	maxatom=-1
	maxcoord=-1
	check_force=flatten(clean_force)
	for i in range(0,len(check_force)/3):
		for j in range(0,3):
			if abs(float(check_force[i*3+j]))>abs(maxforce):
				maxforce=float(check_force[i*3+j])
				maxatom=i
				maxcoord=j
	logger(logfile,str("Maximum force is " + str(float(maxforce)) + " a.u. at coord " + str(int(maxatom)+1) + "/" + str(int(maxcoord)+1) + ".\n"))
	if propagator=="STEEP" or (propagator=="CONJGRAD" and len(last_forces)==0):
		for element in clean_force:
			dispvec.append([float(element[0])*float(initstep)/abs(float(maxforce)),float(element[1])*float(initstep)/abs(float(maxforce)),float(element[2])*float(initstep)/abs(float(maxforce))])
	elif propagator=="CONJGRAD" and len(last_forces)!=0:
		#Fletcher-Reeves
		corr_fac=arr(flatten(clean_force)).dot(arr(flatten(clean_force)))
		corr_fac/=arr(flatten(old_clean_force)).dot(arr(flatten(old_clean_force)))
		counter=0
		for element in clean_force:
			dispvec.append([(float(element[0])-corr_fac*old_clean_force[counter][0])*float(initstep)/abs(float(maxforce)),(float(element[1])-corr_fac*old_clean_force[counter][1])*float(initstep)/abs(float(maxforce)),(float(element[2])-corr_fac*old_clean_force[counter][2])*float(initstep)/abs(float(maxforce))])
			counter+=1
		logger(logfile,str("Effective step at maximum force coord is " + str(float(dispvec[maxatom][maxcoord])) + " a.u.\n"))
	with open(new_gro,"w") as ofile:
		with open(gro) as ifile:
                        counter=0
			for line in ifile:
				ofile.write(line)
                                counter+=1
                                if counter==4:
                                    break
			counter=0
			for line in ifile:
				match=re.search(r'^(.{5})\s(.{5})\s(.{5})\s(.{6})\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)\s*([-]*\d+\.*\d*)', line,flags=re.MULTILINE)
				if not match:
					ofile.write(line)
                                        logger(logfile,str("Successfully wrote " +  str(int(counter)) + " atoms to new g96 file.\n"))
                                        break
				else:
					dispx=dispvec[counter][0]*0.052917721
					dispy=dispvec[counter][1]*0.052917721
					dispz=dispvec[counter][2]*0.052917721
					ofile.write(str(match.group(1))+" "+str(match.group(2))+" "+str(match.group(3))+" "+str(match.group(4))+" {:>15.9f} {:>15.9f} {:>15.9f}\n".format(float(match.group(5))+float(dispx),float(match.group(6))+float(dispy),float(match.group(7))+float(dispz)))
					counter+=1
			for line in ifile:
				ofile.write(line)

def remove_inactive(total_force,active):
	from numpy import array as arr
	new_total_force=[]
	for i in range(0,len(total_force)):
		if (i+1) in arr(active).astype(int):
			new_total_force.append(total_force[i])
		else:
			new_total_force.append([0.0,0.0,0.0])
	return new_total_force

def qmmm_prep(new_gro,top,jobname,curr_step,qminfo,qmatomlist,connlist,linkatoms,basedir,logfile):
	import imp
	import os.path
	make_pcf = imp.load_source("operations", str(basedir+"/pointcharges/generate_pcf_from_top.py"))
	prep_pcf = imp.load_source("operations", str(basedir+"/pointcharges/prepare_pcf_for_shift.py"))
	final_pcf = imp.load_source("operations", str(basedir+"/pointcharges/generate_charge_shift.py"))
	make_gmx2qmmm = imp.load_source("operations", str(basedir+"/gmx2qmmm.py"))
	geo=make_pcf.readg96(new_gro)
	logger(logfile,"List of molecules...")
	mollist=make_pcf.readmols(top)
	logger(logfile,"done.\n")
	logger(logfile,"Reading charges...")
	chargevec=[]
	for element in mollist:
	    chargevec.extend(make_pcf.readcharges(element,top))
	logger(logfile,"done.\n")
	new_xyzq=make_gmx2qmmm.make_xyzq(geo,chargevec)
	logger(logfile,str("Made new xyzq matrix.\n"))
	logger(logfile,"Preparing the point charge field for a numerically optimized charge shift...")
	qmcoordlist,m1list,m2list,updated_chargelist=prep_pcf.prepare_pcf_for_shift_fieldsonly(new_xyzq,qmatomlist,qminfo[3],connlist)
	logger(logfile,"done.\n")
	new_links=make_gmx2qmmm.get_linkatoms_ang(new_xyzq,qmatomlist,m1list,connlist,linkatoms)
	logger(logfile,str("Updated positions of link atoms.\n"))
	filename=jobname
	if curr_step!=0:
		filename+="." + str(int(curr_step))
	if not os.path.isfile(str(filename+".pointcharges")):
		logger(logfile,"Shifting...")
		final_pcf.generate_charge_shift_fieldsonly(updated_chargelist,m1list,qmcoordlist,m2list,filename,basedir)
		logger(logfile,str("Made new PCF file.\n"))
	else:
		logger(logfile,"NOTE: Shifting omitted due to " + str(filename+".pointcharges") + " being an existing file!\n")
	logger(logfile,"done.\n")
	return new_xyzq,m1list,m2list,new_links

def make_opt_step(jobname,xyzq,connlist,propagator,gro,top,total_force,initstep,qmatomlist,qm_corrdata,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,curr_step,last_energy,last_forces,logfile,basedir):
        from numpy import array as arr
	new_gro=str(jobname + "." + str(int(curr_step)+1) + ".g96")
	new_pcffile=str(jobname + "." + str(int(curr_step)+1) + ".pointcharges")
	new_xyzq=[]
	new_links=[]
	new_qm_corrdata=qm_corrdata
	qmenergy=0.0
	mmenergy=0.0
	higher_energy=True
	while higher_energy and float(initstep)>=0.000001:
		if propagator=="STEEP":
			logger(logfile,str("Making a steepest descent step with a maximum step step of " + str(initstep) + " a.u.\n"))
		if propagator=="CONJGRAD":
			logger(logfile,str("Making a conjugate gradient step with a maximum step step of " + str(initstep) + " a.u.\n"))
		higher_energy=False
		make_new_g96(propagator,total_force,last_forces,gro,new_gro,initstep,logfile)
		logger(logfile,str("Made new coordinates in file " + str(new_gro) + ".\n"))
		new_xyzq,m1list,m2list,new_links=qmmm_prep(new_gro,top,jobname,int(curr_step)+1,qminfo,qmatomlist,connlist,linkatoms,basedir,logfile)
		qmenergy,mmenergy,new_qm_corrdata=get_energy(new_gro,qmmminfo[0],new_xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,new_pcffile,new_links,int(curr_step)+1,logfile,basedir)
		curr_energy=float(qmenergy)+float(mmenergy)
		if float(curr_energy)>float(last_energy):
			logger(logfile,str("Rejected one optimization step due to energy increasing. Trying again, with smaller step.\n"))
			from subprocess import call
			insert=""
			if int(curr_step)+1!=0:#this should always happen, but for the sake of safety
				insert=str("." + str(int(curr_step)+1))
			trrname=str(jobname + insert + ".trr")
			tprname=str(jobname + insert + ".tpr")
			gmxlogname=str(jobname + insert + ".gmx.log")
			edrname=str(jobname + insert + ".edr")
			xvgname=str(jobname + insert + ".edr.xvg")
			g16name=str(jobname + insert + ".gjf.log")
			fortname=str(jobname + insert + ".fort.7")
			call(["rm", trrname, tprname, gmxlogname, edrname, xvgname, g16name, fortname])
			higher_energy=True
			initstep*=0.2
		else:
			initstep*=1.2
	return qmenergy,mmenergy,new_qm_corrdata,new_gro,new_pcffile,new_xyzq,new_links,initstep

def opt_cycle(gro,top,xyzq,connlist,qmatomlist,qm_corrdata,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,curr_step,last_energy,last_forces,initstep,active,logfile,basedir):
	import math
	from numpy import array as arr
	from compiler.ast import flatten
	done=0
	f_thresh=float(qmmminfo[2])
	jobname=str(qmmminfo[0])
	total_force=read_forces(qmatomlist,m1list,qmmmtop,qminfo,qmmminfo[0],curr_step,logfile,linkcorrlist,xyzq,pcffile,qm_corrdata,m2list,q1list,linkatoms,active,basedir)
	clean_force=make_clean_force(total_force)
	maxforce=0.0
	for element in flatten(clean_force):
		if abs(float(element))>abs(maxforce):
			maxforce=float(element)
	if abs(maxforce)<float(f_thresh):
		logger(logfile,str("Max force " + str(maxforce) + " below threshold ("+ str(f_thresh) +"). Finishing.\n"))
		done=1
		return done, last_energy, gro, pcffile, xyzq, linkatoms, initstep, qm_corrdata, clean_force
	else:
		logger(logfile,str("Max force not below threshold. Continuing.\n"))
	qmenergy,mmenergy,new_qm_corrdata,new_gro,new_pcffile,new_xyzq,new_links,new_initstep=make_opt_step(jobname,xyzq,connlist,qmmminfo[5],gro,top,total_force,initstep,qmatomlist,qm_corrdata,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,curr_step,last_energy,last_forces,logfile,basedir)
	curr_energy=float(qmenergy)+float(mmenergy)
	if float(new_initstep)<0.000001:
		done=2
		logger(logfile,str("Step became lower than 0.000001 a.u., optimization is considered done for now. This is the best we can do unless reaching unacceptable numerical noise levels.\n"))
	if float(curr_energy)>float(last_energy):
		done=1
		logger(logfile,str("Energy did not drop! Exiting optimizer, this might indicate an error!\n"))
	return done, curr_energy, new_gro, new_pcffile, new_xyzq, new_links, new_initstep, new_qm_corrdata, clean_force

def g96_to_gro(inp,out,logfile):
	import re
	with open(out,"w") as ofile:
		n_a=0
		with open(inp) as ifile:
			for line in ifile:
				match=re.search(r'^POSITION', line,flags=re.MULTILINE)
				if match:
					for line in ifile:
						match=re.search(r'^END', line,flags=re.MULTILINE)
						if match:
							break
						n_a+=1
					break
		ofile.write("GRoups of Organic Molecules in ACtion for Science\n")
		if n_a>99999:
			ofile.write(str(n_a)+"\n")
		else:
			ofile.write("{:>5d}\n".format(n_a))
		with open(inp) as ifile:
			for line in ifile:
				match=re.search(r'^POSITION', line,flags=re.MULTILINE)
				if match:
					for line in ifile:
						match=re.search(r'^\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)', line,flags=re.MULTILINE)
						if match:
							resid=int(match.group(1))
							atomid=int(match.group(4))
							while resid>99999:
								resid-=100000
							while atomid>99999:
								atomid-=100000
							ofile.write("{:>5d}{:<5}{:>5}{:>5d}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(resid,match.group(2),match.group(3),atomid,float(match.group(5)),float(match.group(6)),float(match.group(7))))
							continue
						match=re.search(r'^END', line,flags=re.MULTILINE)
						if not match:
							logger(logfile,str("Unexpected entry in .g96 file. Exiting. Last line:\n"))
							logger(logfile,line)
							exit(1)
						else:
							break
				match=re.search(r'^BOX', line,flags=re.MULTILINE)
				if match:
					for line in ifile:
						match=re.search(r'^\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)', line,flags=re.MULTILINE)
						if not match:
							logger(logfile,str("Unexpected entry in .g96 file. Exiting. Last line:\n"))
							logger(logfile,line)
							exit(1)
						else:
							ofile.write("{:>10.5f}{:>10.5f}{:>10.5f}\n".format(float(match.group(1)),float(match.group(2)),float(match.group(3))))
							break
					break

def perform_opt(gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir):
	from subprocess import call
	import os.path
	count=qmmminfo[7]
	qmenergy,mmenergy,qm_corrdata=get_energy(gro,qmmminfo[0],xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,int(count),logfile,basedir)
	last_energy=float(qmenergy)+float(mmenergy)
	done=0
	maxcycle=int(qmmminfo[3])
	initstep=float(qmmminfo[4])
	new_links=linkatoms
	new_pcffile=pcffile
	new_gro=gro
	new_xyzq=xyzq
	new_qm_corrdata=qm_corrdata
	last_forces=[]
	while not done and count<=maxcycle:
		logger(logfile,str("-----Optimization cycle "+str(int(count)+1)+"-----\n"))
		jobname=qmmminfo[0]
		if count>0:
			jobname+="."+str(int(count))
		archivename=str(jobname)+".tar.gz"
		if os.path.isfile(archivename):
			call(["tar","-xf",archivename])
			call(["rm",archivename])
		archive=["tar","-cf",str(jobname)+".tar"]
		files=[new_pcffile,str(jobname)+".edr",str(jobname)+".edr.xvg",str(jobname)+".trr",str(jobname)+".xvg",str(jobname)+".gmx.log",str(jobname)+".g96",str(jobname)+".gjf",str(jobname)+".mdp",str(jobname)+".boxlarge.g96",str(jobname)+".tpr",str(jobname)+".gjf.log",str(jobname)+".fort.7"]
		done,last_energy,new_gro,new_pcffile,new_xyzq,new_links,initstep,new_qm_corrdata,last_forces=opt_cycle(new_gro,top,new_xyzq,connlist,qmatomlist,new_qm_corrdata,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,new_pcffile,new_links,count,last_energy,last_forces,initstep,active,logfile,basedir)
		archive.extend(files)
		call(archive)
		call(["gzip", str(jobname)+".tar"])
		delete=["rm"]
		delete.extend(files)
		call(delete)
		count+=1
	if done==0:
		logger(logfile,"Optimization canceled due to step limit.\n")
	elif done==1:
		logger(logfile,"Optimization finished due to energy threshold.\n")
	elif done==2:
		logger(logfile,"Optimization finished due to step size.\n")
	g96_to_gro(str(qmmminfo[0]+"."+str(count)+".g96"),str(qmmminfo[0]+".opt.gro"),logfile)
	logger(logfile,"Final geometry written to " + str(qmmminfo[0])+".opt.gro.\n")

def read_pcf_self(qmfile):
	import re
	pcf_self=0.0
	with open(qmfile+".log") as ifile:
		for line in ifile:
			match=re.search(r'^\s+Self\s+energy\s+of\s+the\s+charges\s+=\s+([-]*\d+\.\d+)\s+a\.u\.', line,flags=re.MULTILINE)
			if match:
				pcf_self=float(match.group(1))
				break
	return pcf_self

def get_qmenergy(qmfile,qmprog,extra_string,pcffile,logfile,basedir):
	import re
	import imp
	#make_gmx2qmmm = imp.load_source("operations", str(basedir+"/gmx2qmmm.py"))
	logger(logfile,"Extracting QM energy.\n")
	qmenergy=0.0
	qm_corrdata=[]
	if str(qmprog)=="G16":
		with open(str(qmfile+".log")) as ifile:
			for line in ifile:
				match=[]
				match2=[]
				match2=re.search(r'\sTD[=(\s]', extra_string.upper(),flags=re.MULTILINE)
				if not match2:
					match2=re.search(r'^TD[=(\s]', extra_string.upper(),flags=re.MULTILINE)
				if not match2:
					match2=re.search(r'\sTD$', extra_string.upper(),flags=re.MULTILINE)
				if not match2:
					match2=re.search(r'^TD$', extra_string.upper(),flags=re.MULTILINE)
				if not match2:
					match=re.search(r'^\s*SCF\s*Done:\s*E\(\S+\)\s*\=\s*([-]*\d+\.\d+)', line,flags=re.MULTILINE)
				else:
					match=re.search(r'^\s*Total\s*Energy,\s*E\(\S+\)\s*\=\s*([-]*\d+\.\d+)', line,flags=re.MULTILINE)
				if match:
					logger(logfile,"Obtaining charge self-interaction...")
					#shifted_charges=make_gmx2qmmm.read_charges_clean(pcffile)
					#shifted_charges_au=make_gmx2qmmm.ang2bohr(shifted_charges)
					#pcf_self_pot=make_gmx2qmmm.get_pcf_self_pot(shifted_charges_au)
					pcf_self_pot=read_pcf_self(qmfile)
					logger(logfile,"done: {:>20.10f} a.u.\n".format(float(pcf_self_pot)))
					#G16 energy needs to be corrected for self potential of PCF
					qmenergy=float(match.group(1))-float(pcf_self_pot)
				match=re.search(r'^\s*ESP\s*charges:', line,flags=re.MULTILINE)
				if match:
					for line in ifile:
						break
					for line in ifile:
						match=re.search(r'^\s*(\d+)\s+(\S+)\s+(\S+)', line,flags=re.MULTILINE)
						if match:
							qm_corrdata.append([int(match.group(1)),match.group(2),float(match.group(3))])
						else:
							break
					break
	logger(logfile,"QM energy is "+ str(float(qmenergy)) + " a.u..\n")
	return qmenergy,qm_corrdata

def get_mmenergy(edrname,realprefix,logfile):
	from subprocess import Popen, PIPE, STDOUT#, call
	import re
	mmenergy=0.0
	logger(logfile,"Extracting MM energy.\n")
	#with open("tmpinput.tmp","w") as ofile:
	#	ofile.write("11\n\n")
	p = Popen([realprefix, "energy", "-f", edrname, "-o", str(edrname+".xvg"), "-backup", "no"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	p.communicate(input=b'11\n\n')
	#call(["gmx_d", "energy", "-f", edrname, "-o", str(edrname+".xvg"), "<", "tmpinput.tmp"])
	#call(["rm", "tmpinput.tmp"])
	with open(str(edrname+".xvg")) as ifile:
		for line in ifile:
			match=re.search(r'^    0.000000\s*([-]*\d+.\d+)\n', line,flags=re.MULTILINE)
			if match:
				mmenergy=float(match.group(1))*0.00038087988
				break
	logger(logfile,"MM energy is "+ str(float(mmenergy)) + " a.u..\n")
	return mmenergy

def get_m2charges(xyzq,m1list,m2list):
	from numpy import array as arr
	m2charges=[]
	count=0
	for element in m1list:
		m2chargeline=[]
		for i in range(0,len(m2list[count])):
			m2chargeline.append(float(xyzq[int(m2list[count][i])-1][3]))
		count+=1
		m2charges.append(m2chargeline)
	return m2charges

def read_pcffile(pcffile):
	import re
	pcf=[]
	with open(pcffile) as ifile:
		for line in ifile:
			match=re.search(r'^QM', line,flags=re.MULTILINE)
			if match:
				pcf.append(["QM"])
				continue
			match=re.search(r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line,flags=re.MULTILINE)
			if match:
				pcf.append([float(match.group(1)),float(match.group(2)),float(match.group(3)),float(match.group(4))])
				continue
			match=re.search(r'^$end', line,flags=re.MULTILINE)
			if match:
				break
	return pcf

def get_linkenergy_au(xyzq,qmatomlist,qm_corrdata,linkcorrlist,m1list,m2list,q1list,qmmmtop,linkatoms,pcffile,logfile):
	import math
	from numpy import array as arr
	from numpy import linalg as LA
	from compiler.ast import flatten
	linkenergy=0.0
	m2charges=get_m2charges(xyzq,m1list,m2list)
	for element in linkcorrlist:
		z1=0.0
		v1=[]
		v2=[]
		if int(element[0]) in arr(flatten(m2list)).astype(int):
			for i in range(0,len(m2list)):
				for j in range(0,len(m2list[i])):
					if int(m2list[i][j])==int(element[0]):
						z1=float(m2charges[i][j])
						v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
						break
				if z1!=0.0:
					break
		elif int(element[0]) in arr(qmatomlist).astype(int):
			for i in range(0,len(qmatomlist)):
				if int(qmatomlist[i])==int(element[0]):
					z1=float(qm_corrdata[i][2])
					v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
					break
		elif int(element[0]) in arr(m1list).astype(int):
			for i in range(0,len(m1list)):
				if int(m1list[i])==int(element[0]):
					z1=float(qm_corrdata[i+len(qmatomlist)][2])
					v1=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
					break
		else:
			z1=float(xyzq[int(element[0])-1][3])
			v1=[xyzq[int(element[0])-1][0]/0.52917721,xyzq[int(element[0])-1][1]/0.52917721,xyzq[int(element[0])-1][2]/0.52917721]
		z2=0.0
		if int(element[1]) in flatten(m2list):
			for i in range(0,len(m2list)):
				for j in range(0,len(m2list[i])):
					if int(m2list[i][j])==int(element[1]):
						z2=float(m2charges[i][j])
						v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
						break
				if z2!=0.0:
					break
		elif int(element[1]) in arr(qmatomlist).astype(int):
			for i in range(0,len(qmatomlist)):
				if int(qmatomlist[i])==int(element[1]):
					z2=float(qm_corrdata[i][2])
					v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
					break
		elif int(element[1]) in arr(m1list).astype(int):
			for i in range(0,len(m1list)):
				if int(m1list[i])==int(element[1]):
					z2=float(qm_corrdata[i+len(qmatomlist)][2])
					v2=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
					break
		else:
			z2=float(xyzq[int(element[1])-1][3])
			v2=[xyzq[int(element[1])-1][0]/0.52917721,xyzq[int(element[1])-1][1]/0.52917721,xyzq[int(element[1])-1][2]/0.52917721]
		v12=arr(v1)-arr(v2)
		dist=LA.norm(v12)
		#print str(z1*z2/dist)
		linkenergy+=z1*z2/dist
	#now also all atoms in the corrdata list with the mod and linkcorr point charges
	#mod first. mod is charge in pcffile minus m2charge
	pcf=read_pcffile(pcffile)
	for i in range(0,len(m2list)):
		for j in range(0,len(m2list[i])):
			curr_mod=[]
			for k in range(0,3):
				curr_mod.append(float(pcf[int(m2list[i][j])-1][k])/0.52917721)
			curr_mod_charge=float(float(pcf[int(m2list[i][j])-1][3]))-m2charges[i][j]
			for k in range(0,len(qmatomlist)):
				v1=[xyzq[int(qmatomlist[k])-1][0]/0.52917721,xyzq[int(qmatomlist[k])-1][1]/0.52917721,xyzq[int(qmatomlist[k])-1][2]/0.52917721]
				z1=float(qm_corrdata[k][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				linkenergy+=z1*curr_mod_charge/dist
			for k in range(0,len(linkatoms)):
				v1=[linkatoms[k][0]/0.52917721,linkatoms[k][1]/0.52917721,linkatoms[k][2]/0.52917721]
				z1=float(qm_corrdata[k+len(qmatomlist)][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				linkenergy+=z1*curr_mod_charge/dist
	#now linkcorr. linkcorr are last m2*2 entries in pcf
	m2count=0
	linkstart=len(pcf)-2*len(flatten(m2list))
	for i in range(0,len(m2list)):
		for j in range(0,len(m2list[i])):
			curr_mod=[]
			for k in range(0,3):
				curr_mod.append(float(pcf[int(linkstart)+m2count][k])/0.52917721)
			curr_mod_charge=float(float(pcf[int(linkstart)+m2count][3]))
			m2count+=1
			for k in range(0,len(qmatomlist)):
				v1=[xyzq[int(qmatomlist[k])-1][0]/0.52917721,xyzq[int(qmatomlist[k])-1][1]/0.52917721,xyzq[int(qmatomlist[k])-1][2]/0.52917721]
				z1=float(qm_corrdata[k][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				linkenergy+=z1*curr_mod_charge/dist
			for k in range(0,len(linkatoms)):
				v1=[linkatoms[k][0]/0.52917721,linkatoms[k][1]/0.52917721,linkatoms[k][2]/0.52917721]
				z1=float(qm_corrdata[k+len(qmatomlist)][2])
				v12=arr(v1)-arr(curr_mod)
				dist=LA.norm(v12)
				linkenergy+=z1*curr_mod_charge/dist
	#now, add the correction of energy for the link atoms. currently only C-C bond cuts supported.
	for i in range(0,len(linkatoms)):
		v1=[linkatoms[i][0]/0.52917721,linkatoms[i][1]/0.52917721,linkatoms[i][2]/0.52917721]
		v2=[xyzq[int(flatten(q1list)[i])-1][0]/0.52917721,xyzq[int(flatten(q1list)[i])-1][1]/0.52917721,xyzq[int(flatten(q1list)[i])-1][2]/0.52917721]
		v12=arr(v2)-arr(v1)
		dist=LA.norm(v12)
		linkenergy+=0.439749962284789*dist*dist*dist*0.52917721*0.52917721*0.52917721-2.23510192333531*dist*dist*0.52917721*0.52917721+3.7473966326933*dist*0.52917721+76.5520216417149 #fitted polynomial from a C-C vs. C-H B3LYP/6-31G* butane C-Link scan
		#sign inverted due to correction convention (subtracting)
	return linkenergy

def get_energy(gro,jobname,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,curr_step,logfile,basedir):
	from subprocess import call
	import os.path
	#prefix="/usr/bin/"
	prefix="/home/janjoswig/local/gromacs-2019.1/bin/"
	#realprefix=prefix+"gmx"
	realprefix=prefix+"gmx19"
	mmenergy=0.0
	qmfile=""
	mmfile=""
	insert=""
	nmaflag=0
	if qmmminfo[1]=="NMA":
		nmaflag=1
	if int(curr_step)!=0:
		insert=str("." + str(int(curr_step)))
	logger(logfile,"Computing a single point.\n")
	logger(logfile,"Preparing QM and MM inputs: ")
	if qminfo[0]=="G16":
		qmfile=make_g16_inp(jobname,gro,qmmmtop,qmatomlist,qminfo,qmmminfo,pcffile,curr_step,linkatoms,logfile,nmaflag)
		logger(logfile,"G16 input ready.\n")
	if qminfo[0]=="TM":
		qmfile=tm_stuff.make_tm_inp(jobname,gro,qmmmtop,qmatomlist,qminfo,qmmminfo,pcffile,curr_step,linkatoms,logfile,nmaflag)
		logger(logfile,"Turbomole input ready.\n")
	mmfile=make_gmx_inp(jobname,gro,qmmmtop,qmatomlist,curr_step,logfile,basedir,realprefix)
	logger(logfile,"Gromacs input ready.\n")
	if qminfo[0]=="G16":
		if not os.path.isfile(str(qmfile)+".log"):
			logger(logfile,"Running G16 file.\n")
			call(["rung16",str(qmfile)])
			call(["mv","fort.7",str(jobname+insert+".fort.7")])
			logger(logfile,"G16 done.\n")
		else:
			logger(logfile,"NOTE: Using existing G16 files, skipping calculation for this step.\n")
		if not os.path.isfile(jobname+insert+".fort.7"):
			if not os.path.isfile("fort.7"):
				logger(logfile,"No fort.7 file was created by the last Gaussian run! Exiting.\n")
				exit(1)
			call(["mv","fort.7",str(jobname+insert+".fort.7")])
			logger(logfile,"WARNING: Had to rename fort.7 file but not the log file. MAKE SURE THAT THE FORT.7 FILE FITS TO THE LOG FILE!\n")
	logger(logfile,"Running Gromacs file.\n")
	trrname=str(jobname + insert + ".trr")
	xtcname=str(jobname + insert + ".xtc")
	outname=str(jobname + insert + ".out.gro")
	gmxlogname=str(jobname + insert + ".gmx.log")
	edrname=str(jobname + insert + ".edr")
	call([realprefix, "mdrun", "-s", mmfile, "-o", trrname, "-c", outname, "-x", xtcname, "-g", gmxlogname, "-e", edrname, "-backup", "no"])
	call(["rm", outname])
	qmenergy,qm_corrdata=get_qmenergy(str(qmfile),qminfo[0],qminfo[7],pcffile,logfile,basedir)
	mmenergy=get_mmenergy(str(edrname),realprefix,logfile)
	linkcorrenergy=get_linkenergy_au(xyzq,qmatomlist,qm_corrdata,linkcorrlist,m1list,m2list,q1list,qmmmtop,linkatoms,pcffile,logfile)
	qmenergy-=linkcorrenergy
	methodstring=str(qminfo[1])
	if qminfo[2]!="NONE":
		methodstring+=str("/" + str(qminfo[2]))
	logger(logfile,str("Single point energy done. QM/MM energy is {:>20.10f} (QM, link atom corrected ".format(float(qmenergy)) + methodstring +") + {:>20.10f} (MM) = {:>20.10f} (a.u.)\n".format(float(mmenergy),float(qmenergy)+float(mmenergy))))
	return qmenergy,mmenergy,qm_corrdata

def read_forces(qmatomlist,m1list,qmmmtop,qminfo,jobname,curr_step,logfile,linkcorrlist,xyzq,pcffile,qm_corrdata,m2list,q1list,linkatoms,active,basedir):
	from numpy import array as arr
	logger(logfile,str("Reading forces.\n"))
	qmforces=[]
	mmforces=[]
	qmforces=get_qmforces_au(qmatomlist,m1list,qmmmtop,qminfo,jobname,curr_step,logfile)
	logger(logfile,str("QM forces read.\n"))
	mmforces=get_mmforces_au(jobname,curr_step,logfile)
	logger(logfile,str("MM forces read.\n"))
	linkcorrforces=get_linkforces_au(linkcorrlist,qmatomlist,xyzq,pcffile,qm_corrdata,m1list,m2list,q1list,linkatoms,logfile,basedir)
	logger(logfile,str("Forces for link atom correction read.\n"))
	total_force=arr(qmforces)+arr(mmforces)-arr(linkcorrforces)
	#logger(logfile,str("\n"+str(total_force[106][0])+" "+str(total_force[106][1])+" "+str(total_force[106][2])+"\n"))
	logger(logfile,str("Total forces obtained.\n"))
	total_force=remove_inactive(total_force,active)
	logger(logfile,str("Deleted forces of inactive atoms.\n"))
	return total_force

def perform_nma(gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir):
	import imp
	from numpy import array as arr
	nma_stuff = imp.load_source("operations", str(basedir+"/operations/nma_stuff.py"))
	write_hess = imp.load_source("operations", str(basedir+"/operations/hes_xyz_g09RevD.01.fchk.py"))
	nma = imp.load_source("operations", str(basedir+"/operations/nma_3N-6dof.py"))
	logger(logfile,"------This will be a numerical) normal mode analysis.------\n")
	logger(logfile,"Generating a numerical Hessian for the active region using a displacement step of " + str(qmmminfo[6]) + " a.u.\n")
	logger(logfile,"Will require "+ str(len(active)*6+1) +" single point calculations!\n")
	qmenergy,mmenergy,qm_corrdata=get_energy(gro,qmmminfo[0],xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,0,logfile,basedir)
	start_energy=float(qmenergy)+float(mmenergy)
	start_forces=read_forces(qmatomlist,m1list,qmmmtop,qminfo,qmmminfo[0],0,logfile,linkcorrlist,xyzq,pcffile,qm_corrdata,m2list,q1list,linkatoms,active,basedir)
	start_grad=arr(start_forces)*-1.0
	hessian_xyz_full=[]
	for curr_atom in active:
		grad_deriv_vec=nma_stuff.get_xyz_2nd_deriv(curr_atom,start_energy,start_grad,gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir)
		hessian_xyz_full.extend(grad_deriv_vec)
	prep_hess=nma_stuff.prepare_hess(hessian_xyz_full,active)
	evals=[]
	for i in range(0,len(prep_hess[0])-6):
		evals.extend([float(1000.0)])
	nma_stuff.write_pseudofchk_file(qmmminfo[0],evals,prep_hess,prep_hess,active,qmmmtop,logfile,xyzq)#using prep_hess as pseudo-nm_matrix since we do not know yet
	logger(logfile,"Wrote pseudofchk (G03 format).\n")
	write_hess.hes_xyz_fchk(str(qmmminfo[0]+".pseudofchk"),str(qmmminfo[0]+".hess"))
	logger(logfile,"Wrote orca format .hess file.\n")
	evals,nm_matrix=nma.nma_3Nminus6dof_asfunction(str(qmmminfo[0]+".hess"),basedir)
	print nma_stuff.log_nma(qmmminfo,logfile,evals,nm_matrix,active,qmmmtop,xyzq,prep_hess)

def perform_job(gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,jobtype,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir,step):
	import imp
	g2q = imp.load_source("operations", str(basedir+"/gmx2qmmm.py"))
	if jobtype=="SINGLEPOINT":
		jobname=g2q.stepper(qmmminfo[0],step)
		get_energy(gro,jobname,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,int(0),logfile,basedir)
	elif jobtype=="OPT":
		logger(logfile,"Performing an optimization.\n")
		logger(logfile,"Getting initial energy:\n")
		perform_opt(gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir)
	elif jobtype=="NMA":
		jobname=g2q.stepper(qmmminfo[0],step)
		perform_nma(gro,top,xyzq,connlist,qmatomlist,m1list,m2list,q1list,qmmmtop,qminfo,mminfo,qmmminfo,linkcorrlist,flaglist,pcffile,linkatoms,active,logfile,basedir)
	else:
		logger(logfile,"Unrecognized jobtype \"" + jobtype + "\". Exiting.\n")

if __name__ == '__main__':
	print "This file serves as a library for gmx2qmmm-related functions."
        print "Do not execute directly. Use gmx2qmmm instead."
