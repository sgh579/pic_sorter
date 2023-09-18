
import re,argparse,os,json,md_s,rep_s

if __name__ == '__main__':

    shell = os.environ.get('SHELL')
    if shell:
        print(f'current shell: {shell}\n')
    else:
        print('not right shell\n')
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--change',action='store_true',help='change files if this is set')
    parser.add_argument('-z','--zip_files',action='store',help='input name of the md filezip md file and necessary picture into a folder')
    args = parser.parse_args()


    j_dict = {}

    if os.path.exists('./sort_report.json') == True:
        print('json exists')
        with open('./sort_report.json','r',encoding='utf-8') as fp:
            j_con = fp.read()
            j_dict = json.loads(j_con)

        # print(j_dict)
        print(f'set rep: {j_dict["local_dir"]}\n')

        rep_instance = rep_s.rep_s(select_range=j_dict['range'],change_f=args.change,local_path=j_dict['local_dir'],pic_folder_path=j_dict['md_pic_f_folder'])
        rep_instance.flow()


# zip files


        if args.zip_files != None:
            print('\n=======================zip===============================\n')
            print('you want zip file:')
            print(args.zip_files)
            zip_folder = j_dict['zip_folder']
            print('into')
            print(zip_folder)

            path_list = []
            for path in rep_instance.all_md_abspath:
                if args.zip_files in path:
                    # print(path)
                    path_list.append(path)


            target_file_path = ''
            if path_list == []:
                print('\nnothing found, check your md name')
                exit(0)
            elif len(path_list) == 1:
                target_file_path = path_list[0]
                print('\nyou have no choice,so target is:\n{}'.format(target_file_path))
            else:
                print('\nthis file\'s path maybe ')
                for p in path_list:
                    print(p)

                target_file_path = input('choose one path\n')
                print(f'your choice is {target_file_path}')

                
            mds = md_s.md_s(abspath=target_file_path)
            mds.get_pic_links()
            pic_link_list = mds.unique_sorted_pic_links_list

            real_pic_list = []

            for link in pic_link_list:
                real_pic_list.append(os.path.join(mds.parent_folder,link))

            for pic in real_pic_list:
                os.system(f'cp {pic} {zip_folder}')

            with open(os.path.join(zip_folder,mds.filename),'w',encoding='utf-8') as fp:
                con = mds.con
                for link in mds.unique_sorted_pic_links_list:
                    this_link_name = ''
                    for name in mds.unique_sorted_pic_names_list:
                        if name in link:
                            this_link_name = name
                            break
                    con = con.replace(link,name)
                    print(f'replace {link} to {name}')
                fp.write(con)
            
            print('mds pic names:')
            print(mds.unique_sorted_pic_names_list)
        
  
    else:
        print('no cfg,exit')
        exit(0)


