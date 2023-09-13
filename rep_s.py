import re,argparse,os,json,md_s

local_path = 'C:/Users/孙国珩/Desktop/myThings/dev/pic_sorter/'
pic_folder_path = 'C:/Users/孙国珩/Desktop/myThings/dev/pic_sorter/md_pic_f'
# select_range = 'C:/Users/孙国珩/iCloudDrive/iCloud~md~obsidian/reports/W9'
select_range = local_path

class rep_s:
    # select_range : select checked folders
    # change_f : flag, set False to avoid operations
    def __init__(self,select_range = None,change_f = False,local_path = None, pic_folder_path = None) -> None:
        self.local_path = local_path
        self.pic_folder_path = pic_folder_path
        self.select_range = select_range
        self.change_f = change_f
        self.all_md_abspath = []

        self.pic_cnt = 0
        self.next_pic_cnt = 0
        

        os.chdir(self.local_path)

    def debug(self):
        print('cnt n')
        print(self.pic_cnt)
        print('pwd')
        print(os.getcwd())
        print(f'all md:{self.all_md_abspath}')

    def sort_one_md(self, md_abspath):
        if self.change_f:
            self.get_cfg()
        else:
            self.pic_cnt = self.next_pic_cnt
        # print('this md {}'.format(md_abspath))
        mds = md_s.md_s(abspath = md_abspath)
        mds.get_pic_links()
        mds.update_state()
        if mds.need_to_sort == True:
            # print('this file need to sort : {}'.format(md_abspath))
            # do planning
            sorted_filelist = self.plan_links(mds.valid_raw_pic_links_list)


            
            print(f'''\
{mds.abspath} 
==================================
{mds.valid_raw_pic_links_list}
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
{sorted_filelist}
===================================
\
''')

            # mv
            loop_len = len(sorted_filelist)
            for i in range(loop_len):
                origin_f = os.path.join(mds.parent_folder,mds.valid_raw_pic_links_list[i])
                origin_f = origin_f.replace('\\','/')
                target_f = os.path.join(self.pic_folder_path,sorted_filelist[i])
                if self.change_f == True:
                    os.system(f'mv {origin_f} {target_f}')
                else:
                    print(f'mv {origin_f} {target_f}')

            # update cfg
            
            if self.change_f == True:
                self.update_cfg(self.next_pic_cnt)
            else:
                print(f'cfg change {self.pic_cnt} ===> {self.next_pic_cnt}')

            # replace
            sorted_filelist_rel_p = []
            for i in sorted_filelist:
                pic_abspath = os.path.join(self.pic_folder_path,i)
                sorted_filelist_rel_p.append(os.path.relpath(pic_abspath,mds.parent_folder).replace('\\','/'))

            if self.change_f == True:
                mds.replace_links(sorted_filelist_relative_path=sorted_filelist_rel_p)
            else:
                print('replce links in md:')
                for i in range(len(sorted_filelist_rel_p)):
                    print(f'{mds.valid_raw_pic_links_list[i]} ========>  {sorted_filelist_rel_p[i]}')
        else:
            # print('this file {} won\'t be sorted'.format(md_abspath))
            pass


    def plan_links(self, valid_pic_link_list):
        filename_cnt = self.pic_cnt
        sorted_pic_name_list = []
        for i in valid_pic_link_list:
            sorted_pic_name_list.append('sorted_{}.png'.format(filename_cnt))
            filename_cnt+=1

        self.next_pic_cnt = filename_cnt

        return sorted_pic_name_list


        

    def get_cfg(self)->int:
        cfg_path = os.path.join(self.pic_folder_path,'pic_cfg.json')

        cnt_filename_number = 0
        # open pic_cfg.json
        
        # if json exits
        with open(cfg_path,'r') as fp:
            json_con = fp.read()
            json_dict = json.loads(json_con)
            cnt_filename_number = json_dict["latest_av_num"]
        # parse json,get start count number

        self.pic_cnt = cnt_filename_number
    
    def update_cfg(self,next_n):
        cfg_path = os.path.join(self.pic_folder_path,'pic_cfg.json')
        with open(cfg_path,'w') as fp:
            j_dict = {"latest_av_num":next_n}
            con = json.dumps(j_dict)
            fp.write(con)

    def find_all_markdown(self):
        all_folders_list = self.find_folders(self.select_range)
        # print(all_folders_list)
        all_folders_list.append(self.select_range)
        all_md_path_list = []
        for folder in all_folders_list:
            with os.scandir(folder) as i:
                for entry in i:
                    if '.md' in entry.name:
                        all_md_path_list.append(os.path.join(folder,entry.name))
        self.all_md_abspath = all_md_path_list

    def find_folders(self,path)->list:
        folders = []
        with os.scandir(path) as i:
            for entry in i:
                if entry.is_dir():
                    folders.append(os.path.join(path,entry.name))

        if folders != []:
            for i in folders:
                tf = self.find_folders(i)
                if tf!=[]:
                    folders+=tf

        return folders
    def flow(self):
        self.get_cfg()
        self.next_pic_cnt = self.pic_cnt
        self.find_all_markdown()
        # self.debug()
        for md in self.all_md_abspath:
            self.sort_one_md(md)
        print('flow done')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--change',action='store_true',help='change files if this is set')
    args = parser.parse_args()


    reps = rep_s(select_range= select_range, local_path= local_path, pic_folder_path=pic_folder_path,change_f=args.change)
    reps.flow()
