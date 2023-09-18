# windows
# call in bash
import sys,os,json,re,argparse

# relative to report/
pic_folder_path = './md_pic_f'
cfg_path = './md_pic_f/pic_cfg.json'
change_files_flag = False


# find folders with png,whose md files are set as target files
# check recursively in report/
def get_target_md_files(folder_path):
    target_files_list = []
    with os.scandir(folder_path) as i:
        for entry in i:
            if entry.is_file():
                if entry.name[-3:] == '.md':
                    target_files_list.append(os.path.join(folder_path,entry.name))
    return target_files_list
    

# match and get old pic path list
def get_path(content)->list:
    pattern = r'![[].*?[]]\((.+?)\)' 
    matches = re.findall(pattern,content)

#    delete repetitive items
    s_matches  =[]
    for match in matches:
        if match in s_matches:
            pass
        else:
            s_matches.append(match)
#    print(matches)
    return s_matches

def get_cfg()->int:
    # pf_path = './'
    cnt_filename_number = 0
    # open pic_cfg.json
    
    # if json exits
    with open(cfg_path,'r') as fp:
        json_con = fp.read()
        json_dict = json.loads(json_con)
        cnt_filename_number = json_dict["latest_av_num"]
        pass
    # parse json,get start count number

    return cnt_filename_number 

def update_json(this_n):
    with open(cfg_path,'w') as fp:
        j_dict = {"latest_av_num":this_n}
        con = json.dumps(j_dict)
        fp.write(con)

def find_folders(path)->list:
    # run in report/
    folders = []
    with os.scandir(path) as i:
        for entry in i:
            if entry.is_dir():
                # print(entry.name)
                folders.append(os.path.join(path,entry.name))
    if folders!=[]:
        for i in folders:
            tf = find_folders(i)
            if tf!=[]:
                folders+=tf
    return folders
    # with os.scandir('.') as i:
    #     for entry in i:
    #         if entry.is_file():
    #             print(entry.name)


# get file names(abs path) and update it
def update_md(md_file_name):
    folder_abs_path = os.path.dirname(md_file_name)

    with open(md_file_name,'r+',encoding='utf-8') as fp:
        content = fp.read()

        all_pic_link_list = get_path(content)
        # print('all pic link found in target file:{}'.format(md_file_name))
        # print(all_pic_link_list)
        pic_link_list = []
        # 加入一个判断机制，只有这个图片链接能在找到对应图片，才加入pic_link_list
        for link in all_pic_link_list:
            # 有sorted，就说明是整理过的
            if 'sorted' in link:
                pass
            else:
                # 没有sorted，可能是需要处理的image
                pic_path = os.path.join(folder_abs_path,link)
                if os.path.exists(pic_path) == True:
                    pic_link_list.append(pic_path)

        new_link_list = []
        if pic_link_list != []:
            print('those pictures in {} need to be processed : '.format(md_file_name),end='')
            print(pic_link_list)
        if pic_link_list == []:
            pass
        else:
            this_n = get_cfg()

            for pic in pic_link_list:
                # this_pic_source_path_name = os.path.join(folder_abs_path,pic)
                this_pic_source_path_name = pic

                this_flie_name = 'sorted_'+str(this_n)+'.png' # file catagory determine,all png now
                this_pic_target_path_name = os.path.join(pic_folder_path,this_flie_name)

                new_file_name = os.path.relpath(this_pic_target_path_name,folder_abs_path)
                new_file_name = new_file_name.replace('\\','/')
                new_link_list.append(new_file_name)
                # print(start_n)
                if change_files_flag:
                    os.system('mv {} {}'.format(this_pic_source_path_name,this_pic_target_path_name))
                this_n += 1
            if change_files_flag:
                update_json(this_n)


    old_pic_filenames = []
    for pathname in pic_link_list:
        last_special_char_i = 0
        for i in range(len(pathname)):
            if pathname[i] == '\\' or pathname[i] == '/':
                last_special_char_i = i
        old_pic_filenames.append(pathname[last_special_char_i+1:])


    if change_files_flag:
        with open(md_file_name,'r+',encoding='utf-8') as fp:
            con = fp.read()
            # for i,j in new_link_list,pic_link_list:
            #     con = con.replace(j,i)
            for i in range(len(new_link_list)):
                    con = con.replace(old_pic_filenames[i],new_link_list[i])
            fp.seek(0)
            fp.write(con)
            fp.truncate()

def need_to_sort(path)->bool:
    filelist = []
    with os.scandir(path) as i:
        for entry in i:
            if entry.is_file():
                # print(entry.name)
                filelist.append(entry.name)
    # print(filelist)
    file_suf_list = []
    for file in filelist:
        if file[-3:] in file_suf_list:
            pass
        else:
            file_suf_list.append(file[-3:])
    # print(file_suf_list)
    if '.md' in file_suf_list and 'png' in file_suf_list:
        return True
    return False

debug_flag = 0 
if __name__ == "__main__" and debug_flag != 1:

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--change',action='store_true',help='change files if this is set')
    args = parser.parse_args()

    if args.change == True:
        change_files_flag = 1
    else:
        change_files_flag = 0
        print('''
              ======================================
                    won\'t do anything on files
              ======================================''')

    # 运行时目录为report
    os.chdir('C:/Users/孙国珩/iCloudDrive/iCloud~md~obsidian/reports')
    # print(os.getcwd())

    # 先找到所有的子文件夹
    folders = []
    folders = find_folders('.')
    folders.append('./')
    target_folder_list = []
    # print('find in folders:{}'.format(folders))
    # print('set folder(s) as target : ')
    for folder in folders:
        # 找出所有md png共存文件夹，得到目标文件夹列表
        if need_to_sort(folder)==True:
            print(folder)
            target_folder_list.append(folder)
    if target_folder_list == []:
        print('all clean')
    else:
        print('^^^^^^^^^^^^^^^ target folder(s) ^^^^^^^^^^^^^^^^^^^^^')

    for target_folder in target_folder_list:
        # 找出需要修改的md文件
        md_target_file_list = get_target_md_files(target_folder)
        # print(md_target_file_list)
        for file_i in md_target_file_list:
            # 更新目标文件 
            update_md(file_i)
    

if debug_flag == 1:
    # 运行时目录为report
    pass