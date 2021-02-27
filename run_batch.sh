while getopts n:e:i: flag
do
    case "${flag}" in
        n) name=${OPTARG};;
        e) elements=${OPTARG};;
        i) iterations=${OPTARG};;
    esac
done
source env/bin/activate;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 1024;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 2048;
python mp2.py -d 1 -i $iterations -w 1 -e 1 -n $name --single 4096;
deactivate;
