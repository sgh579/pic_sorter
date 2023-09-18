
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


    else:
        print('no cfg,exit')
        exit(0)

    print(args.zip_files)
  

