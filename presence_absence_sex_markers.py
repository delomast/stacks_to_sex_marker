#!/usr/bin/python3
#Tom Delomas - 2018
#####For STACKS v1.x or v2.x output files
#read cstacks and sstacks output files to
#get loci that match pattern expected under various sex determination systems
##p_a_candidate_XY - males all homozygous, females all missing (failed to type)
##p_a_candidate_WZ - females all homozygous, males all missing (failed to type)
#########in terminal type: python presence_absence_sex_markers.py file/path/to/sample_phenotypes.txt
###sample phenotypes should be tab delimited file with samplename	phenotype
#######and a different sample on each line
################where samplename is the name of the *.matches.tsv file (sstacks output) 	WITHOUT the .matches.tsv
################and phenotype is either male or female

import glob, sys, re

def Test_loci(het_gamet, hom_gamet, s_col, full_catalog):
	#remove all loci that were found in homo_gamet
	hom_cat = []
	for hom_sample in hom_gamet:	
		print('Now searching through sample: ', hom_sample)
		firstline = True
		hom_file = glob.glob(hom_sample + '.matches.tsv')
		for line in open(hom_file[0], 'r'):
			if firstline:	#skip header line of output file
				firstline = False
				continue
			separated = line.split('\t')
			hom_cat.append(separated[s_col])
	print('Now removing loci present in homogametic samples')
	hom_cat = set(hom_cat)
	full_catalog = [x for x in full_catalog if x not in hom_cat]		#remove any loci found in homogametic sex (only remove one instance b/c cstacks output should only have one instance of each)
	print('all removed')

	#determine how many heterogametic sex have the locus and if they are heterozygous		
	het_dict = {}	#build dict of potential loci - 0 means not found in indiv, 1 means found once (idiv is homozygous), 2 means found twice (indiv is het, and thus marker removed)
	for i in full_catalog:
		het_dict[i] = [0,0]
	to_delete = []
	for het_sample in het_gamet:	
		print('Now searching through sample: ', het_sample)
		firstline = True
		het_file = glob.glob(het_sample + '.matches.tsv')
		for line in open(het_file[0], 'r'):
			if firstline:	#skip header line of output file
				firstline = False
				continue
			separated = line.split('\t')
			if separated[s_col] in het_dict:			
				het_dict[separated[s_col]][0] += 1		# add one to heterozygous indicator
				het_dict[separated[s_col]][1] += 1		# add one to successfully genotyped indicator (will add two for loci that are het, but then they will be removed prior to reporting)
		for i in het_dict:
			if het_dict[i][0] > 1:
				to_delete.append(i)	#if sample is heterozygous, add to list to delete
			het_dict[i][0] = 0		#rezero heterozygous indicator for next sample
	
	print('removing loci with invalid genotypes in the heterogametic sex')
	to_delete = set(to_delete)	#remove repititions
	het_dict = [[x, het_dict[x][1]] for x in het_dict if x not in to_delete]		#remove any loci found in homogametic sex (only remove one instance b/c cstacks output should only have one instance of each)
	return het_dict
	


def Main():
	###identify catalog file
	cat_file = glob.glob('*catalog.tags.tsv')
	if len(cat_file) > 1:
		print('More than one *catalog.tags.tsv ', str(cat_file), ' file found. Assessment of only one catalog at a time is allowed. Exiting.')
		return
	
	#generate lists of male and female file names
	females, males = [], []
	try:
		for line in open(sys.argv[1], 'r'):
			separated = re.split('[\t\n]', line)
			if separated[1].lower() == 'male':
				males.append(separated[0])
			elif separated[1].lower() == 'female':
				females.append(separated[0])
	except:
		print('cannot open supplied sample_list')
		return
	print('Read in ', str(len(males)), ' males and ', str(len(females)), ' females.')
		
	#read in loci in catalog
	catalog = []
	print('reading catalog')
	firstline = True
	for line in open(cat_file[0], 'r'):
			if firstline:	
				V1 = re.search('cstacks version 1', line)
				if V1:					#identify if STACKS v1.x was used based on on header of catalog file
					cstacks = 2		#catalog number is third column in s and c stacks v1 outputs
					sstacks = 2
				else:		#assume Stacks v2 unless find otherwise
					cstacks = 1		#catalog number is second column in cstacks v2 output
					sstacks = 0		#catalog number is first column in sstacks v2 output
				firstline = False
				continue
			separated = line.split('\t')
			catalog.append(separated[cstacks])	#catalog number is in third column of cstacks STACKS v1 output
	
	####assuming XX/XY with only Y specific allele
	print('Searching for presence/absence candidates under XX-XY (male heterogamety)')
	dict_out = Test_loci(males, females, sstacks, catalog)	#find loci matching the male heterogametic pattern
	output_file3 = open('p_a_candidate_XY.txt', 'w')
	output_file3.write('Locus\tNum_male\n')
	#loop through loci
	print('Now writing potential loci')
	#output list
	for i in range(0, len(dict_out), 1):
		if dict_out[i][1] > 0:
			output_file3.write(str(dict_out[i][0]) + '\t' + str(dict_out[i][1]) + '\n')
	output_file3.close()

	dict_out = {}	#zero dict out in to prevent an error causing the same dict_out to be written twice

	##next assuming ZZ/WZ with only W specific allele
	print('Searching for presence/absence candidates under WZ-ZZ (female heterogamety)')
	dict_out = Test_loci(females, males, sstacks, catalog)	#find loci matching the female heterogametic pattern
	
	output_file4 = open('p_a_candidate_WZ.txt', 'w')
	output_file4.write('Locus\tNum_female\n')
	#loop through loci
	print('Now writing potential loci')
	#output list
	for i in range(0, len(dict_out), 1):
		if dict_out[i][1] > 0:
			output_file4.write(str(dict_out[i][0]) + '\t' + str(dict_out[i][1]) + '\n')	
	output_file4.close()
	print('Finished searching for presence/absence candidate markers')
	
Main()
			 	 
			 
			 
			 