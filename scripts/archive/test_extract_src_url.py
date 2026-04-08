import re

inputs = ["&lt;iframe height=\"1280\" width= \"720\" src=\"https://www.tiktok.com/player/v1/7619517332515294478?&amp;autoplay=0&amp;timestamp=0&amp;rel=0\" sandbox=\"allow-scripts allow-same-origin allow-popups\" allow=\"fullscreen\" title=\"Tiktok Video\"&gt;&lt;/iframe&gt;",
"&lt;iframe height=\"1280\" width= \"720\" src=\"https://www.tiktok.com/player/v1/7619517332515294478?&amp;autoplay=0&amp;timestamp=0&amp;rel=0\" sandbox=\"allow-scripts allow-same-origin allow-popups\" allow=\"fullscreen\" title=\"Tiktok Video\"&gt;&lt;/iframe&gt;",
"&lt;iframe width=\"113\" height=\"200\" src=\"https://www.youtube.com/embed/YfEgIQUETbY?feature=oembed&amp;enablejsapi=1\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen title=\"\ud83d\udea8 HOJE \u00c9 MEU ANIVERS\u00c1RIO \u2022 ATUALIZA\u00c7\u00c3O DO MEU QUADRO DE SA\u00daDE (VegetariRango)\"&gt;&lt;/iframe&gt;",
"&lt;iframe width=\"113\" height=\"200\" src=\"https://www.youtube.com/embed/YfEgIQUETbY?feature=oembed&amp;enablejsapi=1\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen title=\"\ud83d\udea8 HOJE \u00c9 MEU ANIVERS\u00c1RIO \u2022 ATUALIZA\u00c7\u00c3O DO MEU QUADRO DE SA\u00daDE (VegetariRango)\"&gt;&lt;/iframe&gt;",
 "&lt;iframe width=\"356\" height=\"200\" src=\"https://www.youtube.com/embed/GrAvvDoRUws?feature=oembed&amp;enablejsapi=1\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen title=\"I debated five meat eaters on Skavlan, Sweden&amp;#39;s biggest talk show\"&gt;&lt;/iframe&gt;"
]
def extract_src_url(text):
    # TODO: this doesn't work as expected. fix it!
    match = re.search(r'src="([^"]*)"', text)
    if match:
        return match.group(1)
    return None

for input in inputs:
    print("-", extract_src_url(input))