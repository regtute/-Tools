import shutil
import os
import time
from tkinter import Tk, Button, filedialog, messagebox
import psutil

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("ICO Files", "*.ico")])
    if file_path:
        print("选择的文件路径为:", file_path)
        disk_list = []
        for partition in psutil.disk_partitions():
            if "fixed" in partition.opts and "c:\\" not in partition.mountpoint.lower():
                disk_list.append(partition.mountpoint)
        if disk_list:
            root = Tk()
            root.title("选择磁盘")
            root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

            def copy_to_disk(disk):
                timestamp = str(int(time.time()))
                dest_path = os.path.join(disk, f"{timestamp}.ico")
                shutil.copyfile(file_path, dest_path)
                messagebox.showinfo("复制成功", f"文件已成功复制到磁盘: {dest_path}")

                autorun_path = os.path.join(disk, "autorun.inf")
                with open(autorun_path, "w") as f:
                    f.write(f"[autorun]\nicon={os.path.basename(dest_path)}")

                messagebox.showinfo("创建成功", f"已在磁盘中创建autorun.inf文件: {autorun_path}")

                root.destroy()

            for index, disk in enumerate(disk_list):
                button = Button(root, text=disk, command=lambda disk=disk: copy_to_disk(disk))
                button.pack(pady=5)

            root.mainloop()
        else:
            messagebox.showinfo("错误", "没有找到可用的磁盘")

def shutdown():
    os.system("shutdown /r /t 0")

root = Tk()
root.title("选择ICO文件")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

select_button = Button(root, text="选择ICO文件", command=select_file)
select_button.pack(pady=20)

shutdown_button = Button(root, text="立即重启", command=shutdown)
shutdown_button.pack(pady=20)

root.mainloop()