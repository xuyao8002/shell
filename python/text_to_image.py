# 1、pip install diffusers transformers torch accelerate fastapi uvicorn
# 2、uvicorn main:app --host 0.0.0.0 --port 8080
# 3、curl http://localhost:8080/v1/images/generations \
#   -H "Content-Type: application/json" \
#   -d '{
#     "prompt": "Grazing sheep",
#     "size": "1024x1024",
#     "style": "vivid",
#     "quality": "hd"
#   }'
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image
import base64
from io import BytesIO
import gc

app = FastAPI()

# --- 配置参数映射 ---
SIZE_MAP = {
    "1024x1024": (1024, 1024),
    "1024x1792": (1024, 1792),#显存不够，降低分辨率 
    "1792x1024": (1792, 1024),
}

STYLE_MAP = {
    "vivid": "best quality, vibrant, dramatic lighting, saturated colors",
    "natural": "photorealistic, natural lighting, soft colors, realistic shadows"
}

QUALITY_MAP = {
    "standard": {"num_inference_steps": 30, "refiner": False},
    "hd": {"num_inference_steps": 40, "refiner": True}
}

# --- 设备设置 ---
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16

# --- 懒加载模型函数 ---
def get_base_pipeline():
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch_dtype,
        variant="fp16"
    )
    pipe.enable_attention_slicing()
    return pipe.to(device)

def get_refiner_pipeline():
    pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        torch_dtype=torch_dtype,
        variant="fp16"
    )
    pipe.enable_attention_slicing()
    return pipe.to(device)

# --- 清理 GPU 显存 ---
def clear_gpu_memory():
    torch.cuda.empty_cache()
    gc.collect()

# --- API 请求格式 ---
class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    style: str = "vivid"
    quality: str = "standard"

@app.post("/v1/images/generations")
async def generate_image(req: ImageRequest):
    width, height = SIZE_MAP.get(req.size, (1024, 1024))
    style_prompt = STYLE_MAP.get(req.style, "")
    quality_config = QUALITY_MAP.get(req.quality, {"num_inference_steps": 30, "refiner": False})

    full_prompt = f"{req.prompt}, {style_prompt}"
    negative_prompt = "blurry, low quality, distorted, ugly"

    # -------------------------------
    # 第一阶段：Base 模型生成
    # -------------------------------
    base_pipe = get_base_pipeline()

    try:
        # 🔁 根据是否需要 refiner 决定输出类型
        output_type = "latent" if quality_config["refiner"] else "pil"

        result = base_pipe(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=quality_config["num_inference_steps"],
            output_type=output_type,
        )

        if not quality_config["refiner"]:
            # ✅ 直接返回 PIL 图像
            image = result.images[0]
        else:
            # ✅ 返回 latent，用于 refiner
            image_latent = result.images[0]

    finally:
        base_pipe.to("cpu")
        del base_pipe
        clear_gpu_memory()

    # -------------------------------
    # 第二阶段：Refiner 精炼（仅 high_quality）
    # -------------------------------
    if quality_config["refiner"]:
        refiner_pipe = get_refiner_pipeline()

        try:
            image = refiner_pipe(
                prompt=full_prompt,
                negative_prompt=negative_prompt,
                image=image_latent,
                num_inference_steps=30,
                strength=0.3,
            ).images[0]

            # 删除 latent
            del image_latent

        finally:
            refiner_pipe.to("cpu")
            del refiner_pipe
            clear_gpu_memory()

    # -------------------------------
    # 转为 base64 返回
    # -------------------------------
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return {
        "created": 1234567890,
        "data": [
            {
                "b64_json": img_str,
                "revised_prompt": full_prompt
            }
        ]
    }
