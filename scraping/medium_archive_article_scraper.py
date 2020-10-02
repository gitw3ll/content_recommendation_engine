# -*- coding: utf-8 -*-
"""
initially based off https://github.com/AiswaryaSrinivas/Scraping-Medium-and-Data-Analysis/blob/master/medium_scrapper_tag_archive.py

This scrapper extracts data for a given date range for a particular Medium Tag

to run:
`scrapy runspider -a tag={tag} -a start_date={start_date} -a end_date={end_date} -a clap_limit={clap_limit} -a include_body={include_body} --logfile {log_file} medium_archive_article_scraper.py -o {output_file}`

e.g. `scrapy runspider -a tag=wellness -a start_date=20200101 -a end_date=20200601 -a clap_limit=100 -a include_body=False --logfile logs/file.log medium_archive_article_scraper.py -o output.json`
"""

import scrapy
from datetime import datetime
from datetime import timedelta
import os
import re
from scrapy.exporters import JsonItemExporter


class MediumPost(scrapy.Spider):
    name='medium_scrapper'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.17,
    }
    total_articles = 0
    def start_requests(self):

        startDate=datetime.strptime(self.start_date,"%Y%m%d")
        endDate=datetime.strptime(self.end_date,"%Y%m%d")
        delta=endDate-startDate

        base_url = start_url = 'https://medium.com/tag/'+self.tag+'/archive/'
        self.start_urls=[base_url+datetime.strftime(startDate+timedelta(days=i),'%Y/%m/%d') for i in range(delta.days + 1)]
        print(self.start_urls)
        for start_url in self.start_urls:


            yield scrapy.Request(start_url)


    def parse(self,response, parsed_data=None):

        response_data=response.text
        #for literal Evaluation
        true = True
        false = False
        null = None



        if response._url in self.start_urls:
            #turn text into dictionary
            response_data = eval(re.findall('window\["obvInit"\]\((.+)\)', response_data)[0])

            user_data = response_data['references']['User']
            #user_data keywords: ['userId', 'name', 'username', 'createdAt', 'imageId', 'backgroundImageId', 'bio', 'twitterScreenName', 'allowNotes', 'mediumMemberAt', 'isWriterProgramEnrolled', 'isSuspended', 'isMembershipTrialEligible', 'optInToIceland', 'type']

            post_data = response_data['references']['Post']
            #post_data keywords: ['id', 'versionId', 'creatorId', 'homeCollectionId', 'title', 'detectedLanguage', 'latestVersion', 'latestPublishedVersion', 'hasUnpublishedEdits', 'latestRev', 'createdAt', 'updatedAt', 'acceptedAt', 'firstPublishedAt', 'latestPublishedAt', 'vote', 'experimentalCss', 'displayAuthor', 'content', 'virtuals', 'coverless', 'slug', 'translationSourcePostId', 'translationSourceCreatorId', 'isApprovedTranslation', 'inResponseToPostId', 'inResponseToRemovedAt', 'isTitleSynthesized', 'allowResponses', 'importedUrl', 'importedPublishedAt', 'visibility', 'uniqueSlug', 'previewContent', 'license', 'inResponseToMediaResourceId', 'canonicalUrl', 'approvedHomeCollectionId', 'newsletterId', 'webCanonicalUrl', 'mediumUrl', 'migrationId', 'notifyFollowers', 'notifyTwitter', 'notifyFacebook', 'responseHiddenOnParentPostAt', 'isSeries', 'isSubscriptionLocked', 'seriesLastAppendedAt', 'audioVersionDurationSec', 'sequenceId', 'isEligibleForRevenue', 'isBlockedFromHightower', 'deletedAt', 'lockedPostSource', 'hightowerMinimumGuaranteeStartsAt', 'hightowerMinimumGuaranteeEndsAt', 'featureLockRequestAcceptedAt', 'mongerRequestType', 'layerCake', 'socialTitle', 'socialDek', 'editorialPreviewTitle', 'editorialPreviewDek', 'curationEligibleAt', 'isProxyPost', 'proxyPostFaviconUrl', 'proxyPostProviderName', 'proxyPostType', 'isSuspended', 'isLimitedState', 'seoTitle', 'previewContent2', 'cardType', 'isDistributionAlertDismissed', 'isShortform', 'shortformType', 'responsesLocked', 'isLockedResponse', 'type']

            #post_data['virtuals'] keywords: ['allowNotes', 'previewImage', 'wordCount', 'imageCount', 'readingTime', 'subtitle', 'usersBySocialRecommends', 'noIndex', 'recommends', 'isBookmarked', 'tags', 'socialRecommendsCount', 'responsesCreatedCount', 'links', 'isLockedPreviewOnly', 'metaDescription', 'totalClapCount', 'sectionCount', 'readingList', 'topics']

            titles = [post_data[postId]['title'] for postId in post_data]
            reading_times = [post_data[postId]['virtuals']["readingTime"] for postId in post_data]
            responses_count = [post_data[postId]['virtuals']["responsesCreatedCount"] for postId in post_data]
            clap_count = [post_data[postId]['virtuals']["totalClapCount"] for postId in post_data]
            tags = [[tag['slug'] for tag in post_data[postId]['virtuals']["tags"]] for postId in post_data]
            tags_postCounts = [[tag['postCount'] for tag in post_data[postId]['virtuals']["tags"]] for postId in post_data]
            authors = [user_data[post_data[postId]['creatorId']]['username'] for postId in post_data]

            unique_slugs = [post_data[postId]["uniqueSlug"] for postId in post_data]
            urls = ['https://medium.com/@'+author+'/'+slug for author in authors for slug in unique_slugs ]


            # article_urls = re.findall('data-action-value="(https://medium.com/[@\w.]+/.+?)\?source=tag_archive\-+', response_data)
            # article_urls=list(set(article_urls))
            #
            # article_unique_slugs = re.findall('"uniqueSlug":"([\w-]+)"', response_data)
            # article_clap_counts = re.findall('"totalClapCount":([0-9]+)', response_data)
            # article_response_counts = re.findall('"responsesCreatedCount":([0-9]+)', response_data)
            # # article_social_recommends_count = re.findall('"socialRecommendsCount":([0-9]+)', response_data) #not sure if this is ever non-zero
            date = response._url[-10:].replace('/','')

            n_articles_to_add = sum([1 for clap in clap_count if clap >=int(self.clap_limit)])
            self.total_articles +=n_articles_to_add
            print('***** {0} articles on {1}, {2} total articles so far ****'.format(n_articles_to_add, date, self.total_articles))


            for i in range(len(titles)):
                parsed_data = {"date":date,
                            "title": titles[i],
                            "author":authors[i],
                            "claps":clap_count[i],
                            "length":reading_times[i],
                            "tags": tags[i],
                            "tags_postCounts": tags_postCounts[i],
                            "responses_count": responses_count[i],
                            "url": urls[i]}

                if int(clap_count[i])>=int(self.clap_limit):
                    if eval(self.include_body):
                        yield scrapy.Request(urls[i],callback=self.parse, cb_kwargs={'parsed_data':parsed_data})
                    else:
                        yield parsed_data
                else:
                    continue


        else: #if including body_text we need to go to each article page
            #turn page text into dictionary
            response_data = eval(re.findall('<script>window.__APOLLO_STATE__ =(.+?)</script>', response_data)[0])
            #body text in Paragraph entries
            paragraph_keys = [key for key in response_data.keys() if "Paragraph:" in key and "." not in key]

            body_text = ''
            for paragraph_key in paragraph_keys:
                    body_text+=response_data[paragraph_key]['text']

            parsed_data['body'] = body_text


            yield parsed_data
