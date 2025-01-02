import cv2
import numpy as np
import pyautogui
import time
from utils import stop_event

def get_template_coordinates(image_path: str):
    def find_template(screenshot, template, threshold=0.8):
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            return True, max_loc, max_val
        return False, None, max_val
    
    try:
        print(f"find_template_loop を開始: {image_path}")
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("テンプレート画像が読み込めません")
            return False

        h, w = template.shape

        while not stop_event.is_set():
            try:
                # スクリーンショットを取得
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
                
                # テンプレートマッチング実行
                found, loc, confidence = find_template(screenshot, template)
                
                if found:
                    print("テンプレートを検出しました。")
                    # 検出位置の中心を計算
                    center_x = loc[0] + w//2
                    center_y = loc[1] + h//2

                    return center_x, center_y
                
                time.sleep(0.2)

            except Exception as e:
                print(f"ループ内でエラーが発生: {e}")
                if stop_event.is_set():
                    return False
                

    except Exception as e:
        print(f"get_template_coordinates でエラーが発生: {e}")
        return False
    finally:
        print("get_template_coordinates を終了")

def click_coordinates(x, y, delay=0.5):
    time.sleep(delay)
    print(f"click_coordinates を実行: {x}, {y}")
    pyautogui.click(x, y)

def find_template_and_click(image_path: str, delay=0.5):
    result = get_template_coordinates(image_path)
    if isinstance(result, tuple):
        x, y = result
        click_coordinates(x, y, delay)
