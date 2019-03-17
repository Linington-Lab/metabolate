from .core import *


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path',help='path to input for either task or basketed data for activity mapping')
    parser.add_argument('task',help='task to perform.',choices=['replicate','basket','both','activity','full_pipeline'])
    parser.add_argument('-w','--workers',help="number of parallel workers to spin up",type=int,default=0)
    parser.add_argument('-f','--filename_col',help='column name for the filename',default='Sample')
    parser.add_argument('--basket_info',help='Flag to save basket info as a json object in resulting files.',action='store_true')
    parser.add_argument('--ms2',help='match ms2 ions during basketing Note: Will drastically increase time required',action='store_true')
    parser.add_argument('--activity_data',help='path to activity data or folder containing multiple activity files')
    args = parser.parse_args()

    data_path = Path(args.path)
    if args.task in ['replicate','both','full_pipeline']:
        mp_proc_folder(data_path,FILENAMECOL=args.filename_col,max_workers=args.workers,calc_basket_info=args.basket_info)

    if args.task in ['basket','both','full_pipeline']:
        if args.task == 'both':
            data_path = data_path.joinpath('Replicated')
        else:
            data_path = Path(args.path)
        basket(data_path,args.filename_col,ms2=args.ms2,calc_basket_info=args.basket_info)

    if args.activity_data and args.task not in ('both','basket'):
        print('path argument must be path to basketed data file')
    
    if args.activity_data and args.task in ['activity','full_pipeline']:
        load_and_generate_act_outputs(data_path, args.activity_data)

if __name__ == "__main__":
    main()