import datetime
from package.huffmanCoding import HuffmanCoding
from package.myEnum import Mode,Status
import sys
if __name__=='__main__':
    try:
        result = str(sys.argv[1]).split('--')[1]
    except:
        raise Exception('inline argument missing look at the readme.txt documentation')
    if result in Mode.get_values():
        try:
            debug = str(sys.argv[2]).split('--')[1]=='debug'
        except:
            debug=False
        coding = HuffmanCoding(result,debug)
        if(result==Mode.DECODE.value):coding.decode()
        elif(result==Mode.ENCODE.value):coding.encode()
        else:
            try:
                type = str(sys.argv[2]).split('--')[1]
            except:
                data = coding.xml.get_all_data()
            else:
                if not type in ['between_date','mode','status']:
                    raise Exception('you have to use some of the some of the allow parameters look at the readme.txt documentation')
            if type =='between_date':
                try:
                    from_date = str(sys.argv[3])
                    to_date = str(sys.argv[4])
                except:
                    error=True
                finally:
                    if error:
                        raise Exception('you have to call parameter --between_date with two date values look at the readme.txt documentation')
                data = coding.xml.get_data_by_date(from_date,to_date)
            elif type=='status':
                error=False
                try:
                    type = str(sys.argv[3])
                except: 
                    error=True
                finally:
                    if error or not type in [Status.SUCCESS.value,Status.ERROR.value]:
                        raise Exception('you have to call parameter --status with value success or error look at the readme.txt documentation')
                data = coding.xml.get_data_by_status(type)
            elif type=='mode':
                error=False
                try:
                    type = str(sys.argv[3])
                except:
                    error=True
                finally:
                    if error or not type in [Mode.DECODE.value,Mode.ENCODE.value]:
                        raise Exception('you have to call parameter --mode with value encode or decode look at the readme.txt documentation')
                data = coding.xml.get_data_by_mode(type)
            error_order = ['mode','status','executedTime','errorParameter','errorMessage']
            success_order = ['mode','status','executedTime','fromFilePath','toFilePath','oldSize','newSize']
            for log in data:
                if log['status']==str(Status.SUCCESS.value):
                    for order in success_order:
                        value = 'bytes' if order in [success_order[-2],success_order[-1]] else ''
                        time_convert= datetime.datetime.fromtimestamp(round(float(log[order]))) \
                            if order=='executedTime' else log[order]
                        print(f'{order}=> {time_convert} {value}')
                else:
                    for order in error_order:
                        time_convert= datetime.datetime.fromtimestamp(round(float(log[order]))) \
                            if order=='executedTime' else log[order]
                        print(f'{order}=> {time_convert}')
                print()


    else:
        raise Exception('inline argument is incorrect')
