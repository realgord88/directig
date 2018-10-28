# -*- coding: UTF-8 -*-
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from InstagramAPI import InstagramAPI
import requests
import re
from datetime import datetime
import json

from igmain.models import IGaccount, IGmodel, IGpublic
from igmain.serializers import IGaccountSerializers, IGpublicSerializers


class IGaccounts(APIView):
    def get(self, request):
        igaccounts = IGaccount.objects.all()
        serializer = IGaccountSerializers(igaccounts, many=True)
        return Response(serializer.data)


class IGpublicsRival(APIView):
    def get(self, request):
        igpublics = IGpublic.objects.all()
        serializer = IGpublicSerializers(igpublics, many=True)
        return Response(serializer.data)

#old version
# def get_time_photo(code):
#     url_info = 'https://www.instagram.com/p/' + code
#     date = requests.get(url_info).content
#     date = date.decode("utf-8")
#     date = date.split('taken_at_timestamp":')[1]
#     date = date.split(',')[0]
#     date = datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
#     return date


class ChangeAccount(APIView):
    def post(self, request, format=None):
        global IG
        public_username = request.data['public']
        account_db = IGaccount.objects.get(igaccount=public_username)
        password_db = account_db.igpassword
        IG = InstagramAPI(public_username, password_db)
        IG.login()
        return Response({'status': 'ok'})


IG = None  # global IG


class InfoAccountPublic(APIView):
    def post(self, request, format=None):

        global IG
        if not IG:
            return Response({'status': 'you must be logged in'})

        all_info = {}  # finally info

        public_username = request.data['username']

        try:
            IG.searchUsername(public_username)
            userid = IG.LastJson["user"]["pk"]
        except IndexError:
            return Response({'status': 'page does not exist'})

        # getting number media of public page
        IG.getUsernameInfo(userid)
        n_media = IG.LastJson['user']['media_count']
        followers_public = IG.LastJson['user']['follower_count']
        all_info = {'photos': n_media, 'followers': followers_public}

        IG.getUserFeed(userid)
        req = IG.LastJson

        finally_json = req['items']

        for pagination in range(4):
            next_max_id = req['next_max_id']
            IG.getUserFeed(userid, maxid=next_max_id)
            req = IG.LastJson
            finally_json.extend(req['items'])

        for photo_numb in range(len(finally_json)):
            try:
                caption = finally_json[photo_numb]['caption']['text']
                nickname_girl = re.search(r'@[\w.]+\S', caption)
                nickname_girl = nickname_girl.group(0)[1:]
                #delete emoji
                emoji_pattern = re.compile('['
                                           u'\U0001F600-\U0001F64F'  # emoticons
                                           u'\U0001F300-\U0001F5FF'  # symbols & pictographs
                                           u'\U0001F680-\U0001F6FF'  # transport & map symbols
                                           u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
                                           ']+', flags=re.UNICODE)
                nickname_girl = emoji_pattern.sub(r'', nickname_girl)

                IG.searchUsername(nickname_girl)
                followers_girls = IG.LastJson['user']['follower_count']
            except Exception:  # without caption or nickname
                nickname_girl = 'error'
                followers_girls = '0'

            try:
                dm_status = IGmodel.objects.get(igmodel=nickname_girl)
                dm_status = dm_status.msg_status
            except Exception:
                dm_status = False

            try:
                created_time = (finally_json[photo_numb]['caption']['created_at'])
                created_time = datetime.utcfromtimestamp(int(created_time)).strftime('%Y-%m-%d %H:%M:%S')
            except:
                created_time = 'error'

            try:
                thumbnail_url = finally_json[photo_numb]['image_versions2']['candidates'][1]['url']
            except KeyError:  # if gallery
                thumbnail_url = \
                    finally_json[photo_numb]['carousel_media'][0]['image_versions2']['candidates'][1]['url']
                continue

            all_info[photo_numb + 1] = {'created_time': created_time, 'nickname': nickname_girl,
                                        'followers': followers_girls, 'dm_status': dm_status,
                                        'photo': thumbnail_url}

        return Response({'info': all_info})


class DirectShare(APIView):
    def post(self, request, format=None):
        global IG
        model_username = request.data['username']

        IG.searchUsername(model_username)
        userid = IG.LastJson["user"]["pk"]

        text = 'msg '

        direct = IG.direct_message(recipients=userid, text=text)
        if direct:
            dm_status = IGmodel(igmodel=model_username, msg_status=True)
            dm_status.save()
            return Response({'status': 'sent'})
        else:
            return Response({'status': 'error'})


class AddPublicRival(APIView):
    def post(self, request, format=None):
        public_username = request.data['public']
        public_db = IGpublic(igpublic=public_username)
        public_db.save()
        return Response({'status': 'ok'})


class DelPublicRival(APIView):
    def post(self, request, format=None):
        public_username = request.data['public']
        public_db = IGpublic.objects.get(igpublic=public_username)
        public_db.delete()
        return Response({'status': 'ok'})
