#!/usr/bin/env python
import os
from argparse import ArgumentParser
from eggnogmapper.common import EGGNOG_DATABASES, DATA_PATH, HMMDB_PATH, pexists, pjoin
from eggnogmapper.utils import ask, colorify

def run(cmd):
    print colorify(cmd, 'cyan')
    if not args.simulate:
        os.system(cmd)

def download_hmm_database(level):
    if level == 'euk':
        level = 'euk_500'
    elif level == 'bact':
        level = 'euk_50'
    elif level == 'arch':
        level = 'arch_1'
        
    url = 'http://beta-eggnogdb.embl.de/download/eggnog_4.5/eggnog-mapper-data/hmmdb_levels/%s_hmm/' %level
    cmd = 'mkdir -p %s; cd %s; wget -nH --user-agent=Mozilla/5.0 --relative -r --no-parent --reject "index.html*" --cut-dirs=4 -e robots=off %s' %(HMMDB_PATH, HMMDB_PATH, url)
    run(cmd)

def download_annotations():
    url = 'http://beta-eggnogdb.embl.de/download/eggnog_4.5/eggnog-mapper-data/eggnog.db.gz' 
    cmd = 'cd %s && wget -nH --user-agent=Mozilla/5.0 --relative --no-parent --reject "index.html*" --cut-dirs=4 -e robots=off -O eggnog.db.gz %s && gunzip eggnog.db.gz' %(DATA_PATH, url)
    run(cmd)
    
def download_groups():
    url = 'http://beta-eggnogdb.embl.de/download/eggnog_4.5/eggnog-mapper-data/OG_fasta.tar.gz' 
    cmd = 'cd %s && wget -nH --user-agent=Mozilla/5.0 --relative --no-parent --reject "index.html*" --cut-dirs=4 -e robots=off -O OG_fasta.tar.gz  %s && tar -zxf OG_fasta.tar.gz && rm OG_fasta.tar.gz' %(DATA_PATH,  url)
    run(cmd)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('dbs', metavar='dbs', nargs='+', choices=sorted(EGGNOG_DATABASES.keys()+["all"]),
                        help='list of eggNOG HMM databases to download')

    parser.add_argument('-y', action="store_true", dest='allyes',
                        help='assume "yes" to all questions')

    parser.add_argument('-f', action="store_true", dest='force',
                        help='forces download even if the files exist')
    
    parser.add_argument('-s', action="store_true", dest='simulate',
                        help='simulate and print commands. Nothing is downloaded')
    

    args = parser.parse_args()
    if 'all' in args.dbs:
        args.dbs = EGGNOG_DATABASES

        
    if not pexists(pjoin(DATA_PATH, 'eggnog.db')):
        if args.allyes or ask("Download main annotation database?") == 'y':
            download_annotations()

    if not pexists(pjoin(DATA_PATH, 'OG_fasta')):
        if args.allyes or ask("Download OG fasta files for annotation refinement?") == 'y':
            download_groups()
        
    if args.allyes or ask("Download %d databases (%s)?"%(len(args.dbs), ','.join(args.dbs))) == 'y':
        for db in args.dbs:
            print "Downloading", colorify(db, 'yellow')
            download_hmm_database(db)



            
            
