import gradio as gr
import argparse
import whisper
import os
from utils import OpenaiMgr

TITLE = "视频总结"
prompt_txt_value = "请总结下面内容，要求如下：\n1.简洁，要陈列方式\n2.字数在300字内。\n内容如下:"
video_text = ""


# Whisper模型
WHISPER_MODEL = "large-v2.pt"
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
UP_PROJECT_PATH = os.path.join(PROJECT_PATH, "video_summarize")
MODE_PATH = os.path.join(UP_PROJECT_PATH, "model")
print(MODE_PATH+"/" + WHISPER_MODEL)
whisper_model =  whisper.load_model(MODE_PATH+ "/" + WHISPER_MODEL)

def whisper_to_str(content):
    return whisper_model.transcribe(content)  

def ok_handler(*args):
    [       video_path,  
            prompt      
    ] = args
    if video_path == None:
        gr.Warning("视频不能为空！")
        return
    print("1.提取视频文案")
    video_content = whisper_to_str(video_path)
    question = prompt + video_content["text"]
    print("2.GPT总结文案")
    s1,content = OpenaiMgr.call(question)
    print(content)
    return content
    
    
gradio_root = gr.Blocks(title=TITLE)
with gradio_root:
    with gr.Row():
        with gr.Column(scale=1):  # 修改 scale 为整数
            curVideo = gr.Video(label="In")  # 去掉 type 参数
            prompt_txt = gr.Textbox(label="提示词", lines=12, max_lines=12, value=prompt_txt_value) 
            ok_clik = gr.Button(value="总结", visible=True)  # 去掉 label 参数
        with gr.Column(scale=1, visible=True):  # 修改 scale 为整数
            video_box = gr.Textbox(label="本地总结", info="总结内容", lines=30, max_lines=30, value=video_text)  
    ok_clik.click(fn=ok_handler, inputs=[curVideo, prompt_txt], outputs=[video_box])
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7888, help="Set the listen port.")
    parser.add_argument("--share", action='store_true', help="Set whether to share on Gradio.")
    parser.add_argument("--listen", type=str, default=None, metavar="IP", nargs="?", const="0.0.0.0", help="Set the listen interface.")
    args = parser.parse_args()
    gradio_root.launch(inbrowser=True, server_name=args.listen, server_port=args.port, share=args.share)