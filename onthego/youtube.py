from __future__ import print_function

import os

import tempfile
import gdata.youtube.service
import pafy

def download_to_tmp(track_name, artist):
    video = check_url(track_name, artist,True)
    video2 = check_url(track_name, artist,False)
    if(video==None and video2==None):
        return None
    elif(video==None and video2!=None):
        best=video2.getbestaudio()
    elif(video!=None and video2==None):
        best=video.getbestaudio()
    elif(video.length >= video2.length):
        best = video2.getbestaudio()
    else:    
        best = video.getbestaudio()  
    tmp_path = get_tmp_path(best)
    best.download(tmp_path)
    return tmp_path

def check_url(track_name, artist,no_lyrics):
    swf_url = get_swf_url(track_name, artist,no_lyrics)
    if swf_url is None:
        return None
    video = pafy.new(swf_url)
    return video


def get_swf_url(track_name, artist,no_lyrics):
    search_query = get_search_query(track_name, artist,no_lyrics)
    swf_url = get_first_search_result(search_query)
    return swf_url

def get_search_query(track_name, artist,no_lyrics):
    if no_lyrics == False :
        return (track_name + " " + artist + " lyrics").lower()
    else :
        return (track_name + " " + artist).lower()


def get_first_search_result(search_query):
    yt_service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    try:
        query.vq = search_query.encode("utf-8")
    except UnicodeDecodeError:
        query.vq = search_query
    feed = yt_service.YouTubeQuery(query)
    # return first entry with valid swf url
    for entry in feed.entry:
        if entry.GetSwfUrl() is not None:
            return entry.GetSwfUrl()

def get_tmp_path(result_stream):
    filename = result_stream.title + "." + result_stream.extension
    filename = filename.replace('/', ' ')
    return os.path.join(tempfile.gettempdir(), filename)
