#!/usr/bin/env python3

from requests import post
import subprocess
import argparse
import platform
from os import mkdir, chdir, remove

url = 'https://graphql.melearn.mn'

def get_course(url: str, course_id: str, quality: str, auth: dict, yt_dlp: str) -> None:
    _data = {"operationName": "get_course_chapters", "variables": {"course": f"{course_id}"},
                 "query": "query get_course_chapters($course: ID!) {\n  get_course_chapters(course: $course) {\n    chapters {\n      _id\n      title\n      description\n      sortBy\n      createdAt\n      updatedAt\n      createdUser {\n        _id\n        firstname\n        lastname\n        username\n        email\n        avatar\n        followed\n        amisubscription\n        amipremium\n        __typename\n      }\n      lessons {\n        _id\n        title\n        description\n        type\n        status\n        isComplete\n        lastWatchPosition\n        createdAt\n        updatedAt\n        video {\n          _id\n          duration\n          __typename\n        }\n        __typename\n      }\n      \n      __typename\n    }\n    __typename\n  }\n}\n"}
    resp = post(url=url, json=_data, headers=auth)
    _index = 0
    for chapter in resp.json()['data']['get_course_chapters']['chapters']:
        for lesson in chapter['lessons']:
            _id = lesson['_id']
            _title = str(_index) + ' - ' + lesson['title'].replace(' ', '_') + '.mp4'
            _index += 1
            _data2 = {"operationName": "get_course_lesson", "variables": {"_id": f"{_id}"},
                          "query": "query get_course_lesson($_id: String) {\n  get_course_lesson(_id: $_id) {\n    lesson {\n      _id\n      title\n      description\n      type\n      status\n      isComplete\n      lastWatchPosition\n      createdAt\n      updatedAt\n      chapter {\n        _id\n        __typename\n      }\n      video {\n        _id\n        p360\n        p480\n        p720\n        p1080\n        duration\n        key\n        __typename\n      }\n      file {\n        _id\n        thumb_800\n        thumb_300\n        url\n        duration\n        videoThumbnail\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
            try:
                x = post(url=url, json=_data2, headers=auth)
                video_url = x.json()['data']['get_course_lesson']['lesson']['video'][quality] #p720

                subprocess.run([yt_dlp, '-o', _title, video_url]) #os.system(f'..\yt-dlp.exe -o {_title} ' + p72)
                print(_title)
                print('\n***\n')
            except Exception as e:
                print('Suirel2: ', e)

def login(url: str, uname: str, passwd: str) -> str:
    _data = {"operationName":"login","variables":{"email":f"{uname}","password":f"{passwd}"},"query":"mutation login($email: String!, $password: String!) {\n  login(email: $email, password: $password) {\n    success\n    message\n    token\n    user {\n      _id\n      firstname\n      lastname\n      avatar\n      cover\n      email\n      emailVerified\n      username\n      phoneprefix\n      phonenumber\n      countrycode\n      bio\n      instagram\n      twitter\n      amiadmin\n      amipremium\n      amipodcaster\n      amiblogger\n      amiteacher\n      amiverified\n      amisubscription\n      specialteacher\n      specialblogger\n      accountType\n      blocked\n      followed\n      followers\n      following\n      referralCode\n      contentcount\n      createdAt\n      updatedAt\n      __typename\n    }\n    __typename\n  }\n}\n"}
    resp = post(url=url,json=_data)
    return resp.json()['data']['login']['token']

def search(url: str, title: str) -> str:
    _data = {"operationName":"search","variables":{"keyword":f"{title}","categoryIds":[],"type":"all"},"query":"query search($keyword: String, $categoryIds: [String], $type: SearchType!) {\n  search(keyword: $keyword, categoryIds: $categoryIds, type: $type) {\n    success\n    message\n    result {\n      courses {\n        _id\n        title\n        url\n        overview\n        level\n        language\n        status\n        tags\n        image {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        price\n        teacher {\n          _id\n          firstname\n          lastname\n          username\n          email\n          avatar\n          followed\n          amisubscription\n          amipremium\n          __typename\n        }\n        categories {\n          _id\n          title\n          url\n          image\n          description\n          index\n          createdAt\n          updatedAt\n          __typename\n        }\n        contentStatus\n        isCertificate\n        isSpecial\n        examCount\n        watchUserCount\n        isBookmark\n        isBlocked\n        isLocked\n        totalDuration\n        myProgress\n        viewCount\n        rate\n        isCanRate\n        totalLessons\n        createdAt\n        courseType\n        updatedAt\n        isComplete\n        __typename\n      }\n      episodes {\n        _id\n        title\n        description\n        url\n        image {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        audio {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        totalClapCount\n        clapCount\n        commentCount\n        createdUser {\n          _id\n          firstname\n          lastname\n          username\n          email\n          avatar\n          followed\n          amisubscription\n          amipremium\n          __typename\n        }\n        viewCount\n        status\n        isView\n        isBookmark\n        createdAt\n        podcast {\n          _id\n          title\n          url\n          categories {\n            _id\n            title\n            url\n            image\n            description\n            index\n            createdAt\n            updatedAt\n            __typename\n          }\n          tags\n          image {\n            _id\n            thumb_800\n            thumb_300\n            url\n            duration\n            videoThumbnail\n            __typename\n          }\n          isSpecial\n          user {\n            _id\n            firstname\n            lastname\n            username\n            email\n            avatar\n            followed\n            amisubscription\n            amipremium\n            __typename\n          }\n          totalEpisodes\n          status\n          contentStatus\n          createdAt\n          __typename\n        }\n        __typename\n      }\n      blogs {\n        _id\n        title\n        description\n        url\n        viewCount\n        frontImage {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        coverImage {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        content\n        isSpecial\n        isBookmark\n        readMinute\n        status\n        contentStatus\n        categories {\n          _id\n          title\n          url\n          image\n          description\n          index\n          createdAt\n          updatedAt\n          __typename\n        }\n        isView\n        createdAt\n        totalClapCount\n        commentCount\n        clapCount\n        createdUser {\n          _id\n          firstname\n          lastname\n          username\n          email\n          avatar\n          followed\n          amisubscription\n          amipremium\n          __typename\n        }\n        __typename\n      }\n      audiobooks {\n        _id\n        title\n        url\n        image {\n          _id\n          thumb_800\n          thumb_300\n          url\n          duration\n          videoThumbnail\n          __typename\n        }\n        categories {\n          _id\n          title\n          url\n          image\n          description\n          index\n          createdAt\n          updatedAt\n          __typename\n        }\n        tags\n        overview\n        description\n        author {\n          name\n          bio\n          image {\n            _id\n            thumb_800\n            thumb_300\n            url\n            duration\n            videoThumbnail\n            __typename\n          }\n          __typename\n        }\n        status\n        contentStatus\n        isSpecial\n        isView\n        isLocked\n        isBookmark\n        viewCount\n        totalDuration\n        chapterCount\n        createdAt\n        __typename\n      }\n      users {\n        _id\n        firstname\n        lastname\n        username\n        email\n        avatar\n        followed\n        amisubscription\n        amipremium\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    resp = post(url=url, json=_data)
    return resp.json()['data']['search']['result']['courses'][0]['_id']

def get_ytdlp() -> str:
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.run(['powershell', '-Command', 'Invoke-WebRequest', '-Uri', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', '-OutFile', 'yt-dlp.exe'], capture_output=True)
        return 'yt-dlp.exe'
    elif os_name == "Darwin":
        subprocess.run(['wget', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos'], capture_output=True)
        return 'yt-dlp_macos'
    else:
        subprocess.run(['wget', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp'], capture_output=True)
        return 'yt-dlp'
def main() -> None:
    auth = {}
    parser = argparse.ArgumentParser(description="Download courses from melearn.mn")
    parser.add_argument("username", type=str, help="Нэвтрэх нэр")
    parser.add_argument("password", type=str, help="Нууц үг")
    parser.add_argument("title", type=str, help="Татах хичээлийн нэр")
    parser.add_argument("res", type=str, help="Татах хичээлийн quality: p360, p480, p720, p1080")
    args = parser.parse_args()
    auth['Authorization'] = login(url, args.username, args.password)
    course_id = search(url, args.title)
    mkdir(args.title)
    chdir(args.title)
    bin = get_ytdlp()
    get_course(url=url, course_id=course_id, quality=args.res, auth=auth, yt_dlp=bin)
    remove(bin)
    print('Done. ')

if __name__ == "__main__":
    main()