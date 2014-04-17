#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Music module


"""

# music.py
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
        print("[limestonedb music][debug] "+str(msg))

def get_substone(file_name):
    try:
        data = lsutilities.get_raw_media_informations(file_name)
    except:
        return {}
    else:
        output = {}
        for inname, outname in [
                ("format_name", "format_name"), # mp3
                ("duration","duration"),        # 176.519250
                ]:
            if inname in data['format']:
                output[outname] = data['format'][inname]
        if 'tags' in data['format']:
            for inname, outname in [
                    ("artist","artist"),
                    ("title","title"),
                    ("genre","genre"),
                    ]:
                if inname in data['format']['tags']:
                    output[outname] = data['format']['tags'][inname]
        return output

