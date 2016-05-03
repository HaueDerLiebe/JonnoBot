# -*- coding: utf-8 -*-
"""
Created on Mon May 02 19:35:18 2016

@author: Markus
"""

import praw
import re
import os
user_agent = ("Jonno Bet 0.1");

r = praw.Reddit(user_agent = user_agent)
 
subreddit = r.get_subreddit("sportsbook")

teams=[["ATL",      "Atlanta",      "Hawks"],
["BKN",    "Brooklyn",     "Nets"],
["BOS",	"Boston", "Celtics"],
["CHA",	"Charlotte" ,"Hornets"],
["CHI",	"Chicago", "Bulls"],
["CLE",     "Cleveland" ,"Cavaliers","Cavs"],
["DAL",     "Dallas", "Mavericks"],
["DEN",     "Denver" ,"Nuggets"],
["DET",     "Detroit", "Pistons"],
["GS",      "Golden State" ,"Warriors"],
["HOU",	"Houston", "Rockets"],
["IND"	,"Indiana" ,"Pacers"],
["LAC"	,"Los Angeles", "Clippers"],
["LAL"	,"Los Angeles","Lakers"],
["MEM"	,"Memphis", "Grizzlies"],
["MIA"	,"Miami" ,"Heat"],
["MIL"	,"Milwaukee", "Bucks"],
["MIN"	,"Minnesota","Timberwolves"],
["NOP"	,"New Orleans", "Pelicans"],
["NYK"	,"New York" ,"Knicks"],
["OKC"	,"Oklahoma City" ,"Thunder"],
["ORL"	,"Orlando" ,"Magic"],
["PHI"	,"Philadelphia" ,"76ers"],
["PHX"	,"Phoenix" ,"Suns"],
["POR"	,"Portland", "Trail Blazers"],
["SAC"	,"Sacramento" ,"Kings"],
["SA"      ,"San Antonio" ,"Spurs"],
["TOR"	,"Toronto", "Raptors"],
["UTA"	,"Utah", "Jazz"],
["WSH"	,"Washington" ,"Wizards"]];

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)




playing=[];
for submission in subreddit.get_new(limit = 50):
    t=re.match(r'NBA Daily',submission.title);
    if t is not None:
        for index1, item1 in enumerate(teams):
#            print index1,item1
            for index2, item2 in enumerate(item1):
                t_match=re.search(item2,submission.selftext)
                if t_match is not None:
                    playing.append([index1,index2,item2,0,submission.title[10:len(submission.title)]]);
        submission.replace_more_comments(limit=None, threshold=0);
        flat_comments=praw.helpers.flatten_tree(submission.comments)
        for team in playing:
            mask=r"";
            for name_index,name in enumerate(teams[team[0]]):
                mask+="(" + name + " \+|"+name+r" \-)";
                if len(teams[team[0]])-1>name_index:
                    mask+="|";
#            print mask
            for comment in flat_comments:
#                print comment.id
                if comment.id not in posts_replied_to:
                    if re.search(mask,comment.body,re.IGNORECASE) is not None:
                        team[3]+=1;
                        posts_replied_to.append(comment.id)
                    
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")            
#        print "Title: ", submission.title
#        print "Score: ", submission.score
#        print "Text: ", submission.selftext
#        print "---------------------------------\n"
#        for 
#        text=submission.selftext
#with open("results.txt", "w") as f:
#    for result in playing:
#        for resultresult in result:
#            f.write(resultresult + "\n")            
