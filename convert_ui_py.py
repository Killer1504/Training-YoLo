import os
cmd1 = "pyuic5 -x hello.ui -o ui_hello.py"
cmd2 = "pyuic5 -x autodlg.ui -o ui_autodlg.py"
cmd3 = "pyuic5 -x Label.ui -o ui_label.py"
cmd4 = "pyuic5 -x training.ui -o ui_training.py"
cmd5 = "pyuic5 -x classdlg.ui -o ui_classdlg.py"
cmd6 = "pyuic5 -x setting.ui -o ui_setting.py"
os.system(cmd1)
os.system(cmd2)
os.system(cmd3)
os.system(cmd4)
os.system(cmd5)
os.system(cmd6)