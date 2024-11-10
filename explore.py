import os
import csv
from collections import Counter

"""
Given an oral history file, return a dictionary with keys
speaker initials and values [number of times spoken, words spoken]
"""
def find_speakers(filename):
    file = open(filename, "r")
    speakers = {}
    for line in file:
        # Check if a speaker is identified at the beginning of a line
        index_speaker = line[0:4].find(':')
        if index_speaker != -1:
            speaker = line[0:index_speaker]
            start = line.index(":") + 2
            words = line[start:].split()
            if speaker not in speakers:
                speakers[speaker] = [1, len(words)]
            else:
                speakers[speaker][0] = speakers[speaker][0]+1
                speakers[speaker][1] = speakers[speaker][1]+len(words)

    #print(filename)
    for key in speakers.keys():
        print(key)
    file.close()
    return speakers

# Given an oral history file and an array of speaker identifiers,
# return an array of speaker initials
def count_speaker_freq(file, speakers):
    file = open(file, "r")
    speaker_counts = {speaker: 0 for speaker in speakers}
    file.seek(0)  # Reset the file pointer to the beginning
    curr_speaker = None
    for line in file:
        if len(line) == 0: speaker = None
        if line[0] == '<': speaker = None
        for speaker in speakers:
            if speaker in line[0:4]:
                curr_speaker = speaker
        if curr_speaker:
            if curr_speaker == 'JC':
                print(line, len(line[4:].split()))
            speaker_counts[curr_speaker] += len(line.split())
    file.close()
    return speaker_counts

# Given an oral history file and an array of speaker identifiers,
# return the question and longest answer
def longest_qa_pair(file, speakers):
    longest_line = ""
    question = ""
    prev = ""
    file.seek(0)  # Reset the file pointer to the beginning
    for line in file:
        for speaker in speakers:
            if speaker in line[0:4]:
                if len(line) > len(longest_line):
                    longest_line = line
                    question = prev
                prev = line
    file.close()
    return question, longest_line

file = 'transcripts_clean/ddr-ajah-1-1-transcript.txt'
speakers = find_speakers(file)
print(speakers)

def check_lines(filename):
    file = open(filename, "r")
    ct=0
    for line in file:
        if line[2:4] != ": " and line[1:3] != ": " and line[3:5] != ": ":
            print(line[:30])
            ct+=1
    return ct

def count_interviewers(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        all = []
        for row in csv_reader:
            interviewers = row[1].split(",")
            for interviewer in interviewers:
                if len(interviewer)>0:
                    all.append(interviewer)
    c = Counter(all)
    # Sort by frequency in descending order
    print(f"Interviewer           Count")
    for interviewer, count in c.most_common(150):
        print(f"{interviewer:<20}: {count}")
    print("Number of unique interviewers: ", len(set(all)))


count_interviewers("metadata.csv")
# directory = 'transcripts_clean'
# for filename in os.listdir(directory):
#      file_path = os.path.join(directory, filename)
#      if os.path.isfile(file_path):
#          if filename != ".DS_Store":
            #find_speakers(file_path)
            #ct += check_lines(file_path)


