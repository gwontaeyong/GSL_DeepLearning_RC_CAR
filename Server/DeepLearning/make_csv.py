import csv
import os


def search(dirname, wr):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename, wr)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.jpg': 
                    temp = full_filename.split("_")
                    #print(temp)
                    angle = temp[3]
                    temp2 = temp[4].split(".")
                    speed = temp2[0]
                    wr.writerow([full_filename,angle,speed])
    except PermissionError:
        pass


if __name__=="__main__":
<<<<<<< HEAD
    f = open('output.csv', 'w', newline='')
    wr = csv.writer(f)
    search("./Image2", wr)          # 전역변수 <-- 이미지폴더 있는 상위 폴더 주소 ex) D:\DeepLearning\2018-05-12 니까 D:/DeepLearning
                                        # Tools - Preferences - current working directory 값 잡아준대에 csv파일 저장됨..
=======

    file_dir = "csv"
    file_name = 'track_1_2_pigure.csv'

    search_dir = "Image"
    image_dir = ""


    file_full_name = os.path.join(file_dir, image_dir+file_name)
    image_full_name = os.path.join(search_dir, image_dir)


    f = open(file_full_name, 'w', newline='')
    wr = csv.writer(f)

    search(image_full_name, wr)
>>>>>>> 534cea4... save
    f.close()
