#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Video module


"""

# video.py
# This file is part of limestonedb
# 
# Copyright (C) 2014 - Enrico Polesel
#
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import lsutilities

debug = 5

def print_debug(level,msg):
    if level <= debug:
        print("[limestonedb film][debug] "+str(msg))

def get_substone(file_name):
    try:
        data = lsutilities.get_raw_media_informations(file_name)
    except:
        return {}
    else:
        output = {}
        for inname, outname in [
                ("format_name", "format_name"), # matroska,webm
                ("duration","duration"),        # 4515.712000
                ]:
            if inname in data['format']:
                output[outname] = data['format'][inname]
        if 'tags' in data['format']:
            for inname, outname in [
                    #("artist","artist"),
                    ("title","title"),
                    #("genre","genre"),
                    ]:
                if inname in data['format']['tags']:
                    output[outname] = data['format']['tags'][inname]
        output['video_stream'] = {}
        output['audio_streams'] = []
        output['subtitle_streams'] = []
        for stream in data['streams']:
            if stream['codec_type'] == 'video':
                for inname, outname in [
                    ('codec_name','codec'),
                    ('width','width'),
                    ('height','height'),
                    ]:
                    if inname in stream:
                        output['video_stream'][outname] = stream[inname]
            elif stream['codec_type'] == 'audio':
                thisstream = {}
                for inname, outname in [
                    ('codec_name','codec'),
                    ('channels','channels'),
                    ('index','index'),
                    ]:
                    if inname in stream:
                        thisstream[outname] = stream[inname]
                if 'tags' in stream:
                    for inname, outname in [
                        ('title','title'),
                        ('language','language'),
                        ]:
                        if inname in stream['tags']:
                            thisstream[outname] = stream['tags'][inname] 
                if thisstream != {}:
                    output['audio_streams'].append(thisstream)
            elif stream['codec_type'] == 'subtitle':
                thisstream = {}
                for inname, outname in [
                    ('codec_name','codec'),
                    ('index','index'),
                    ]:
                    if inname in stream:
                        thisstream[outname] = stream[inname]
                if 'tags' in stream:
                    for inname, outname in [
                        ('title','title'),
                        ('language','language'),
                        ]:
                        if inname in stream['tags']:
                            thisstream[outname] = stream['tags'][inname] 
                if thisstream != {}:
                    output['subtitle_streams'].append(thisstream)

        return output

