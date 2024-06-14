from psd_tools import PSDImage
from PIL import Image

import bpy

# import os
# import sys
# # PYTHONPATHにzipファイルを追加
# basepath = os.path.split(os.path.realpath(__file__))[0]
# print(os.path.join(basepath, 'ex-library'))
# sys.path.insert(0, os.path.join(basepath, 'ex-library'))
# # PILモジュールのロード
# import PIL
# from PIL import Image
# from psd_tools import PSDImage

def make_psd_data(psd_path):
    psd = PSDImage.open(psd_path)
    psd_list = _reprocess_psd(psd)
    image = _make_image(psd,psd_list)


def _reprocess_psd(psd):
    psd_list = []
    # psd_list作成
    for index,layer in enumerate(psd):
        if layer.is_group():# レイヤーがグループの場合、その中のレイヤーも処理
            sublayer_list = []
            for sublayer in layer:
                layer_info = [sublayer.left, sublayer.top, sublayer.visible]
                sublayer_list.append(layer_info)
            psd_list.append(sublayer_list)
        else:# レイヤーが単独のレイヤーの場合
            psd_list.append([[layer.left, layer.top, layer.visible]])
    return psd_list

def _make_image(psd,psd_list):
    combined_image = Image.new('RGBA', psd.size)
    for group_index,item in enumerate(psd_list):
        if len(item) == 1:
            if item[0][2]:
                layer_image = psd[group_index].composite()
                combined_image.paste(layer_image, (item[0][0], item[0][1]), layer_image)
        else:# グループレイヤーの場合
            for layer_index, layer_info in enumerate(item):
                if layer_info[2]:
                    layer_image = psd[group_index][layer_index].composite()
                    combined_image.paste(layer_image, (layer_info[0], layer_info[1]), layer_image)
    combined_image.show()
    return combined_image

if __name__ == "__main__":
    make_psd_data("./test/小春六花ver1.1_めじろーす_im11070159.psd")