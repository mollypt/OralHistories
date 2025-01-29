
# Includes modules to
#       1.) convert htm transcript files to text files,
#       2.) extract metadata from the cleaned transcript files,
#       3.) further clean text files such that dialogue appears on one line

from bs4 import BeautifulSoup
import os
import csv
import pandas as pd

# Clean html file with path filepath and write to transcripts_txt/filename
def html_to_text(filepath, filename):
    try:
        # Try reading the HTML file using UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try reading with ISO-8859-1 (Latin-1)
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # Get the entire text content of the HTML file
    plain_text = soup.get_text()

    # Strip leading whitespace from each line
    stripped_text = "\n".join(line.lstrip() for line in plain_text.splitlines())
    # print(stripped_text)

    # Save the cleaned plain text to a file
    output_filename = f"transcripts_txt/{filename[:-4]}.txt"
    with open(output_filename, 'w', encoding='utf-8', errors='ignore') as output_file:
        output_file.write(stripped_text)

# Write metadata of interview with path filepath, name filename to metadata_backup.csv
def get_metadata(filepath, filename):
    # Initialize flags to check if metadata found
    title_found = False
    narrator_found = False
    interviewer_found = False
    date_found = False
    location_found = False
    collection_found = False
    id_found = False
    title, narrator, interviewer, date, location, collection, id = None, None, None, None, None, None, None

    with open(filepath, 'r', encoding='utf-8') as file:
        linect = 0
        for i, line in enumerate(file, start=1):
            # Collection title appears on third line
            if len(line) > 1:
                linect += 1
                if linect == 3:
                    collection = line[:-1]
                    collection_found = True

            # Look for title
            if line[:6] == "Title:" and not title_found:
                try:
                    title = line.strip().split(":")[1].strip()
                    title_found = True  # Set the flag to True if a name is found
                except IndexError:
                    # If there's an error in parsing the name, pass through silently
                    pass

            # Look for narrator
            if line[:8] == "Narrator" and not narrator_found:
                try:
                    narrator = line.strip().split(":")[1].strip()
                    narrator_found = True
                    while ", " in narrator:
                        start = narrator.lower().index(", ")
                        narrator = narrator[:start+1]+ narrator[start+2:]
                    while " - " in narrator:
                        start = narrator.lower().index(" - ")
                        narrator = narrator[:start] + "," +narrator[start + 3:]
                    if " and " in narrator:
                        start = narrator.lower().index(" and ")
                        narrator = narrator[:start] +"," +narrator[start + 5:]
                except IndexError:
                    print(IndexError)
                    pass

            # Look for interviewer
            if line[:11] == "Interviewer" and not interviewer_found:
                try:
                    # Attempt to extract the name as you specified
                    interviewer = line.strip().split(":")[1].strip()
                    interviewer_found = True  # Set the flag to True if a name is found
                    if " (primary)," in interviewer.lower() or " (primary);" in interviewer.lower():
                        start = interviewer.lower().index(" (primary)")
                        interviewer = interviewer[:start].strip() + "," + interviewer[start+len("(primary),")+1:].strip()
                        #print(interviewer)
                    if "(secondary)" in interviewer.lower():
                        start = interviewer.lower().index("(secondary)")
                        interviewer = interviewer[:start].strip()
                        #print(interviewer)
                    if ", " in interviewer:
                        start = interviewer.lower().index(", ")
                        interviewer = interviewer[:start+1]+ interviewer[start+2:]
                except IndexError:
                    print(IndexError)
                    pass

            # Look for date
            if line[:4] == "Date" and not date_found:
                try:
                    date = line.strip().split(":")[1].strip()
                    date_found = True
                except IndexError:
                    print(IndexError)
                    pass

            # Look for location
            if line[:8] == "Location" and not location_found:
                try:
                    location = line.strip().split(":")[1].strip()
                    location_found = True
                except IndexError:
                    print(IndexError)
                    pass

            # Look for Densho ID
            if line[:9] == "Densho ID" and not id_found:
                try:
                    id = line.strip().split(":")[1].strip()
                    id_found = True
                except IndexError:
                    print(IndexError)
                    pass

        # Print information not found
        if not title_found:
            print(f"No title found for file {filename}")
        if not narrator_found:
            print(f"No narrator found for file {filename}")
        if not interviewer_found:
            print(f"No interviewer found for file {filename}")
        if not date_found:
            print(f"No date found for file {filename}")
        if not location_found:
            print(f"No location found for file {filename}")
        if not collection_found:
            print(f"No collection found for file {filename}")
        if not id_found:
            print(f"No id found for file {filename}")

        data = [
            [narrator, interviewer, date, location, collection, title, id, filename]
        ]


        with open("metadata_temp.csv", "a", newline="") as file2:
            writer = csv.writer(file2)
            writer.writerows(data)  # Pass the list of lists as a single argument

    # Define csv headers
    headers = ["Narrator", "Interviewer", "Date", "Location", "Collection", "Title", "ID", "filename"]

    # Read the CSV without headers
    df = pd.read_csv("metadata_temp.csv", header=None)

    # Save the new CSV with headers by first writing the headers, then appending the data
    df.to_csv("metadata.csv", header=headers, index=False)



# Run to print copyright and narrator notes
# directory = 'transcript_lines'
# for filename in os.listdir(directory):
#     file_path = os.path.join(directory, filename)
#     if os.path.isfile(file_path):
#         if filename != ".DS_Store":
#             find_tags(file_path, filename)



# # Run to get metadata
# directory = 'transcripts_txt'
# for filename in os.listdir(directory):
#      file_path = os.path.join(directory, filename)
#      if os.path.isfile(file_path):
#          if filename != ".DS_Store":
#             get_metadata(file_path, filename)
# # get_metadata('transcripts_txt/ddr-densho-1000-81-transcript-9e2a615857.txt', 'ddr-densho-1000-81-transcript-9e2a615857.txt')

# Run to write html transcripts_original > txt transcripts_original
# directory = 'transcripts_original'
# # Iterate over files in the directory
# for filename in os.listdir(directory):
#     file_path = os.path.join(directory, filename)
#     # Check if it's a file (and not a directory)
#     if os.path.isfile(file_path):
#         html_to_text(file_path, filename)
#html_to_text('transcripts_original/ddr-densho-1000-83-transcript-8859458391.htm', 'ddr-densho-1000-83-transcript-8859458391.txt')
