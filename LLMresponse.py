import discord
from discord.ext import commands
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
    LlamaTokenizerFast,
)
from peft import LoraConfig, PeftModel
from transformers import GemmaForCausalLM, AutoTokenizer,TextStreamer
import re
from zhconv import convert
import os
# 設置日誌的嚴重性級別
logging.set_verbosity(logging.CRITICAL)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# 加載模型和分詞器
model_name = "OpenBuddy/openbuddy-gemma-7b-v18.1-4k"

device_map = "cuda:0"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=False,
)        
# 加載基礎模型
model = GemmaForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map=device_map
)
model.config.use_cache = False  # 禁用cache以節省記憶體
model.eval()
# 加載LLaMA的分詞器
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"  # 設定填充位置在右側
streamer = TextStreamer(tokenizer, skip_prompt = True, skip_special_tokens = True)
def remove_input_from_output(input_text, output_text):
    # 使用正則表達式匹配輸入文本
    pattern = re.escape(input_text)
    # 移除匹配到的輸入文本
    filtered_output = re.sub(pattern, '', output_text, flags=re.IGNORECASE)
    return filtered_output.strip()
def generate_response(system_prompt,prompt):
    model.bfloat16()
    # 生成回應
    formatted_prompt = "system:"+system_prompt + "\n" + prompt + "\nAssistant:"
    inputs = tokenizer(str(formatted_prompt), return_tensors="pt")
    inputs = inputs.to(model.device)
    sentence = model.generate(**inputs, 
                                num_beams = 5, 
                                max_new_tokens = 700,
                                temperature=0.7,  # 控制生成多樣性的溫度參數
                                no_repeat_ngram_size=2,  # 防止生成重複的n-gram
                                repetition_penalty = 1.0, 
                                length_penalty =0.1, 
                                early_stopping = False, 
                                do_sample= True, 
                                num_return_sequences=1)
    decode_sentence = tokenizer.decode(sentence[0], skip_special_tokens=True)
    decode_sentence = remove_input_from_output(formatted_prompt, decode_sentence)
    # 定義正規表達式
    pattern = r"<built-in function input>\n(.+)"
    match = re.search(pattern, decode_sentence, re.DOTALL)
    if match:
        response = match.group(1).strip()
    else:
        response = decode_sentence
    response = response.replace("<eos>", "")
    
    response = convert(response,'zh-tw')
    return response
