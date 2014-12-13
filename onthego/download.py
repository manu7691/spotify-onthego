from __future__ import print_function

from glob import glob
import os
import subprocess

import onthego.youtube

import eyed3

def audio(track, directory,
        skip_existing=True, convert_to_mp3=True):

    artist = track["artists"][0]["name"].encode("utf-8")
    track_name = track["name"].encode("utf-8")
    if should_skip(track_name, artist, directory, skip_existing, convert_to_mp3):
        print("++ Skipping %s - %s" % (artist, track_name))
        return

    print("++ Processing %s - %s" % (artist, track_name))
    audio_file_path = onthego.youtube.download_to_tmp(track_name, artist)
    if audio_file_path is None:
        print("---- No You Tube video found for '%s - %s'" % (artist, track_name))
        return

    convert_or_copy(audio_file_path, directory, track, convert_to_mp3)

def should_skip(track_name, artist, directory, skip_existing, convert_to_mp3):
    if skip_existing:
        if convert_to_mp3 and audio_file_is_already_downloaded(directory, track_name, artist, ".mp3"):
            return True
        elif not convert_to_mp3 and audio_file_is_already_downloaded(directory, track_name, artist, ".*"):
            return True
    return False

def audio_file_is_already_downloaded(directory, track_name, artist, extension):
    pattern = get_audio_file_path(directory, track_name, artist, extension)
    return len(glob(pattern)) > 0

def get_audio_file_path(directory, track_name, artist, extension):
    return os.path.join(directory, "%s - %s%s" % (artist, track_name, extension))

def convert(track,src_path, dst_path):
    subprocess.call(["avconv", "-v", "quiet", "-i", src_path, dst_path])
    os.remove(src_path)
    audiofile = eyed3.load(dst_path)
    audiofile.tag.artist = track["artists"][0]["name"]
    audiofile.tag.album = track["album"]["name"]
    numartists = len(track["artists"])    
    if (numartists)>0 :
        artists = ""
        for index in range(len(track["artists"])):
            artists=artists+track["artists"][index]["name"]
            if(index != (numartists-1)):
                artists=artists+","
    audiofile.tag.album_artist = artists
    audiofile.tag.title = track["name"]
    audiofile.tag.track_num = track["track_number"]
    audiofile.tag.save()


def convert_or_copy(audio_file_path, directory, track, convert_to_mp3):
    ensure_directory_exists(directory)
    if convert_to_mp3:
        dst_path = get_audio_file_path(directory, track["name"], track["artists"][0]["name"], ".mp3")
        remove_file(dst_path)
        convert(track,audio_file_path, dst_path)
    else:
        extension = os.path.splitext(audio_file_path)[1]
        dst_path = get_audio_file_path(directory, track["name"], track["artists"][0]["name"], extension)
        remove_file(dst_path)
        os.rename(audio_file_path)

def ensure_directory_exists(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
