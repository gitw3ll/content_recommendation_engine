# -*- coding: utf-8 -*-
"""
based off https://github.com/AiswaryaSrinivas/Scraping-Medium-and-Data-Analysis/blob/master/medium_scrapper_tag_archive.py
This scrapper extracts data for a given date range for a particular Medium Tag

to run:
`scrapy runspider -a tag='tagSlug' -a start_date=YYYYmmdd -a end_date=YYYYmmdd medium_scraper_tag_archive.py`
e.g. `scrapy runspider -a tag='wellness' -a start_date=20200101 -a end_date=20200601 medium_scraper_tag_archive.py`
"""

import scrapy
from datetime import datetime
from datetime import timedelta
import os
import re
from scrapy.exporters import JsonItemExporter
# from scrapy.utils.log import configure_logging



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


    def parse(self,response):

        response_data=response.text

        #turn text into dictionary
        true = True
        false = False
        response_data = eval(re.findall('window\["obvInit"\]\((.+)\)', response_data)[0])

        if response._url in self.start_urls:

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

            # self.total_articles +=len(article_urls)
            n_articles_to_add = sum([1 for clap in clap_count if clap >=int(self.clap_limit)])
            self.total_articles +=n_articles_to_add
            print('***** {0} articles on {1}, {2} total articles so far ****'.format(n_articles_to_add, date, self.total_articles))

            # for url,claps in zip(article_urls,article_clap_counts):
            #     if int(claps)>=int(self.clap_limit):
            #         yield scrapy.Request(url,callback=self.parse)
            #     else:
            #         continue

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
                    yield parsed_data
                else:
                    continue

        else:
            import pdb; pdb.set_trace()
            date = re.findall('"datePublished":"([0-9-]+)T', response_data)[0]

            try:
                tags= set(re.findall('"Tag:([a-z-]+)"', response_data))
            except:
                tags = re.findall('href="/tag/([\w-]+?)"', response_data)

            css_title = response.css('title::text').getall()[0].split(' | ')
            try:
                #doesn't work for all, but when it does it works better than css_title[0]
                title = re.findall('"og:title" content="([\w .:,?!-/“]+)"', response_data)[0]
            except:
                title = css_title[0]
            try:
                author = re.findall('name="author" content="([\w .:,-]+)"', response_data)[0]
            except:
                author = css_title[1][3:] #remove "by "

            responses_count = int(re.findall('"responsesCount":([0-9]+)', response_data)[0])
            claps = int(re.findall('"clapCount":([0-9]+)', response_data)[0])
            length = int(re.findall('value="([0-9]+) min read"', response_data)[0])
            url = response._url
            comments = None
            author_bio = None
            subtitle = None

            parsed_data = {"date":date,
                        "tags":tags,
                        "title":title,
                        "author":author,
                        "claps":claps,
                        "length":length,
                        "url":url,
                        "responses_count": responses_count}


            yield parsed_data
