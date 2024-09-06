import os
import json
import urllib.request
import shutil
import uuid
import argparse

def generate_manifest(root_path, replace_files, append_guid):
    # original code by @castierook in the AstroDX Discord Server
    def generate_guid():
        return str(uuid.uuid4())

    def create_manifest(directory, sub_dirs):
        manifest = {
            "name": os.path.basename(directory), 
            "id": None,
            "serverUrl": None,
            "levelIds": sub_dirs
        }
        return manifest

    def process_directories(path, replace_files=False, append_guid=False):
        root_dir = os.path.abspath(path)  # Use the specified path
        output_dir = os.path.join(root_dir, 'output')
        collections_dir = os.path.join(output_dir, 'collections')
        levels_dir = os.path.join(output_dir, 'levels')

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(collections_dir)
        os.makedirs(levels_dir)

        for root, dirs, files in os.walk(root_dir):
            if root == root_dir or output_dir in root:
                continue

            relative_root = os.path.relpath(root, root_dir)
            if os.path.basename(relative_root) == "output":
                continue

            sub_dirs = []
            for dir_name in dirs:
                if append_guid:
                    new_dir_name = f"{dir_name}-{generate_guid()}"
                    sub_dirs.append(new_dir_name)
                else:
                    sub_dirs.append(dir_name)

            manifest = create_manifest(root, sub_dirs)
            manifest_path = os.path.join(collections_dir, relative_root, 'manifest.json')
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

            for original_dir_name, dir_name in zip(dirs, sub_dirs):
                src_dir = os.path.join(root, original_dir_name)
                dst_dir = os.path.join(levels_dir, dir_name)
                if replace_files:
                    shutil.move(src_dir, dst_dir)
                else:
                    shutil.copytree(src_dir, dst_dir)

            if replace_files:
                shutil.rmtree(root)

            dirs.clear()  # prevent descending into subdirectories
    process_directories(root_path, replace_files, append_guid)
    # Example usage:
    # process_directories('/path/to/directory', replace_files=True, append_guid=True)

def unknownHandler(title_value, folder_path, catcode):
    chosen = False
    print(f"unable to determine genre for {title_value} in {folder_path}")
    while not chosen:
        print("Choices:")
        print("[1] Copy to unidentified folder")
        print("[2] Choose Manually")
        print("[3] Log to unidentifiedCharts.txt and Ignore")

        choice = str(input("Enter the number of your choice: "))
        match choice:
            case "1":
                chosen = True
                os.makedirs(root_path + "/levels/Unidentified/" + os.path.basename(folder_path), exist_ok=True)
                try:
                    shutil.copytree(folder_path, root_path + "/levels/Unidentified/" + os.path.basename(folder_path), dirs_exist_ok=True)
                except:
                    print(f"Error: Copy failed: {folder_path}")
                    debugging.write(f"Error: Copy failed: {folder_path} to Output folder\n")
                print(f"copied to output: {folder_path}")
                
            case "2":
                chosen = True
                print("Choices:")
                print(f"[1] {catcode[0]}")
                print(f"[2] {catcode[1]}")
                print(f"[3] {catcode[2]}")
                print(f"[4] {catcode[3]}")
                print(f"[5] {catcode[4]}")
                print(f"[6] {catcode[5]}")
                print(f"[7] {catcode[6]}")
                print(f"[8] {catcode[7]}")
                print(f"[9] {catcode[8]}")
                manualChosen = False
                while not manualChosen:
                    manualChoice = str(input("Enter the number of your choice: "))
                    if manualChoice in ["1","2","3","4","5","6","7","8","9"]:
                        os.makedirs(root_path + "/levels/" + catcode[int(manualChoice)-1] + "/" + os.path.basename(folder_path), exist_ok=True)
                        try:
                            shutil.copytree(folder_path, root_path + "/levels/" + catcode[int(manualChoice)-1] + "/" + os.path.basename(folder_path), dirs_exist_ok=True)
                        except:
                            print(f"Error: Copy failed: {folder_path}")
                            debugging.write(f"Error: Copy failed: {folder_path} to Output folder\n")
                        print(f"copied to output: {folder_path}")
                        manualChosen = True
                    else:
                        print("Invalid choice, please try again")
                        manualChosen = False
                        continue
            case "3":
                chosen = True
                print(f"IGNORED: {title_value} in {folder_path}")
                unidentifiedChartsDebug.write(f"IGNORED: {title_value} in {folder_path}\n")
                
            case "_":
                print("Invalid choice, please try again")
                chosen = False
                continue

