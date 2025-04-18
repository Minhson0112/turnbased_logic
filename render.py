import requests
from io import BytesIO
from PIL import Image
from PIL.Image import Resampling

# 1. Tải ảnh
bg_url = "https://cdn.discordapp.com/attachments/1359135350538244120/1361923584397803740/Valley_of_the_end.png?ex=68027fed&is=68012e6d&hm=5248f88d8516aa9cf131e6fb4149d5c0d9e4bb6f3807c94f0980b3f1d26b31a2&"
fg1_url = "https://cdn.discordapp.com/attachments/1359449182938726612/1359784637651484723/Uzumaki_Naruto.gif?ex=6801f821&is=6800a6a1&hm=31044ffc6ae632fffb50e09379d09075475a7fb18f39b8145ecfd5bcf0f39fd0&"
fgl2_url = "https://cdn.discordapp.com/attachments/1359415696240410714/1359437380536500397/Minato.gif?ex=6802aef8&is=68015d78&hm=da0e2c23c0ef921afabe8f2a34569c6ded2c11a2f58c062af3bf37a3600deb5b&"
fgl3_url = "https://cdn.discordapp.com/attachments/1359141742666059934/1359165563871428689/Kushina.gif?ex=68030352&is=6801b1d2&hm=3f009c34293934e93b343835fd43574bbac28513f438559feb5730576e89e71a&"
resp_bg = requests.get(bg_url)
resp_fg1 = requests.get(fg1_url)
resp_fg2 = requests.get(fgl2_url)
resp_fg3 = requests.get(fgl3_url)



bg = Image.open(BytesIO(resp_bg.content)).convert("RGBA")
fg1 = Image.open(BytesIO(resp_fg1.content)).convert("RGBA")
fg2 = Image.open(BytesIO(resp_fg2.content)).convert("RGBA")
fg3 = Image.open(BytesIO(resp_fg3.content)).convert("RGBA")



def resize(image):
    # 2. Resize foreground giữ nguyên tỉ lệ
    target_width = 150  # bạn có thể thay bằng target_height nếu muốn cố định chiều cao
    orig_w, orig_h = image.size
    aspect_ratio = orig_h / orig_w
    target_height = int(target_width * aspect_ratio)

    return image.resize((target_width, target_height), Resampling.LANCZOS)


fg1 = resize(fg1)
fg2 = resize(fg2)
fg3 = resize(fg3)

bw, bh = bg.size

fw, fh = fg1.size
n = 3
total_space = bw - (n * fw)
spacing = total_space // (n + 1)

pos1 = (spacing, 100)
pos2 = (spacing * 2 + fw, 100)
pos3 = (spacing * 3 + fw * 2, 100)


# 4. Ghép ảnh giữ alpha
bg.paste(fg1, pos1, fg1)
bg.paste(fg2, pos2, fg2)
bg.paste(fg3, pos3, fg3)

# 5. Hiển thị hoặc lưu file
bg.show()
# bg.save("result.png")
