import sys

from insta_loader import post_comments, story_download, \
    post_detail_download, hashtag_posts_download, igtv_download, story_download1
from instalooterw import pp_download, download_image_video, instalooterw

if __name__ == '__main__':
    try:
        while True:
            a = "Press 'D' to download an instagram detail(image, video,...)." \
                "\nPress 'E' to download an hashtag posts." \
                "\nPress 'F' to download an instagram post comments (best_way)." \
                "\nPress 'Q' to exit."
            print(a)
            select = str(input("\nInstaSave > ")).upper()
            try:
                if select == 'A':
                    pp_download()
                if select == 'B':
                    download_image_video()
                if select == 'C':
                    instalooterw()
                if select == 'D':
                    post_detail_download()
                if select == "E":
                    hashtag_posts_download()
                if select == 'F':
                    post_comments()
                if select == 'G':
                    story_download()
                if select == 'H':
                    igtv_download()
                if select == 'I':
                    story_download1()
                if select == 'Q':
                    sys.exit()
                else:
                    sys.exit()
            except (KeyboardInterrupt):
                print("Programme Interrupted")
    except(KeyboardInterrupt):
        print("\nProgramme Interrupted")