def parse_JSON_Database():
    try:
        response = urllib.request.urlopen(maimai_JP_songlist_URL)
        if response.status == 200:
            maimaiSongInfoJSON = json.loads(response.read())
        else:
            print(f"Failed to fetch data, status code: {response.status}")
            print("loading from local database")
            maimaiSongInfoJSON = json.load(open("maimai_songs.json"))
    except Exception as e:
        print(f"Error fetching or parsing JSON: {e}")
        maimaiSongInfoJSON = []

    try:
        response = urllib.request.urlopen(zerataku_maimai_songlist_URL)
        if response.status == 200:
            zerataku_maimai_songlist_JSON = json.loads(response.read())
        else:
            print(f"Failed to fetch data, status code: {response.status}")
            print("loading from local database")
            zerataku_maimai_songlist_JSON = json.load(open("zerataku_maimai_songlist.json"))
    except Exception as e:
        print(f"Error fetching or parsing JSON: {e}")
        zerataku_maimai_songlist_JSON = []

    try:
        response = urllib.request.urlopen(manualCheckURL)
        if response.status == 200:
            manualCheckJSON = json.loads(response.read())
        else:
            print(f"Failed to fetch data, status code: {response.status}")
            print("loading from local database")
            manualCheckJSON = json.load(open("manualCheck.json"))
    except Exception as e:
        print(f"Error fetching or parsing JSON: {e}")
        manualCheckJSON = []

    for item in maimaiSongInfoJSON:
        if item.get('catcode') == 'maimai':
            maimai.append(item.get('title'))
        elif item.get('catcode') == 'POPS＆アニメ':
            popAndAnime.append(item.get('title'))
        elif item.get('catcode') == 'ゲーム＆バラエティ':
            gameAndVariety.append(item.get('title'))
        elif item.get('catcode') == '東方Project':
            touhouProject.append(item.get('title'))
        elif item.get('catcode') == 'niconico＆ボーカロイド':
            niconicoAndVocaloid.append(item.get('title'))
        elif item.get('catcode') == 'オンゲキ＆CHUNITHM':
            ongekiAndChunithm.append(item.get('title'))
        else:
            print(f"Unknown catcode: {item.get('catcode')}\n Title: {item.get('title')}")

    return maimaiSongInfoJSON, zerataku_maimai_songlist_JSON, manualCheckJSON


def parse_maidata(filepath):
    lv_7_value = None
    title_value = None
    
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        for line in file:
            if line.startswith("&title="):
                title_value = line.strip().split('=')[1]
                if not title_value:  # If title is somehow empty
                    print(f"Warning: Title is empty in file {filepath}")
            elif line.startswith("&lv_7="):
                lv_7_value = line.strip().split('=')[1]
    
    return lv_7_value, title_value

