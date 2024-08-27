FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

WORKDIR /app/

RUN apt update && apt install -y wget && \
   mkdir nougat-base \
   && cd nougat-base \
   && wget https://github.com/facebookresearch/nougat/releases/download/0.1.0-base/config.json \
   && wget https://github.com/facebookresearch/nougat/releases/download/0.1.0-base/pytorch_model.bin \
   && wget https://github.com/facebookresearch/nougat/releases/download/0.1.0-base/special_tokens_map.json  \
   && wget https://github.com/facebookresearch/nougat/releases/download/0.1.0-base/tokenizer.json  \
   && wget https://github.com/facebookresearch/nougat/releases/download/0.1.0-base/tokenizer_config.json

RUN pip install -U nougat-ocr && pip install -U albumentations==1.0
RUN pip install transformers==4.38.2

WORKDIR /app/

ENTRYPOINT ["nougat", "--checkpoint", "./nougat-base/" -o "."]
