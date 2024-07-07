import os
import torch
from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration, BitsAndBytesConfig

model_id = "llava-hf/LLaVA-NeXT-Video-7B-hf"

# Quantization Config
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_storage=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = LlavaNextVideoForConditionalGeneration.from_pretrained(
    model_id, 
    quantization_config=quantization_config,
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    torch_dtype=torch.bfloat16
)

processor = LlavaNextVideoProcessor.from_pretrained(
    model_id,
    trust_remote_code=True,
)

save_dir = 'backend/ai_models/videoSummarizer/llava-next'
os.makedirs(save_dir, exist_ok=True)
model.save_pretrained(save_dir)
processor.save_pretrained(save_dir)