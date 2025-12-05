import streamlit as st
import streamlit.components.v1 as components
import json

def main():
    st.set_page_config(layout="wide", page_title="Floating & Breathing Keyboard")

    # --- 余白削除 & ワイド表示用のCSS設定 ---
    st.markdown("""
        <style>
            /* メインエリアのパディングを削除して横幅最大化 */
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
                max-width: 100%;
            }
            /* iframeの強制ワイド化 */
            iframe {
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("⌨️ Floating & Breathing Keyboard")
    st.caption("キーボードが呼吸しながら、画面内を不規則に浮遊します。")

    # サイドバー設定
    with st.sidebar:
        st.header("呼吸（サイズ）の設定")
        breath_speed = st.slider("呼吸の速さ (秒)", 0.1, 5.0, 2.0, 0.1)
        scale_min = st.slider("最小サイズ (縮小時)", 0.5, 1.0, 0.8, 0.01)
        scale_max = st.slider("最大サイズ (拡大時)", 1.0, 1.5, 1.1, 0.01)

        st.divider() # 区切り線

        st.header("浮遊（移動）の設定")
        move_speed = st.slider("移動の速さ (秒)", 1.0, 20.0, 5.0, 0.5, help="数値が小さいほど激しく動きます")
        move_range = st.slider("移動距離 (px)", 0, 200, 30, 5, help="上下左右に動く幅です")

    # --- キーボードデータ ---
    rows = [
        # Row 1
        [
            {"label": "~", "sub": "`", "val": "`", "w": 1},
            {"label": "!", "sub": "1 ぬ", "val": "1", "w": 1},
            {"label": "@", "sub": "2 ふ", "val": "2", "w": 1},
            {"label": "#", "sub": "3 あ", "val": "3", "w": 1},
            {"label": "$", "sub": "4 う", "val": "4", "w": 1},
            {"label": "%", "sub": "5 え", "val": "5", "w": 1},
            {"label": "^", "sub": "6 お", "val": "6", "w": 1},
            {"label": "&", "sub": "7 や", "val": "7", "w": 1},
            {"label": "*", "sub": "8 ゆ", "val": "8", "w": 1},
            {"label": "(", "sub": "9 よ", "val": "9", "w": 1},
            {"label": ")", "sub": "0 わ", "val": "0", "w": 1},
            {"label": "-", "sub": "ー", "val": "-", "w": 1, "color": "yellow"},
            {"label": "+", "sub": "=", "val": "=", "w": 1},
            {"label": "BS", "sub": "", "val": "BS", "w": 2, "align": "right"},
        ],
        # Row 2
        [
            {"label": "Tab", "sub": "", "val": "\t", "w": 1.5, "align": "left"},
            {"label": "Q", "sub": "た", "val": "q", "w": 1},
            {"label": "W", "sub": "て", "val": "w", "w": 1},
            {"label": "E", "sub": "い", "val": "e", "w": 1},
            {"label": "R", "sub": "す", "val": "r", "w": 1, "color": "red"},
            {"label": "T", "sub": "か", "val": "t", "w": 1},
            {"label": "Y", "sub": "ん", "val": "y", "w": 1},
            {"label": "U", "sub": "な", "val": "u", "w": 1},
            {"label": "I", "sub": "に", "val": "i", "w": 1},
            {"label": "O", "sub": "ら", "val": "o", "w": 1},
            {"label": "P", "sub": "せ", "val": "p", "w": 1},
            {"label": "{", "sub": "「", "val": "{", "w": 1, "color": "yellow"},
            {"label": "}", "sub": "」", "val": "}", "w": 1, "color": "yellow"},
            {"label": "|", "sub": "ー", "val": "|", "w": 1, "color": "yellow"},
        ],
        # Row 3
        [
            {"label": "Caps", "sub": "", "val": "", "w": 1.8, "align": "left"},
            {"label": "A", "sub": "ち", "val": "a", "w": 1},
            {"label": "S", "sub": "と", "val": "s", "w": 1},
            {"label": "D", "sub": "し", "val": "d", "w": 1, "color": "red"},
            {"label": "F", "sub": "は", "val": "f", "w": 1, "color": "red"},
            {"label": "G", "sub": "き", "val": "g", "w": 1},
            {"label": "H", "sub": "く", "val": "h", "w": 1},
            {"label": "J", "sub": "ま", "val": "j", "w": 1},
            {"label": "K", "sub": "の", "val": "k", "w": 1},
            {"label": "L", "sub": "り", "val": "l", "w": 1},
            {"label": ":", "sub": ";", "val": ":", "w": 1, "color": "green"},
            {"label": "\"", "sub": "'", "val": "\"", "w": 1, "color": "green"},
            {"label": "Enter", "sub": "", "val": "\n", "w": 2.2, "align": "right"},
        ],
        # Row 4
        [
            {"label": "Shift", "sub": "", "val": "", "w": 2.3, "align": "left"},
            {"label": "Z", "sub": "つ", "val": "z", "w": 1},
            {"label": "X", "sub": "さ", "val": "x", "w": 1, "color": "red"},
            {"label": "C", "sub": "そ", "val": "c", "w": 1, "color": "red"},
            {"label": "V", "sub": "ひ", "val": "v", "w": 1, "color": "red"},
            {"label": "B", "sub": "こ", "val": "b", "w": 1},
            {"label": "N", "sub": "み", "val": "n", "w": 1},
            {"label": "M", "sub": "も", "val": "m", "w": 1},
            {"label": "<", "sub": "、", "val": "<", "w": 1},
            {"label": ">", "sub": "。", "val": ">", "w": 1},
            {"label": "?", "sub": "・", "val": "?", "w": 1},
            {"label": "Shift", "sub": "", "val": "", "w": 2.7, "align": "right"},
        ],
        # Row 5
        [
            {"label": "Ctrl", "sub": "", "val": "", "w": 1.5},
            {"label": "Fn", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "", "sub": "", "val": " ", "w": 6},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Ctrl", "sub": "", "val": "", "w": 1},
            {"label": "←", "sub": "", "val": "", "w": 1},
            {"label": "↑↓", "sub": "", "val": "", "w": 1, "is_arrow": True},
            {"label": "→", "sub": "", "val": "", "w": 1},
        ]
    ]

    rows_json = json.dumps(rows)

    # --- HTML/CSS/JS テンプレート ---
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&family=Noto+Sans+JP:wght@400&display=swap');

        body {{
            font-family: 'Roboto Mono', 'Noto Sans JP', monospace;
            background-color: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            overflow: hidden;
        }}

        /* スクリーン（入力欄）は固定して見やすく */
        #screen {{
            width: 95%;
            height: 50px;
            background-color: #333;
            color: #0f0;
            font-size: 20px;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            font-family: monospace;
            resize: none;
            box-sizing: border-box;
            z-index: 200; /* 最前面に */
            position: relative;
        }}

        /* --- アニメーション定義 --- */

        /* 1. 呼吸（サイズ変化） */
        @keyframes breathe {{
            0% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
            50% {{ transform: scaleX({scale_max}) scaleY({scale_max}); }}
            100% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
        }}

        /* 2. 浮遊（位置移動）: 8の字やランダムな軌道を模倣 */
        @keyframes float {{
            0% {{ transform: translate(0px, 0px); }}
            20% {{ transform: translate({move_range}px, -{move_range/2}px); }}
            40% {{ transform: translate(-{move_range/2}px, {move_range}px); }}
            60% {{ transform: translate(-{move_range}px, -{move_range/2}px); }}
            80% {{ transform: translate({move_range/2}px, {move_range/2}px); }}
            100% {{ transform: translate(0px, 0px); }}
        }}

        /* コンテナ1: 移動を担当（外側） */
        .movement-wrapper {{
            animation: float {move_speed}s infinite ease-in-out;
            width: 95%;
            display: flex;
            justify-content: center; /* 内部のキーボードを中央寄せ */
            /* 移動してもレイアウトが崩れないように少し余裕を持たせる */
            padding: {move_range}px; 
        }}

        /* コンテナ2: 呼吸を担当（内側） */
        .keyboard-wrapper {{
            animation: breathe {breath_speed}s infinite ease-in-out;
            padding: 10px;
            background-color: #e8eaed;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%; /* 親要素(movement-wrapper)の幅に合わせる */
            height: 55vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }}

        .kb-row {{
            display: flex;
            justify-content: space-between;
            width: 100%;
            height: 18%;
        }}

        .key {{
            background-color: white;
            border: 1px solid #999;
            border-bottom: 3px solid #777;
            border-radius: 4px;
            margin: 0 1px;
            position: relative;
            cursor: pointer;
            transition: all 0.1s;
            user-select: none;
            box-shadow: 0 2px 2px rgba(0,0,0,0.1);
            flex-basis: 0; 
            height: 100%;
        }}

        .key:active {{
            transform: translateY(2px);
            border-bottom: 1px solid #777;
            background-color: #f0f0f0;
        }}

        .label-top {{
            position: absolute;
            top: 4px;
            left: 6px;
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }}
        
        .label-sub {{
            position: absolute;
            bottom: 4px;
            right: 6px;
            font-size: 10px;
            color: #888;
        }}

        @media (max-width: 800px) {{
             .label-top {{ font-size: 10px; }}
             .label-sub {{ font-size: 8px; }}
        }}

        .color-red {{ background-color: #ea9999; border-color: #c06666; }}
        .color-yellow {{ background-color: #ffe599; border-color: #d1b866; }}
        .color-green {{ background-color: #b6d7a8; border-color: #7b9e6d; }}

        .arrow-stack {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            font-size: 10px;
            line-height: 10px;
        }}

    </style>
    </head>
    <body>
        <textarea id="screen" placeholder="Tap keys..."></textarea>
        
        <div class="movement-wrapper">
            <div class="keyboard-wrapper" id="keyboard"></div>
        </div>

        <script>
            const rows = {rows_json};
            const container = document.getElementById('keyboard');
            const screen = document.getElementById('screen');

            rows.forEach(row => {{
                const rowDiv = document.createElement('div');
                rowDiv.className = 'kb-row';

                row.forEach(k => {{
                    const keyDiv = document.createElement('div');
                    keyDiv.className = 'key';
                    keyDiv.style.flexGrow = k.w;
                    
                    if(k.color) keyDiv.classList.add('color-' + k.color);

                    if(k.is_arrow) {{
                        keyDiv.innerHTML = `
                            <div class="arrow-stack">
                                <span>▲</span><span>▼</span>
                            </div>
                        `;
                    }} else {{
                        keyDiv.innerHTML = `
                            <span class="label-top">${{k.label || ''}}</span>
                            <span class="label-sub">${{k.sub || ''}}</span>
                        `;
                    }}

                    keyDiv.onclick = () => {{
                        if (k.val === 'BS') {{
                            screen.value = screen.value.slice(0, -1);
                        }} else if (k.val) {{
                            screen.value += k.val;
                        }}
                        screen.scrollTop = screen.scrollHeight;
                    }};

                    rowDiv.appendChild(keyDiv);
                }});

                container.appendChild(rowDiv);
            }});
        </script>
    </body>
    </html>
    """
    
    # 動き回ってもはみ出さないよう、高さを多めに確保
    components.html(html_code, height=700, scrolling=False)

if __name__ == "__main__":
    main()
