import datetime
import decimal
import json
import os

import numpy as np
import scipy.io as sio


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytearray):  # 返回内容如果包含bytearray类型的数据
            return str(obj, encoding='utf-8')
        elif isinstance(obj, datetime.datetime):  # 返回内容如果包含datetime类型的数据
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, decimal.Decimal):  # 返回内容如果包含Decimal类型的数据
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    load_fn = '2%.mat'
    load_data = sio.loadmat(load_fn)
    print(load_data.keys())

    save_fn = os.path.splitext(load_fn)[0] + '.json'
    file = open(save_fn, 'w', encoding='utf-8')
    file.write(json.dumps(load_data, cls=MyEncoder, indent=4))
    file.close()
