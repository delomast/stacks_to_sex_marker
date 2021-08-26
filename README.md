# stacks_to_sex_marker
Scripts for finding candidate sex markers from output files of Stacks pipeline for RAD-seq data

Instructions for use

Note: These scripts have been tested on Linux.

##############
Vcf_sex_markers.py

This script requires a vcf file and a sample list as inputs. The vcf file should be one output by Stacks and the sample 
list follows a similar format to the population map accepted by Stacks. The sample list is a tab delimited file that contains 
sample names in the first column and sex (Male or Female) in the second column. For example:
  <br/>
Sample_1	Female  <br/>
Sample_2	Female  <br/>
Sample_3	Male  <br/>
Sample_4	Male   <br/>

The sample names must match the headers of the vcf output by Stacks, which should be the case as long as the sample names 
are the same as those you used in the population map you input to Stacks.

In the terminal, navigate to the directory where you saved the python script. Then type:  <br/>
  <br/>
	  python Vcf_sex_markers.py file/path/to_your/vcf_file.vcf file/path/to_your/sample_phenotype_list.txt
  <br/>  <br/>
The script will then search for sex marker candidates assuming 1. male heterogamety, and then 2. female heterogamety. 
After completing each search, the script will write a tab delimited file containing the catalog locus number and snp location 
(format: Locusnumber_snplocation) of the candidate markers, the number of females that have genotypes for that marker, the number 
of males that have genotypes for that marker, and the total number of samples with genotypes for that marker. You can then look
 up the consensus sequence in cstacks or populations output based on the catalog locus number. If no candidate markers are found, 
 the file will just contain the header row.

 
################
presence_absence_sex_markers.py

This script requires the cstacks output, sstacks ouput, and a sample list as inputs. The sample list follows a similar format to 
the population map accepted by Stacks. The sample list is a tab delimited file that contains sample names in the first column and
 sex (Male or Female) in the second column. For example:
   <br/>
Sample_1	Female  <br/>
Sample_2	Female  <br/>
Sample_3	Male  <br/>
Sample_4	Male   <br/>
  <br/>
The sample names must match the file names of the sstacks output WITHOUT the .matches.tsv. For example, with the above sample
 names, your sstacks ouput files should be named
  <br/>
Sample_1.matches.tsv  <br/>
Sample_2.matches.tsv  <br/>
Sample_3.matches.tsv  <br/>
Sample_4.matches.tsv  <br/>
  <br/>
In the terminal, navigate to the directory that contains the cstacks and sstacks output and save the python script in this same 
location. Then type:
  <br/>
	  python presence_absence_sex_markers.py file/path/to_your/sample_phenotype_list.txt
  <br/>  <br/>
The script will then search for presence/absence sex marker candidates assuming 1. male heterogamety, and then 2. female heterogamety. 
After completing each search, the script will write a tab delimited file containing the catalog locus number of the candidate markers, and 
the number of samples of the heterogametic sex with genotypes for that marker. You can then look up the consensus sequence in the cstacks 
output based on the catalog locus number. If no candidate markers are found, the file will just contain the header row. 

