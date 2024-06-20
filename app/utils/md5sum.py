import hashlib
import os 

class CheckFileByMd5sum():
    
    def make_md5sum_txt(self, files, path):

        # Create a dictionary to store the file names and their respective MD5 checksums
        md5sums = {}
        
        folder = path + "/md5sum"
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Calculate the MD5 checksum for each file and add it to the dictionary
        for file in files:
            with open(f'{path}/{file}', 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                md5sums[file] = md5
        
        # Write the file names and their MD5 checksums to a text file
        with open(f"{path}/md5sum/md5sum.txt", 'w') as f:
            for file, md5 in md5sums.items():
                f.write("{}  {}\n".format(md5, file))
                
        
    def check_md5sum_txt(self,path):

        md5sums = {}
        with open(f"{path}/md5sum/md5sum.txt", 'r') as f:
            print(" ---------------- ")
            print("/ MD5SUM RESULT / ")
            print("---------------- " + '\n')
            
            for line in f:
                line = line.strip().split()
                expected_md5 = line[0]
                file = line[1]
                md5sums[file] = expected_md5
            
        # Calculate the actual MD5 checksum for each file and compare it to the expected value
        for file, expected_md5 in md5sums.items():
            with open(f'{path}/{file}', 'rb') as f:
                data = f.read()
                actual_md5 = hashlib.md5(data).hexdigest()
                
                if actual_md5 != expected_md5:
                    print("{}: FAILED".format(file))
                else:
                    print("{}: OK".format(file))


