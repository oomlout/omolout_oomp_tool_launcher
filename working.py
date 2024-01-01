import oom_kicad
import oom_markdown
import os
import yaml

# to exe
# auto-py-to-exe


#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    #place_parts(**kwargs)
    #make_readme(**kwargs)
    #get part input
    content = input("part_id: ").lower()
    part_id = oomp_parts_id.get(content, "")
    if part_id == "":
        #check for md5
        part_id = oomp_parts_md5_6.get(content, "")
    if part_id == "":
        #check for md5
        part_id = oomp_parts_md5_6_alpha.get(content, "")
    if part_id == "":
        #check for md5
        part_id = oomp_parts_oomlout_short_code.get(content, "")
    if part_id != "":
        directory_part_base = "C:/gh/oomlout_oomp_current_version/parts"
        directory_part = f"{directory_part_base}/{part_id}"
        directory_part = directory_part.replace("/","\\")
        #open in explorer using os
        print(f"opening {directory_part}")
        os.system(f"explorer {directory_part}")
    else:
        print("not found")
    

def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)
    
#take component positions from working_parts.csv and place them in working.kicad_pcb
def place_parts(**kwargs):
    board_file = "kicad/current_version/working/working.kicad_pcb"
    parts_file = "working_parts.csv"
    #load csv file
    import csv
    with open(parts_file, 'r') as f:
        reader = csv.DictReader(f)
        parts = [row for row in reader]


    
    oom_kicad.kicad_set_components(board_file=board_file, parts=parts, corel_pos=True, **kwargs)




def load_parts(**kwargs):
    load_parts_force = kwargs.get("load_parts_force", False)
    global oomp_parts
    directory_parts = "C:/gh/oomlout_oomp_current_version/parts"
    pickle_file = "tmp/parts.pickle"
    if os.path.exists(pickle_file) and not load_parts_force:
        import pickle
        with open(pickle_file, "rb") as infile:
            oomp_parts = pickle.load(infile)
    else:
        #get all files called working.yaml using glob
        print("loading parts from yaml")
        import glob
        files = glob.glob(f"{directory_parts}/**/working.yaml", recursive=True)
        count = 0
        for file in files:
            #load yaml
            with open(file, "r") as infile:
                #print a dot
                count += 1
                part = yaml.load(infile, Loader=yaml.FullLoader)
                if part != None:
                    oomp_parts[part["id"]] = part
            #every 1000 print a dot
            if count % 100 == 0:
                print(".", end="", flush=True)
        #save to pickle
        import pickle
        #make directroies
        os.makedirs(os.path.dirname(pickle_file), exist_ok=True)        
        with open(pickle_file, "wb") as outfile:
            pickle.dump(oomp_parts, outfile)
        #make a dictionary of id's
    print("making indexes")
    for part_id in oomp_parts:        
        oomp_parts_id[part_id] = part_id
        part = oomp_parts[part_id]
        #make a dictionary of md5's
        md5 = part["md5_6"]
        oomp_parts_md5_6[md5] = part_id
        #make a dictionary of md5's
        md5 = part["md5_6_alpha"]
        oomp_parts_md5_6_alpha[md5] = part_id
        #make a dictionary of short_codes
        short_code = part.get("oomlout_short_code","")
        if short_code != "":
            oomp_parts_oomlout_short_code[short_code] = part_id
    pass 

oomp_parts = {}
oomp_parts_id = {}
oomp_parts_md5_6 = {}
oomp_parts_md5_6_alpha = {}
oomp_parts_oomlout_short_code = {}

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=1112, debug=True, threaded=True)
    kwargs = {}
    kwargs["load_parts_force"] = False
    load_parts(**kwargs)
    main(**kwargs)