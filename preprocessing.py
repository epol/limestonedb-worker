#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Preprocessing program

This program will:
- check if there are a new file to process (not implemented yet)
- process the file getting informations (not implemented yet)
- move the file to the proper directory (not implemented yet)

"""

# preprocessing.py
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

import hashlib
import pymongo
import datetime
import os
import importlib

debug = 5

def print_debug(level,msg):
    if level <= debug:
        print("[limestonedb preprocessing][debug] "+str(msg))

def get_file_hash_size(file_name):
    file_hash = hashlib.sha512()
    chunk_size = 1024*1024  # 1MiB
    try:
        with open(file_name, 'rb') as f:
            byte = f.read(chunk_size)
            previous_byte = byte
            byte_size = len(byte)
            while byte:
                file_hash.update(byte)
                previous_byte = byte
                byte = f.read(chunk_size)
                byte_size += len(byte)
    except IOError:
        raise ("Unable to read "+file_name)
    except:
        raise ("Error while hashing "+file_name)
    return file_hash.hexdigest() , byte_size

def create_stone(file_name):
    hashsum , size = get_file_hash_size(file_name)
    stone = {
        'name' : os.path.basename(file_name) ,
        'hash' : hashsum,
        'size' : size,
        # TODO: location,
        'insertion_date' : datetime.datetime.utcnow()
        }
    return stone

def insert_in_db(mongodb, stone):
    try:
        stones = mongodb['stones']
        insertion_id = stones.insert(stone)
    except:
        raise ("Error inserting in the db")
    else:
        return insertion_id

def scan_directory(mongodb,path,modules = []):
    found = []
    for dirpath, dirs, files in os.walk(path):
        for file_name in files:
            print("Scanning "+file_name)
            try:
                stone = create_stone(os.path.join(dirpath,file_name))
                for module in modules:
                    try:
                        substone = get_substone(module,os.path.join(dirpath,file_name))
                    except:
                        pass
                    else:
                        if substone != {}:
                            stone[module] = substone
            except:
                print ("Unable to process "+ os.path.join(dirpath,file_name))
            else:
                found.append(insert_in_db(mongodb,stone))
    return found
    



def initialize_db(url):
    try:
        client = pymongo.MongoClient(url)
        database = client['limestone']
    except:
        raise ('Database error')
    else:
        return database
    

def get_substone(module_name, file_name):
    try:
        module = importlib.import_module(module_name)
    except:
        raise("Error importing "+module_name+" module")
    try:
        substone = module.get_substone(file_name)
    except:
        raise("Error getting the "+module_name+" substone from "+file_name)
    else:
        return substone

