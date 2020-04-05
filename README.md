# MACNode
Use this program to verify database
 
## first generate sql base
```bash
sqlacodegen --outfile MACNodeSQL.py mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=utf8
```

## second generate test vector
```bash
python ./MACTestGenVipData.py
```

## check database
```bash
python ./MACCalData.py

```

## open mysql to see table `mymacnoderesult`