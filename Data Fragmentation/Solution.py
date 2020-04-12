#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:30:52 2020

@author: parthavpatel
"""

import psycopg2
import os
import sys
# Donot close the connection inside this file i.e. do not perform openconnection.close()
def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    con = openconnection
    cur = con.cursor()
    # Fetching metadata
    cur.execute("select * from RangeRatingsMetadata;")
    metadatarows = cur.fetchall()
    anslist = []
    # Iterating through metadata table
    for row in metadatarows:
        minimumRating = row[1]
        maximumRating = row[2]
        table = "RangeRatingsPart" + str(row[0])
        if not ((ratingMinValue > maximumRating) or (ratingMaxValue < minimumRating)):
            cur.execute("select * from {} where rating >= {} and rating <= {};".format(table,str(ratingMinValue),str(ratingMaxValue)))
            results = cur.fetchall()
            # Writing data to a file
            for result in results:
                anslist.append((str(table),str(result[0]),str(result[1]),str(result[2])))
            
    #Fetching metadata
    cur.execute("select partitionnum from RoundRobinRatingsMetadata;")
    #Getting numberofpartitions
    numPartitions = cur.fetchall()[0][0]
    
    i = 0
    while i < numPartitions:
        table = "RoundRobinRatingsPart" + str(i)
        cur.execute("select * from {} where rating >= {} and rating <= {};".format(table, str(ratingMinValue),str(ratingMaxValue)))
        results = cur.fetchall()
        # Writing data to a file
        for result in results:
            anslist.append((str(table) ,str(result[0]), str(result[1]),str(result[2])))
        i+=1
    
    writeToFile("RangeQueryOut.txt", anslist)
    
        



def PointQuery(ratingsTableName, ratingValue, openconnection):
    con = openconnection
    cur = con.cursor()
    #Fetching metadata
    cur.execute("select * from RangeRatingsMetadata;")
    metarows = cur.fetchall()
    anslist = []
    # Iterating through metadata table
    for row in metarows:
        minimumRating = row[1]
        maximumRating = row[2]
        table = "RangeRatingsPart" + str(row[0])
        if ((row[0] == 0 and ratingValue >= minimumRating and ratingValue <= maximumRating) or (row[0] != 0 and ratingValue > minimumRating and ratingValue <= maximumRating)):
            cur.execute("select * from {} where rating = {};".format(table,str(ratingValue)))
            results = cur.fetchall()
            #Writing to a file
            for result in results:
                anslist.append((str(table),str(result[0]),str(result[1]),str(result[2])))

    #Fetching metadata
    cur.execute("select partitionnum from RoundRobinRatingsMetadata;")
    #Getting numberofpartitions
    numPartitions = cur.fetchall()[0][0]
    i = 0
    while i < numPartitions:
    	table = "RoundRobinRatingsPart" + str(i)
    	cur.execute("select * from {} where rating = {};".format(table,str(ratingValue)))
    	results = cur.fetchall()
        # Writing data to a file
        for result in results:
            anslist.append((str(table) ,str(result[0]), str(result[1]),str(result[2])))
        i+=1
    writeToFile("PointQueryOut.txt", anslist)
        
def writeToFile(filename, rows):
    f = open(filename, 'w')
    for line in rows:
        f.write(','.join(str(s) for s in line))
        f.write('\n')
    f.close()
            
                