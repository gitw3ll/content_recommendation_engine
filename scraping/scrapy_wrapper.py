import os
import argparse


#defaults
start_date = '20180101'
end_date = '20200701'
clap_limit = '0'
tag = 'health'
output_dir = 'scraped_data/'
scrapper_file = 'medium_scraper_tag_archive.py'

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-tag', default=tag)
parser.add_argument('-start_date', default=start_date)
parser.add_argument('-end_date', default=end_date)
parser.add_argument('-clap_limit', default=clap_limit)
args = parser.parse_args()

#output files
log_file = 'logs/'+args.start_date+'_'+args.tag+'_'+args.end_date+'.log'
output_file = output_dir+args.start_date+'_'+args.tag+'_'+args.end_date+'.json'

if os.path.exists(output_file):
    os.remove(output_file)

print('START DATE: '+args.start_date)
print('END DATE: '+args.end_date)
print('TAG: '+args.tag)
print('>= {0} CLAPS'.format(args.clap_limit))

os.system('scrapy runspider -a tag={tag} -a start_date={start_date} -a end_date={end_date} -a clap_limit={clap_limit} --logfile {log_file} {scrapper_file} -o {output_file}'.format(tag=args.tag,start_date=args.start_date,end_date=args.end_date,clap_limit=args.clap_limit,scrapper_file=scrapper_file,output_file=output_file, log_file = log_file))
