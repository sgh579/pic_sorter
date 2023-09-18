
import re,argparse,os,json,md_s,rep_s

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--change',action='store_true',help='change files if this is set')
    parser.add_argument('-z','--zip_files',action='store',help='input name of the md filezip md file and necessary picture into a folder')
    args = parser.parse_args()


    j_dict = {}

    if os.path.exists('./sort_cfg.json') == True:
        print('cfg exists')
        with open('./sort_cfg.json','r',encoding='utf-8') as fp:
            j_con = fp.read()
            j_dict = json.loads(j_con)

        print(j_dict)



    else:
        print('no cfg,exit')
        exit(0)

    print(args.zip_files)
  

