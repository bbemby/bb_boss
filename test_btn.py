import os, sys
sys.path.insert(0, '/app/bb_emby')
os.chdir('/app/bb_emby')

import bot.func_helper.fix_bottons as fb
keyword = fb.judge_start_ikb(True, True)
print(keyword)
for row in keyword.inline_keyboard:
    for btn in row:
        print(btn)