def check_only_folders(root_path,maimaiSongInfoJSON,manualCheckJSON):
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"&title:\t\t{title_value}")

                if lv_7_value:
                    print(f"matched to in maimaiJSON: \tutage")

                elif title_value in popAndAnime or folder in popAndAnime:
                    print(f"matched to maimaiJSON: \tpop and anime")

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    print(f"matched to maimaiJSON: \tniconico and vocaloid")

                elif title_value in touhouProject or folder in touhouProject:
                    print(f"matched to maimaiJSON: \ttouhou project")

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    print(f"matched to maimaiJSON: \tgame and variety")

                elif title_value in maimai or folder in maimai:
                    print(f"matched to maimaiJSON: \tmaimai")
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    print(f"matched to maimaiJSON: \tongeki and chunithm")
                
                else:
                    if title_value in manualCheckJSON:
                        if manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"matched to manualCheckJSON: \tpop and anime")

                        elif manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"matched to manualCheckJSON: \tniconico and vocaloid")

                        elif manualCheckJSON[title_value] == "東方Project":
                            print(f"matched to manualCheckJSON: \ttouhou project")

                        elif manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"matched to manualCheckJSON: \tgame and variety")

                        elif manualCheckJSON[title_value] == "maimai":
                            print(f"matched to manualCheckJSON: \tmaimai")

                        elif manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print(f"matched to manualCheckJSON: \tongeki and chunithm")

                        elif manualCheckJSON[title_value] == "中国流行乐":
                            print(f"matched to manualCheckJSON: \tchinese pop")

                        elif manualCheckJSON[title_value] == "宴会場":
                            print(f"matched to manualCheckJSON: \tutage")

                        else:
                            print(f"{title_value} found in manual check, value empty, @venb304 please update manualCheck.json")
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                        else:
                            print(f"No title found, Unidentified genre in {folder_path}")
                
            else:
                print(f"{folder_path} is empty, moving on")

