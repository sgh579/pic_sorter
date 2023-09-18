import re,os

class md_s:
    def __init__(self, abspath = None, relpath = None) -> None:
        self.abspath = abspath
        self.filename = os.path.split(self.abspath)[-1]
        self.parent_folder =  os.path.split(self.abspath)[0]

        self.con = ''
        self.get_con()

        self.all_pic_links_list = []
        self.sorted_pic_links_list = []
        self.raw_pic_links_list = []
        self.unique_raw_pic_links_list = []
        self.unique_sorted_pic_links_list = []
        self.unique_sorted_pic_names_list = []

        self.valid_raw_pic_links_list = []
        self.broken_pic_links_list = []
        
        self.need_to_sort = False
    def get_con(self):
        with open(self.abspath,'r',encoding='utf-8') as fp:
            self.con = fp.read()

    def replace_links(self,sorted_filelist_relative_path):
        for i in range(len(self.valid_raw_pic_links_list)):
            self.con = self.con.replace(self.valid_raw_pic_links_list[i],sorted_filelist_relative_path[i])

        # write
        with open(self.abspath,'w',encoding='utf-8') as fp:
            fp.write(self.con)

    def debug(self):
        print(self.abspath)
        print(self.con)
        print('all')
        print(self.all_pic_links_list)
        print('all sorted')

        print(self.sorted_pic_links_list)
        print('un sorted')
        print(self.unique_sorted_pic_links_list)
        print('all raw')
        print(self.raw_pic_links_list)
        print('un raw')
        print(self.unique_raw_pic_links_list)
        print('valid piclinks {}'.format(self.valid_raw_pic_links_list))
        print('state need to sort : {}'.format(self.need_to_sort))
        print('broken: {}'.format(self.broken_pic_links_list))

    def update_state(self):
        # print('update') 
        if self.all_pic_links_list == [] or self.unique_raw_pic_links_list == []:
            self.need_to_sort = False
            # print('because of null')
        
        # print('uniq raw pic links:{}'.format(self.unique_raw_pic_links_list))
        for link in self.unique_raw_pic_links_list:
            if os.path.exists(os.path.join(self.parent_folder,link)):
                self.valid_raw_pic_links_list.append(link)

        for link in self.all_pic_links_list:
            if not os.path.exists(link):
                self.broken_pic_links_list.append(link)

        self.broken_pic_links_list = list(set(self.broken_pic_links_list))
            
        if self.valid_raw_pic_links_list != []:
            self.need_to_sort = True
        else:
            self.need_to_sort = False
            # print('no valid pic links')


        
# affect some memberlist variables
# all_pic_links_list 
# sorted_pic_links_list
# raw_pic_links_list
# unique_sorted_pic_links_list
    def get_pic_links(self):
        l_all_pic_links_list = []
        pattern = r'![[].*?[]]\((.+?)\)' 
        matches = re.findall(pattern,self.con)
        l_all_pic_links_list += matches
        self.all_pic_links_list = l_all_pic_links_list

        for link in self.all_pic_links_list:
            if 'sorted' in link:
                self.sorted_pic_links_list.append(link)
            else:
                self.raw_pic_links_list.append(link)

        for link in self.sorted_pic_links_list:
            if link not in self.unique_sorted_pic_links_list:
                self.unique_sorted_pic_links_list.append(link)

        for link in self.raw_pic_links_list:
            if link not in self.unique_raw_pic_links_list:
                self.unique_raw_pic_links_list.append(link)

        for link in self.unique_sorted_pic_links_list:
            name_start = 0
            i = 0
            for char in link:
                if char == '/' or char == '\\':
                    name_start = i+1
                i+=1

            self.unique_sorted_pic_names_list.append(link[name_start:])

        


if __name__ == '__main__':
    mds = md_s('C:/Users/孙国珩/Desktop/myThings/dev/pic_sorter/debug.md')
    mds.get_pic_links()
    mds.update_state()
    mds.debug()