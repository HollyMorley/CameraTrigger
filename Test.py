import csv
import os
directory = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\"
folder = "test"
list = ['one', 'two', 'three']
folder_name = [os.path.join(directory,folder + "{}".format(i)) for i in list]
print(folder_name)
[print(fdr) for fdr in folder_name]
for fdr in folder_name:
    with open(fdr + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SN", "Name", "Contribution"])
        writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
