filename = "Hist1.txt"
file = open(filename, "r")


# Given an oral history file, return an array of speaker initials
def find_speakers(file):
    speakers = []
    for line in file:
        # Check if a speaker is identified at the beginning of a line
        index_speaker = line[0:4].find(':')
        if index_speaker != -1:
            speaker = line[0:index_speaker]
            if speaker not in speakers:
                speakers.append(speaker)
    return speakers

# Given an oral history file and an array of speaker identifiers,
# return an array of speaker initials
def count_speaker_freq(file, speakers):
    speaker_counts = {speaker: 0 for speaker in speakers}
    file.seek(0)  # Reset the file pointer to the beginning
    for line in file:
        for speaker in speakers:
            if speaker in line[0:4]:
                speaker_counts[speaker] += len(line.split()) - 1
                break
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
    return question, longest_line

speakers = find_speakers(file)
speaker_counts = count_speaker_freq(file, speakers)
lines = longest_qa_pair(file, speakers)
print(lines)
print(speaker_counts)


