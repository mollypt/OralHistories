import os
import csv
from collections import Counter
import matplotlib.pyplot as plt


def lexical_dispersion(filepath, word1, word2):
    # Initialize lists to hold the line numbers where the words appear
    line_numbers_word1 = []
    line_numbers_word2 = []

    # Open the file and read it line by line
    with open(filepath, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):  # Keep track of line numbers
            # Check if each word appears in the line
            if word1 in line.split():
                line_numbers_word1.append(line_number)
            if word2 in line.split():
                line_numbers_word2.append(line_number)

    # Plot the dispersion for both words
    plt.figure(figsize=(12, 4))  # Adjust figure size
    plt.scatter(line_numbers_word1, [1] * len(line_numbers_word1),
                marker='|', color='blue', s=300, label=word1)  # Plot word1 in blue
    plt.scatter(line_numbers_word2, [2] * len(line_numbers_word2),
                marker='|', color='red', s=300, label=word2)  # Plot word2 in red

    # Adjust plot aesthetics
    plt.yticks([1, 2], [word1, word2], fontsize=10)  # Label y-axis with the two words
    plt.xticks(fontsize=10)  # Make x-axis labels readable
    plt.xlabel("Line Number", fontsize=12)  # Label for x-axis
    plt.title(f"Lexical Dispersion of '{word1}' and '{word2}' in {filepath.split('/')[-1]}", fontsize=14)
    plt.legend(loc='upper right')  # Add a legend for the two words
    plt.grid(axis='x', linestyle='--', alpha=0.5)  # Simplify gridlines
    plt.tight_layout()  # Avoid overlapping elements
    plt.show()

lexical_dispersion("transcripts_clean/ddr-densho-1000-118-transcript-f9c855a292.txt",
                   '[Eng.]', '[Jpn.]')

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
        if line.find(": ") > 4 or line.find(": ") == -1:
            print(filename, line[:30])
            ct+=1
    return 1

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


# count_interviewers("metadata.csv")
# directory = 'transcripts_clean'
# ct=0
# for filename in os.listdir(directory):
#      file_path = os.path.join(directory, filename)
#      if os.path.isfile(file_path):
#          if filename != ".DS_Store":
#             # find_speakers(file_path)
#             ct += check_lines(file_path)
# print(ct)


