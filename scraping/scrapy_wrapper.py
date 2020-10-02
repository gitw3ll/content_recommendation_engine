import os
import argparse


#defaults
start_date = '20180101'
end_date = '20200701'
clap_limit = '0'
tag = 'health'
output_dir = 'scraped_data/'
scrapper_file = 'medium_archive_article_scraper.py'

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-tag', default=tag,
                    help='Medium tag to search archive.')
parser.add_argument('-start_date', default=start_date,
                    help='Archive search start date. YYYYMMDD')
parser.add_argument('-end_date', default=end_date,
                    help='Archive search end date. YYYYMMDD')
parser.add_argument('-clap_limit', default=clap_limit,
                    help='Only include articles with claps greater than or equal to this number.')
parser.add_argument('--include_body', action='store_true',
                    help='If this argument is included, output will include text body of article. Significantly slows down run time.')
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
print('INCLUDE BODY = {0}'.format(args.include_body))

os.system('scrapy runspider -a tag={tag} -a start_date={start_date} -a end_date={end_date} -a clap_limit={clap_limit} -a include_body={include_body} --logfile {log_file} {scrapper_file} -o {output_file}'.format(tag=args.tag,start_date=args.start_date,end_date=args.end_date,clap_limit=args.clap_limit,include_body=args.include_body,scrapper_file=scrapper_file,output_file=output_file, log_file = log_file))
