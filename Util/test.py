# -*- encoding=utf8 -*-
__author__ = "timo"

from airtest.core.api import *
from airtest.utils.transform import TargetPos

init_device()
# touch(Template(filename=r"/Users/timo/Downloads/WeChat94b142bae9bf158c1910b2c0c99fe59e.png", record_pos=(0.37, -0.825), resolution=(1080, 2340)))2340
# touch(Template(r"tpl1646100165596.png", record_pos=(-0.167, -0.896), resolution=(1080, 2244)))
screen = G.DEVICE.snapshot(filename=None, quality=ST.SNAPSHOT_QUALITY)
focus_pos = Template(filename=r"/Users/timo/Downloads/WechatIMG95.png",
                     record_pos=(-0.167, -0.896), resolution=(1080, 2244)).match_in(screen)
print(focus_pos[0])
print(focus_pos[1])
