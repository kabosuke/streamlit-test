import streamlit as st
import random
# import pandas as pd これは後でね。


st.set_page_config(
    page_title="streamlit main",
    page_icon="😽"
)

hands = {1:'グー', 2:'チョキ', 3:'パー'}

def get_my_num():
    return random.randint(1, 3)

def show_result(my_num, yours):
    your_num = [k for k, v in hands.items() if v == yours][0]
    if my_num < your_num:
        my_num = my_num + 3
    diff = my_num - your_num
    if diff == 0:
        return 'あいこです😑'
    elif diff == 1:
        return 'あなたの勝ちです😸'
    else:
        return 'あなたの負けです😿'

yours = st.radio("じゃんけんの手を選んでください",(hands.values()))
pon = st.button("ポン!", icon="😼", type="primary")
cleared = st.button("クリア")

if pon:
    my_num = get_my_num()
    st.write(f"わたしは{hands[my_num]}です。　" + show_result(my_num, yours))
else:
    st.write("")

