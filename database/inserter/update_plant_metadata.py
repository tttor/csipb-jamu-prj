# update_plant_meta.py

## PLANT #######################################################################
elif [ "$1" == "upidr" ]; then
  ### update IDR plant name
  mode=updatePlantIdrName
  outDir=/home/tor/robotics/prj/csipb-jamu-prj/xprmt/insert-data-ijah
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/latin2idr_20170118-114630.json
  python insert_plant.py $db $user $passwd $host $port $mode $outDir $path

def updatePlantIdrName(csr,outDir,fpath):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    latin2idr = {}
    with open(fpath,'r') as f:
        latin2idr = yaml.load(f)

    idx = 0
    log = []
    for latin,idr in latin2idr.iteritems():
        idx += 1
        s = 'updating '+latin+': '+idr+ ' idx= '+str(idx)+' of '+str(len(latin2idr))
        print s

        qf = "UPDATE plant SET pla_idr_name="+"'"+idr+"'"
        qr = " WHERE pla_name="+"'"+latin+"'"
        q = qf+qr
        csr.execute(q)
        affectedRows = csr.rowcount;

        if affectedRows==0:
            log.append('NOT FOUND:'+s)

    with open(outDir+'/updatePlantIdrName_'+timestamp+'.log','w') as f:
        for i in log: f.write(i+'\n');