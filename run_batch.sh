while getopts n:e:i: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        e) elements=${OPTARG};;
        i) iterations=${OPTARG};;
    esac
done
source env/bin/activate;
python bwt.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 1024;
python bwt.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 2048;
python bwt.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 4096;
deactivate;
