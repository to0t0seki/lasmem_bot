from image_detector import find_template_and_click
import pygetwindow as gw

def main():
    count = 1
    window = gw.getWindowsWithTitle('Last Memories')[0]
    window.activate()
    while True:
        print(f"count: {count}")
        find_template_and_click("images/challenge.png",1)
        find_template_and_click("images/ok.png",1)
        find_template_and_click("images/result.png",1)
        count += 1

if __name__ == "__main__":
    main()