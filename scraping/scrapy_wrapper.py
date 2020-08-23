import os
import argparse


#defaults
start_date = '20180101'
end_date = '20200701'
tag = 'health'
output_dir = 'scraped_data/'
scrapper_file = 'medium_scraper_tag_archive.py'


if os.path.exists(output_file):
    os.remove(output_file)

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-tag', default=tag)
parser.add_argument('-start_date', default=start_date)
parser.add_argument('-end_date', default=end_date)
args = parser.parse_args()

#output files
log_file = 'logs/'+start_date+'_'+args.tag+'_'+end_date+'.log'
output_file = output_dir+start_date+'_'+args.tag+'_'+end_date+'.json'

print('START DATE: '+args.start_date)
print('END DATE: '+args.end_date)
print('TAG: '+args.tag)

os.system('scrapy runspider -a tag={tag} -a start_date={start_date} -a end_date={end_date} --logfile {log_file} {scrapper_file} -o {output_file}'.format(tag=args.tag,start_date=args.start_date,end_date=args.end_date,scrapper_file=scrapper_file,output_file=output_file, log_file = log_file))
