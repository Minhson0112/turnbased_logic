import requests
from io import BytesIO
from PIL import Image
from PIL.Image import Resampling

# 1. Tải ảnh
bg_url = "https://cdn.discordapp.com/attachments/1359135350538244120/1361923584397803740/Valley_of_the_end.png?ex=6801d72d&is=680085ad&hm=02de38203de79d18bbe5c7bab0bbbee20c363374b6a5c21bb99f46cede366585&"
fg_url = "https://cdn.discordapp.com/attachments/1359449182938726612/1359784637651484723/Uzumaki_Naruto.gif?ex=6801f821&is=6800a6a1&hm=31044ffc6ae632fffb50e09379d09075475a7fb18f39b8145ecfd5bcf0f39fd0&"

resp_bg = requests.get(bg_url)
resp_fg = requests.get(fg_url)

bg = Image.open(BytesIO(resp_bg.content)).convert("RGBA")
fg = Image.open(BytesIO(resp_fg.content)).convert("RGBA")

# 2. Resize foreground bằng Resampling.LANCZOS (tương đương ANTIALIAS cũ)
fg = fg.resize((200, 200), Resampling.LANCZOS)

# 3. Tính toạ độ ở giữa background
bw, bh = bg.size
fw, fh = fg.size
pos = ((bw - fw) // 2, (bh - fh) // 2)

# 4. Ghép ảnh giữ alpha
bg.paste(fg, pos, fg)

# 5. Hiển thị hoặc lưu file
bg.show()
# bg.save("result.png")
