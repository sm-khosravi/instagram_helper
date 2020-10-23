import json
import re

import instaloader
from instaloader import Post, Instaloader, Profile

from date_converter import Gregorian

instaloader_model = Instaloader(download_video_thumbnails=False,
                                compress_json=False,
                                download_geotags=False,
                                request_timeout=5)


def post_detail_download():
    list_pages = {}
    dict_post_props = {}
    post = get_and_check_post_url()
    dict_post_props['caption'] = post.caption
    dict_post_props['caption_hashtags'] = post.caption_hashtags
    dict_post_props['caption_mentions'] = post.caption_mentions
    dict_post_props['num_of_comments'] = post.comments
    date_time = post.date_local
    georgian_date = f'{date_time.year}-{date_time.month}-{date_time.day}'  # date is georgian
    dict_post_props['date'] = Gregorian(georgian_date).persian_string()  # date is georgian
    dict_post_props['time'] = f'{date_time.hour}:{date_time.minute}:{date_time.second}'  # time is iran
    dict_post_props['num_of_likes'] = post.likes
    dict_post_props['tagged_users'] = post.tagged_users
    if post.location:
        dict_post_props['location'] = post.location
    elif post.location_2:
        dict_post_props['location'] = post.location_2['slug']
    else:
        dict_post_props['location'] = None

    if post.typename == 'GraphSidecar':
        children = post.graph_sidecar_children()
        children = None
        if children:
            if len(children) > 0:
                num = 0
                for child in children:
                    page = {}
                    node = child['node']
                    page['is_video'] = node['is_video']
                    if node['is_video']:
                        page['video_url'] = node['video_url']
                        page['video_thumb_url'] = node['display_url']
                        page['video_view_count'] = node['video_view_count']
                        page['video_duration'] = None
                    else:
                        page['image_url'] = node['display_resources'][2]['src']
                        page['image_thumb_medium_url'] = node['display_resources'][1]['src']
                        page['image_thumb_small_url'] = node['display_resources'][0]['src']

                        list_tags = []
                        edges = node['edge_media_to_tagged_user']['edges']
                        for edge in edges:
                            username = edge['node']['user']['username']
                            list_tags.append(username)
                        page['tagged_users'] = list_tags

                    list_pages[f'page_{num}'] = page
                    num += 1
        else:
            for edge_number, sidecar_node in enumerate(post.get_sidecar_nodes(), start=1):
                page = {}
                page['is_video'] = sidecar_node.is_video
                if sidecar_node.is_video:
                    page[f'video_url_{edge_number}'] = sidecar_node.video_url
                    page[f'video_thumb_url_{edge_number}'] = sidecar_node.display_url
                    page['video_view_count'] = sidecar_node.video_view_count
                    page['video_duration'] = None
                else:
                    page[f'image_url_{edge_number}'] = sidecar_node.display_url
                    page['image_thumb_medium_url'] = None
                    page['image_thumb_small_url'] = None
                list_pages[f'page_{edge_number}'] = page
    elif post.typename == 'GraphImage':
        page = {}
        page['is_video'] = post.is_video
        page['image_url'] = post.url
        page['image_thumb_medium_url'] = post.display_resources[1].get('src', None)
        page['image_thumb_small_url'] = post.display_resources[0].get('src', None)
        list_pages['page_0'] = page
    elif post.typename == 'GraphVideo':
        page = {}
        page['is_video'] = post.is_video
        page['video_url'] = post.video_url
        page['video_thumb_url'] = post.url
        page['video_view_count'] = post.video_view_count
        page['video_duration'] = post.video_duration
        list_pages['page_0'] = page
    else:
        raise ("Warning: {0} has unknown typename: {1}".format(post, post.typename))

    dict_post = {'list_pages': list_pages, 'post_details': dict_post_props}
    # instaloader_model.download_post(post=post, target='download')
    print(dict_post)
    # return dict_post