def proces_toGenre(root_path, maimaiSongInfoJSON, manualCheckJSON, catcode):
    savedFolderPaths = [[],[],[],[],[],[],[],[],[]]
    
    if os.path.isdir(root_path + "/levels/"):
        if not os.listdir(root_path + "/levels/"):
            print(f"{root_path}/levels/ is empty")
        else:
            print(f"{root_path}/levels/ is not empty")
            print(f"deleting {root_path}/levels/")
            shutil.rmtree(root_path + "/levels/")
            # modify to say a different folder name instead of /levels at line 374

    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            maidata_path = os.path.join(folder_path, 'maidata.txt')
            
            if os.path.isfile(maidata_path):
                lv_7_value, title_value = parse_maidata(maidata_path)
                print(f"Folder: {folder_path}")
                
                if lv_7_value:
                    print(f"{title_value} has utage difficulty | matched to in maimaiJSON: utage")
                    savedFolderPaths[6].append(folder_path)

                elif title_value in popAndAnime or folder in popAndAnime:
                    print(f"{title_value} matched to maimaiJSON: pop and anime")
                    savedFolderPaths[0].append(folder_path)

                elif title_value in niconicoAndVocaloid or folder in niconicoAndVocaloid:
                    print(f"{title_value} matched to maimaiJSON: niconico and vocaloid")
                    savedFolderPaths[1].append(folder_path)

                elif title_value in touhouProject or folder in touhouProject:
                    print(f"{title_value} matched to maimaiJSON: touhou project")
                    savedFolderPaths[2].append(folder_path)

                elif title_value in gameAndVariety or folder in gameAndVariety:
                    print(f"{title_value} matched to maimaiJSON: game and variety")
                    savedFolderPaths[3].append(folder_path)

                elif title_value in maimai or folder in maimai:
                    print(f"{title_value} matched to maimaiJSON: maimai")
                    savedFolderPaths[4].append(folder_path)
                
                elif title_value in ongekiAndChunithm or folder in ongekiAndChunithm:
                    print(f"{title_value} matched to maimaiJSON: ongeki and chunithm")
                    savedFolderPaths[5].append(folder_path)
                
                else:
                    if title_value in manualCheckJSON:
                        if manualCheckJSON[title_value] == "POPS＆アニメ":
                            print(f"{title_value} matched to manualCheckJSON: pop and anime")
                            savedFolderPaths[0].append(folder_path)

                        elif manualCheckJSON[title_value] == "niconico＆ボーカロイド":
                            print(f"{title_value} matched to manualCheckJSON: niconico and vocaloid")
                            savedFolderPaths[1].append(folder_path)

                        elif manualCheckJSON[title_value] == "東方Project":
                            print(f"{title_value} matched to manualCheckJSON: touhou project")
                            savedFolderPaths[2].append(folder_path)

                        elif manualCheckJSON[title_value] == "ゲーム＆バラエティ":
                            print(f"{title_value} matched to manualCheckJSON: game and variety")
                            savedFolderPaths[3].append(folder_path)

                        elif manualCheckJSON[title_value] == "maimai":
                            print("title matched in manual check: maimai list")
                            savedFolderPaths[4].append(folder_path)

                        elif manualCheckJSON[title_value] == "オンゲキ＆CHUNITHM":
                            print("title matched in manual check: ongeki and chunithm list")
                            savedFolderPaths[5].append(folder_path)

                        elif manualCheckJSON[title_value] == "中国流行乐":
                            print("title matched in manual check: chinese pop list")
                            savedFolderPaths[7].append(folder_path)

                        elif manualCheckJSON[title_value] == "宴会場":
                            print("title matched in manual check: utage list")
                            savedFolderPaths[6].append(folder_path)

                        else:
                            print(title_value + " found in manual check, value empty, @venb304 please update manualCheck.json")
                    else:
                        if title_value:
                            print(title_value + " not match, Unidentified genre")
                        else:
                            print("No title found, Unidentified genre") 
                        
                        savedFolderPaths[8].append(folder_path)
            else:
                print(f"{folder_path} is empty, moving on")

    for category in savedFolderPaths:
        match savedFolderPaths.index(category):
            case 0:
                print("\ncurrent category: pop and anime\n")
            case 1:
                print("\ncurrent category: niconico and vocaloid\n")
            case 2:
                print("\ncurrent category: touhou project\n")
            case 3:
                print("\ncurrent category: game and variety\n")
            case 4:
                print("\ncurrent category: maimai\n")
            case 5:
                print("\ncurrent category: ongeki and chunithm\n")
            case 6:
                print("\ncurrent category: utage\n")
            case 7:
                print("\ncurrent category: chinese pop\n")
            case 8:
                print("\ncurrent category: unidentified\n")
            case _:
                print("\ncurrent category: how? there should not be another category, how did this return to 8\n")
        
        for savedPaths in category:
            if savedFolderPaths.index(category) == 8:
                unknownHandler(os.path.basename(savedPaths), savedPaths, catcode)
                continue
            else:
                os.makedirs(root_path + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), exist_ok=True)
                try:
                    shutil.copytree(savedPaths, root_path + catcode[savedFolderPaths.index(category)] + "/" + os.path.basename(savedPaths), dirs_exist_ok=True)
                except:
                    print(f"Error: Copy failed: {savedPaths}")
                    debugging.write(f"Error: Copy failed: {savedPaths} to Output folder\n")
                print(f"copied to {catcode[savedFolderPaths.index(category)]}: {savedPaths}")

                # removed the creation of the levels folder and instead creates the genre folders in the root path
                # unfortunately, the original charts do still exist as this program just copies them to the genre folders
                # the original charts are not deleted
                # implement a way to first have program un-nest the folders first, 
                #   then create backup collection.json files to be used for reverting changes
                # either to generate it first using the function generate_manifest 
                #   or use the data.json from zerataku's database of maimai songs to organize them as 
                #   necesseary by version again as a way to revert back after organizing by genre

        

# Start of the program
os.makedirs("logging", exist_ok=True)
debugging = open("logging/debugging.txt","w", encoding="utf-8-sig")
unidentifiedChartsDebug = open("logging/unidentifiedCharts.txt","w", encoding="utf-8-sig")

popAndAnime = []
niconicoAndVocaloid = []
touhouProject = []
gameAndVariety = []
maimai = []
ongekiAndChunithm = []
catcode = [["POPS＆アニメ", "niconico＆ボーカロイド", "東方Project", "ゲーム＆バラエティ", "maimai", "オンゲキ＆CHUNITHM", "宴会場", "中国流行乐","UNIDENTIFEIED"],["POPS ＆ ANIME", "niconico＆VOCALOID", "TOUHOU Project", "GAME ＆ VARIETY", "maimai", "ONGKEI ＆ CHUNITHM", "UTAGE", "CHINESE-POP","UNIDENTIFIED"]]
maimaiSongInfoJSON = []
manualCheckJSON = []

