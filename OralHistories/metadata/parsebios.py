"""
Parse narrator bios to create dataset with columns
"id", "Narrator", "Bio", "Birthday", "Birthplace"
"""
import csv
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')

with open("scraped_bios.csv", 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    ct, ct2 =0,0
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    data = []
    for row in reader:
        bio = row[2].strip()
        birthday_str = ""
        loc = ""
        if "born" in bio.lower():
            birthday_start = bio.lower().index("born") + 4
            s = bio[birthday_start:].split(".")[0].split()
            for w in s:
                if w[:4].strip().isdigit():
                    birthday_str = w[:4]
                    ct += 1
                    break

            # # Born April 30, 1902
            # if birthday[0] in months:
            #     if birthday[1][:-1].isdigit():
            #         if birthday[2][:4].isdigit():
            #             birthday_str = birthday[0] + " " + birthday[1][:-1]+ " " +birthday[2][:4]
            #             ct +=1
            # # Born in 1902
            # elif birthday[0] == "in":
            #     if birthday[1][0:4].isdigit():
            #         ct +=1
            #         birthday_str = birthday[1][:4]
            # # Born 1902
            # elif birthday[0][0:4].isdigit():
            #     ct += 1
            #     birthday_str = birthday[0][0:4]

            # Look for birth location
            bio_arr = bio[birthday_start:].split(".")[0].split()
            potential_place=False

            if len(bio_arr) > 13:
                max=13
            else:
                max=len(bio_arr)

            found = False
            start = -1
            end = -1
            for i in range(max):
                if bio_arr[i] == "in" and not found:
                    start = i
                    for j in range(i+1, max):
                        if end !=-1 and j - end > 3:
                            break
                            found = True
                        if bio_arr[j] == "in":
                            break
                        doc = nlp(bio_arr[j])
                        for entity in doc.ents:
                            if entity.label_ == 'GPE':
                                found = True
                                end = j
                                break

            # print(start, end+1)
            for k in range(start+1, end+1):
                loc += bio_arr[k] + " "

            if len(loc) > 0:
                if loc.strip()[-1] == "." or loc.strip()[-1] == ",":
                    loc = loc.strip()[:-1]
                ct2+=1
                print(f"{loc:<{50}}{row[1]}")

            #
            #         potential_place = True
            #     elif potential_place:
            #
            #
            #
            #         curr = False
            #         doc = nlp(bio_arr[i])
            #         for entity in doc.ents:
            #             if entity.label_ == 'GPE':
            #                 end = i
            #                 prev = True
            #                 curr = True
            #                 loc += entity.text + " "
            #         if prev and not curr:
            #             break
            #
            # if len(loc) > 0:
            #     ct2 += 1
            #     middle = ""
            #     for i in range(start+1, end):
            #         middle += bio_arr[i] + " "
            #
            # if middle.strip()[:-1] not in loc:
            #     loc = middle.strip()[:-1] + " "+ loc
            # print(loc)

                # doc = nlp(middle)
                # print(middle)
                # for entity in doc.ents:
                #     if entity.label_ == 'GPE':
                #         print(entity, "is a location.")
                #         # print(entity.text)
                #         if entity.text not in loc:
                #             # print(entity.text)
                #             print("adding", entity.text, "to location.")
                #             loc = entity.text + " " + loc

            # print(bio_arr[:13])
            # print()


            # doc = nlp(bio[birthday_start:birthday_start+50])
            # loc = ""
            # for entity in doc.ents:
            #     if entity.label_ == 'GPE':
            #         loc += entity.text + " "
            # if len(loc) >0:
            #     print(loc)

        # Nisei male. April 30, 1902
        else:
            birthday = bio.split()
            if len(birthday) >2:
                if birthday[2] in months:
                    if birthday[3][:-1].isdigit():
                        if birthday[4][:4].isdigit():
                            birthday_str = birthday[4][:4]
                            ct +=1


        data.append([row[0], row[1], row[2], birthday_str, loc])

    headers = ["id", "Narrator", "Bio", "Birthday", "Birthplace"]

    # Create a DataFrame
    df = pd.DataFrame(data, columns=headers)
    df.to_csv("bios_backup.csv", index=False)

    print("CSV file with headers written successfully!")
    print(ct)
    print(ct2)
            # birthday_start = bio.lower().index("born") + 4
            # demographic = bio[:birthday_start]
            # birthday = bio[birthday_start:].split()
            #
            # # born November 30, 1921
            # if birthday[3][:-1].isnumeric():
            #     birthday_end = bio.index(birthday[3][:-1]) + 4
            #     #print(bio[birthday_start+5:birthday_end])
            #     ct+=1
            #     place = ""
            #     if birthday[4] =="in":
            #         ct2+=1
            #         if "," in birthday[5]:
            #             place = birthday[5] + " " + birthday[6]
            #         elif  "," in birthday[6]:
            #             place = birthday[5] + " " + birthday[6] + " " + birthday[7]
            #         else:
            #             place = birthday[5]
            #         #print(bio[birthday_start+5:birthday_end] + " " +  place)
            #         print(birthday, place)
            # # born 1918
            # elif birthday[1][:-1].isnumeric():
            #     birthday_end = bio.index(birthday[1][:-1]) + 4
            #     #print(bio[:50])
            #     if birthday[2] =="in":
            #         ct2+=1
            #         if "," in birthday[3]:
            #             place = birthday[3] + " " + birthday[4]
            #         elif  "," in birthday[4]:
            #             place = birthday[3] + " " + birthday[4] + " " + birthday[5]
            #         else:
            #             print("weird case: ", bio[:40])
            #             place = birthday[4]
            #             if place == "During":
            #                 place=birthday[3]
            #
            #     #print(place)

            # # born in 1927, born in 1927
            # elif birthday[2].isnumeric():
            #     birthday_end = bio.index(birthday[2]) + 4
            #     #print(bio[birthday_end-4:birthday_end])
            #     ct += 1
            #     #print(bio[:50])


                # if not birthday_end:
                #     print(bio[:50])
                # else:
                #     print(bio[birthday_start:birthday_end])
                #print(bio[birthday_end+4:birthday_end+12])
                #ct2+=1
                # born 1918
                # elif birthday[2][:-1].isnumeric():
                #     birthday_end = bio.index(birthday[1][:-1]) + 4
                #     print(bio[birthday_start + 5:birthday_end])
                #     ct += 1

                # else:
                #     if bio[birthday_start:30]:
                #         print(bio[birthday_start:30])
                #     else:
                #         print("Nothing for bio" + str(bio[0:40]))
                #     ct2+=1
            #else:
                # print("No birthday in bio for: ", row[1], bio[:30])
    #print(ct)
    #print(ct2)