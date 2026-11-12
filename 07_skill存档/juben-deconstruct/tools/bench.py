import os, time
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, pymupdf

def patched_init():
    import rapidocr_onnxruntime.utils as ru
    from onnxruntime import SessionOptions
    class SO(SessionOptions):
        def __init__(self):
            super().__init__()
            self.intra_op_num_threads = 1
            self.inter_op_num_threads = 1
    ru.SessionOptions = SO

patched_init()
from rapidocr_onnxruntime import RapidOCR
e = RapidOCR()
d = pymupdf.open(r"C:\Users\12258\Downloads\954虚拟游戏\剧本\剧本\1李雨婷.pdf")
for i in [0, 1, 2]:
    t = time.time()
    pix = d[i].get_pixmap(matrix=pymupdf.Matrix(1.51, 1.51), colorspace=pymupdf.csGRAY, alpha=False)
    g = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    arr = np.repeat(g[:, :, None], 3, axis=2)
    t2 = time.time()
    r, _ = e(arr)
    print("p%d render=%.2f ocr=%.2f boxes=%d" % (i + 1, t2 - t, time.time() - t2, 0 if not r else len(r)), flush=True)