manualCheckURL = "https://raw.githubusercontent.com/VenB304/AstroDX-Collection-Genre-Reorganizer/main/manualCheck.json"
zerataku_maimai_songlist_URL = ""
maimai_JP_songlist_URL = "https://maimai.sega.jp/data/maimai_songs.json"

maimaiSongInfoJSON, zerataku_maimai_songlist_JSON, manualCheckJSON = parse_JSON_Database()


running = True

while running:
    print("\nMenu\n")
    print("[1] Check folders only for GENRE grouping (check if your copied path is correct)")
    print("[2] Check folders for GENRE grouping and copy to Output folder")
    print("[3] Generate collection.json files")
    # list of what i wanna do now
    # 1. Perform CHeck: check folders only for genre grouping and displays the genre it belongs to
    # 2. Perform organize into Genre: checks and takes a list matched and unidentified folders, copies the content of matched folders to genre folders, and user can choose what to do with unidentified folders
    # 2.1 also implement to copy or to move the files to the genre folders and makes it so that the will be unnested
    # 3. Restructure Collection: generate collection.json files and unnests the folders from path to be used for newer beta 2.0 of AstroDX
    # 4. Restructure Collection for pre beta: reads collection.json files and restructures the folders to be nested for pre beta versions of AstroDX(ehem, apple devices hehe[this could become outdated as fumi might update for apple deviced any time now])
    # 5. backup: use generate_manifest to create a backup of the current collection and to be used to revert back to the original collections
    # 6. restore: use the backup collection.json files to revert back to the original collections

    print("[0] Exit")

    choice = str(input("Enter the number you wanna do: "))

    match choice:
        case "1":
            print("Checking folders only for GENRE grouping")
            print("this will not copy to levels folder")
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            root_path = input("Enter the root directory path: ").strip()
            check_only_folders(root_path,maimaiSongInfoJSON,manualCheckJSON)
        case "2":
            print("Checking folders for GENRE grouping and copy to Output folder")
            print("this will copy to levels folder within the same root directory/path you input")
            print("Sample path: C:/Users/username/Downloads/maisquared/")
            print("inside the maisquared folder, there should be folders with maidata.txt files")
            print("this will generate a new folder called 'levels'")
            print("after the program is finished, inside the levels folder there should be genre folders like pop and anime, niconico and vocaloid, etc.")
            root_path = input("Enter the root directory path: ").strip()
            langChosen = False
            while not langChosen:
                print("\nJapanese or English Collection Name:")
                print("[0] Japanese Collection Name")
                print("[1] English Collection Name")
                catLang = str(input("Enter choice: ")).strip()
                if catLang in ["0","1"]:
                    langChosen = True
                else:
                    print("Invalid choice, please try again")
                    langChosen = False
                    continue
            proces_toGenre(root_path,maimaiSongInfoJSON,manualCheckJSON,catcode[int(catLang)])
        case "3":
            print("Generating collection.json files")
            print("this will generate collection.json files in the levels folder of a path")
            print("Sample root path: C:/Users/username/Downloads/maisquared/levels")
            print("inside the levels folder or any folder, there should be genre folders like pop and anime, niconico and vocaloid, etc.")
            

            root_path = input("Enter the root directory path: ").strip()
            replace_files = input("Move files in levels folder to output? this will move them instead of copy only(y/n): ").strip()
            append_guid = input("Append GUID to folder names? (y/n): ").strip()

            if replace_files == "y":
                replace_files = True
            else:
                replace_files = False

            if append_guid == "y":
                append_guid = True
            else:
                append_guid = False

            generate_manifest(root_path, replace_files, append_guid)

            print(f"collection.json files generated in {root_path}/output")
        case "0":
            print("Exiting program")
            debugging.close()
            unidentifiedChartsDebug.close()

            running = False
        case _:
            print("Invalid choice, please try again")
            continue