def hashtag_posts_download():
    hashtag = input('write hashtag (without #): ')
    num = input('max of posts: ')
    num = int(num)
    dict_posts = {}
    dict_post_props = {}
    num_of_posts = 0
    list_posts = instaloader_model.download_hashtag(hashtag=hashtag, max_count=num)
    if len(list_posts) > 0:
        for post in list_posts:
            num_of_posts += 1
            dict_post_props['caption'] = post.caption
            dict_post_props['caption_hashtags'] = post.caption_hashtags
            dict_post_props['caption_mentions'] = post.caption_mentions
            dict_post_props['num_of_comments'] = post.comments
            dict_post_props['date'] = post.date_local  # date is georgian but time is iran
            dict_post_props['num_of_likes'] = post.likes
            dict_post_props['tagged_users'] = post.tagged_users
            if post.location:
                dict_post_props['location'] = post.location
            elif post.location_2:
                dict_post_props['location'] = post.location_2
            else:
                dict_post_props['location'] = None

            if post.typename == 'GraphSidecar':
                for edge_number, sidecar_node in enumerate(post.get_sidecar_nodes(), start=1):
                    if sidecar_node.is_video:
                        dict_post_props[f'video_url_{edge_number}'] = sidecar_node.video_url
                        dict_post_props[f'video_thumb_url_{edge_number}'] = sidecar_node.display_url
                        dict_post_props['video_view_count'] = sidecar_node.video_view_count
                    else:
                        dict_post_props[f'image_url_{edge_number}'] = sidecar_node.display_url
            elif post.typename == 'GraphImage':
                dict_post_props['image_url'] = post.url
                dict_post_props['is_video'] = post.is_video
            elif post.typename == 'GraphVideo':
                dict_post_props['is_video'] = post.is_video
                dict_post_props['video_duration'] = post.video_duration
                dict_post_props['video_url'] = post.video_url
                dict_post_props['video_view_count'] = post.video_view_count
            else:
                raise ("Warning: {0} has unknown typename: {1}".format(post, post.typename))

            dict_posts[f'post_{num_of_posts}'] = dict_post_props
    print(dict_posts)
    # return dict_posts


def post_comments():
    # post = get_and_check_post_url()
    # comments = instaloader_model.update_comments(post=post, filename='post_comments.json')
    file = open('post_comments.json', )
    comments = json.load(file)
    for comment in comments:
        text = comment['text']
        username = comment['owner']['username']
        print(text)


def igtv_download():
    profile_name = str(input('insert profile name: '))
    profile = Profile.from_username(instaloader_model.context, profile_name)
    list_igtv_urls = profile.get_igtv_videos()
    print(list_igtv_urls)
    # return list_igtv_urls


def story_download1():
    profile_name = str(input('insert profile name: '))
    profile = Profile.from_username(instaloader_model.context, profile_name)
    list_igtv_urls = profile.has_public_story
    print('list_igtv_urls')
    # return list_igtv_urls


def story_download():
    L = instaloader.Instaloader()
    L.login(user='smkh1285', passwd='sm110kh135')
    # L.interactive_login('smkh1285')
    # L.load_session_from_file('smkh1285')

    # L.two_factor_login(two_factor_code)
    post = Post.from_shortcode(L.context, 'CGkG0yHAU9i')
    L.download_post(post=post, target='download')

    # instaloader_model.download_storyitem(target=instaloader_model.download_stories, item=)
    # q = instaloader_model.check_profile_id(profile_name='campain.shivafar1')
    # instaloader_model.download_stories(userids=[q.userid])

    # import requests
    #
    # url = "https://rapidapi.p.rapidapi.com/media_likers"
    #
    # querystring = {"short_code": "CGXtIFoAmaN"}
    #
    # headers = {
    #     'x-rapidapi-host': "instagram28.p.rapidapi.com",
    #     'x-rapidapi-key': "ad7a9ffb31msh17871e5c370e9f0p15b073jsncd2109e5b65f"
    # }
    #
    # response = requests.request("GET", url, headers=headers, params=querystring)
    #
    # print(response.text)


def get_and_check_post_url():
    _RX_CODE = re.compile(r'^[0-9a-zA-Z_\-]{10,11}$')
    url = input('url: ')
    is_valid = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
    if is_valid:
        code = url.split('/')[4]
        if _RX_CODE.match(code):
            post = Post.from_shortcode(instaloader_model.context, code)
            return post
    return None
