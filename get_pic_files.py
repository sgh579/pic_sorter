import md_s,os


target_file_path = 'C:/Users/孙国珩/iCloudDrive/iCloud~md~obsidian/reports/W9/VIVADO使用总结-1.md'
image_folder = 'C:/Users/孙国珩/Desktop/myThings/dev/pic_sorter/images'
if __name__ == '__main__':


    os.chdir(image_folder)

    mds = md_s.md_s(abspath=target_file_path)
    mds.get_pic_links()
    pic_lick_list = mds.unique_sorted_pic_links_list
    print(pic_lick_list)
    realpath_pic_list = []
    for link in pic_lick_list:
        realpath_pic_list.append(os.path.join(mds.parent_folder,link))

    # print(realpath_pic_list)

    # # cp pics
    # for pic in realpath_pic_list:
    #     os.system(f'cp {pic} {image_folder}')

    # cp md
    # with open(mds.filename,'w') as fp:
    #     con = mds.con
    #     con

    