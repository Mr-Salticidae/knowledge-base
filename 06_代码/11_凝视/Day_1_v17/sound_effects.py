"""
《凝视》视频音效生成模块 v2
关键改进:
- 不只用低频(纯低频在手机/电脑扬声器上几乎听不到)
- 每个音效都包含中频和高频内容
- 使用瞬态(transient)制造打击感
- 整体响度参考商业作品标准
"""

import numpy as np
from moviepy import AudioArrayClip

SAMPLE_RATE = 44100


def _to_audio_clip(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> AudioArrayClip:
    if samples.ndim == 1:
        stereo = np.stack([samples, samples], axis=-1)
    else:
        stereo = samples
    stereo = np.clip(stereo, -1.0, 1.0)
    return AudioArrayClip(stereo, fps=sample_rate)


def silence(duration: float) -> AudioArrayClip:
    n_samples = int(duration * SAMPLE_RATE)
    return _to_audio_clip(np.zeros(n_samples, dtype=np.float32))


def _highpass_simple(samples: np.ndarray, cutoff: float, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """简单的一阶高通滤波(去除直流和极低频)"""
    rc = 1.0 / (2 * np.pi * cutoff)
    dt = 1.0 / sample_rate
    alpha = rc / (rc + dt)
    
    out = np.zeros_like(samples)
    out[0] = samples[0]
    for i in range(1, len(samples)):
        out[i] = alpha * (out[i-1] + samples[i] - samples[i-1])
    return out


def low_drone(duration: float, 
              volume: float = 0.5,
              fade_in: float = 0.4,
              fade_out: float = 0.4) -> AudioArrayClip:
    """
    drone 持续音 v3
    - 去除白噪声(避免电流声)
    - 用 detune(轻微失谐)叠加多个正弦波,模拟真实乐器的"厚度"
    - 加入缓慢的呼吸感(LFO 调制)
    - 基础频率改用小三和弦关系,听起来"对"
    
    设计参考:大提琴/低音弦乐组的低音延音
    """
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # 用 A2 (110Hz) 为根音,构建 A minor 三和弦的低八度
    # A2 = 110Hz, C3 = 130.81Hz, E3 = 164.81Hz
    # 但全部往下 octave 让它沉一些
    root_freq = 55  # A1 (A2 的低八度)
    minor_third = 65.4  # C2
    fifth = 82.4  # E2
    
    samples = np.zeros(n_samples)
    
    # 主和弦:每个音用 3 个轻微 detune 的正弦波叠加
    # detune 让单频变成"宽频带",像真实乐器的厚度
    def add_detuned(freq, amplitude, detune_cents=8):
        """加一个'胖正弦波'(三个detuned叠加)"""
        # detune 成 cents (1200 cents = 1 octave)
        f_low = freq * (2 ** (-detune_cents / 1200))
        f_high = freq * (2 ** (detune_cents / 1200))
        return (
            np.sin(2 * np.pi * freq * t) * amplitude * 0.5 +
            np.sin(2 * np.pi * f_low * t + 0.3) * amplitude * 0.3 +
            np.sin(2 * np.pi * f_high * t + 0.7) * amplitude * 0.3
        )
    
    samples += add_detuned(root_freq, 0.5)
    samples += add_detuned(minor_third, 0.35)
    samples += add_detuned(fifth, 0.35)
    
    # 加一些上方八度(让中频也有内容,小喇叭能播)
    samples += add_detuned(root_freq * 2, 0.20, detune_cents=12)
    samples += add_detuned(minor_third * 2, 0.15, detune_cents=12)
    samples += add_detuned(fifth * 2, 0.15, detune_cents=12)
    
    # "呼吸"调制:整体音量缓慢起伏(0.3Hz,约 3秒一个周期)
    breath_lfo = 1.0 + 0.12 * np.sin(2 * np.pi * 0.3 * t - np.pi/2)
    samples *= breath_lfo
    
    # 应用淡入淡出
    fade_in_samples = int(fade_in * SAMPLE_RATE)
    fade_out_samples = int(fade_out * SAMPLE_RATE)
    if fade_in_samples > 0:
        samples[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    if fade_out_samples > 0:
        samples[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    
    # 归一化
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.95
    
    samples *= volume
    return _to_audio_clip(samples.astype(np.float32))


def pulse(duration: float = 0.04, volume: float = 0.95, decay_curve: float = 4.0) -> AudioArrayClip:
    """
    机械时钟咔嗒声 v2 (彻底重做)
    
    上一版的问题:有共鸣层(700-1300Hz木质腔体共振 + 残响尾巴),
    导致听起来像敲竹板/木鱼,而不是机械时钟。
    
    这一版:
    - 去除所有共鸣层
    - 频率改到真实时钟范围(1500-2500Hz)
    - 极短(40ms)
    - 加一点点低频底给"金属重量感"(避免被视觉抢戏)
    
    设计参考:真实机械时钟的擒纵机构 -- 金属齿与齿之间的瞬间接触
    """
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    samples = np.zeros(n_samples)
    
    # ========== 唯一的一层:金属瞬态(15ms) ==========
    # 真实时钟咔嗒就是金属齿轮接触的瞬间,没有"身体",只有"接触"
    transient_dur = 0.015  # 15ms
    transient_samples = int(transient_dur * SAMPLE_RATE)
    if transient_samples > 0 and transient_samples < n_samples:
        tt = t[:transient_samples]
        # 高频金属(1800-2400Hz是机械时钟咔嗒的核心频率)
        click = (
            np.sin(2 * np.pi * 1900 * tt) * 0.5 +
            np.sin(2 * np.pi * 2400 * tt + 0.4) * 0.4 +
            # 极少量噪声给"金属粗糙感",但量小不会变沙沙声
            np.random.randn(transient_samples) * 0.1
        )
        # 极快衰减(20ms内基本消失)
        click_env = np.exp(-200 * tt)
        samples[:transient_samples] += click * click_env
    
    # ========== 极轻微的低频"砸"(5ms,只是为了不被视觉盖过) ==========
    # 这一层不应该被"听到",但应该被"感觉到"
    # 模拟金属齿轮接触时的力度
    sub_dur = 0.008
    sub_samples = int(sub_dur * SAMPLE_RATE)
    if sub_samples > 0:
        st = t[:sub_samples]
        thump = np.sin(2 * np.pi * 150 * st) * 0.3  # 150Hz 低频
        thump_env = np.exp(-300 * st)
        samples[:sub_samples] += thump * thump_env
    
    # 注意:不再有任何"残响尾巴"或"中频共鸣"——那些是竹板,不是时钟
    
    # 归一化
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.95
    
    samples *= volume
    
    return _to_audio_clip(samples.astype(np.float32))


def click(duration: float = 0.08, volume: float = 0.6) -> AudioArrayClip:
    """咔嗒声"""
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    signal = (
        np.sin(2 * np.pi * 2000 * t) * 0.4 +
        np.sin(2 * np.pi * 4000 * t) * 0.3 +
        np.random.randn(n_samples) * 0.4
    )
    envelope = np.exp(-50 * t / duration)
    samples = signal * envelope * volume
    
    return _to_audio_clip(samples.astype(np.float32))


def resonance(duration: float = 2.5, volume: float = 0.6) -> AudioArrayClip:
    """
    长共鸣 v3
    设计为"和弦延音"——基于完整的小三和弦,有调性,听起来不别扭
    去除白噪声,用 detune 叠加产生厚度
    """
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # A minor 三和弦(同 drone 的调性,保持系列统一感)
    root = 55      # A1
    minor_third = 65.4  # C2
    fifth = 82.4   # E2
    
    samples = np.zeros(n_samples)
    
    def add_detuned(freq, amplitude, detune_cents=10):
        f_low = freq * (2 ** (-detune_cents / 1200))
        f_high = freq * (2 ** (detune_cents / 1200))
        return (
            np.sin(2 * np.pi * freq * t) * amplitude * 0.5 +
            np.sin(2 * np.pi * f_low * t + 0.5) * amplitude * 0.3 +
            np.sin(2 * np.pi * f_high * t + 1.1) * amplitude * 0.3
        )
    
    # 主和弦
    samples += add_detuned(root, 0.45)
    samples += add_detuned(minor_third, 0.35)
    samples += add_detuned(fifth, 0.35)
    
    # 上方八度(中频内容)
    samples += add_detuned(root * 2, 0.22, detune_cents=15)
    samples += add_detuned(minor_third * 2, 0.18, detune_cents=15)
    samples += add_detuned(fifth * 2, 0.18, detune_cents=15)
    
    # 再上一层(给一点"光泽")
    samples += add_detuned(root * 4, 0.10, detune_cents=20) * 0.5
    
    # 缓慢衰减(收尾要有"消散感")
    envelope = np.exp(-1.0 * t / duration)
    
    # 慢呼吸
    breath = 1.0 + 0.08 * np.sin(2 * np.pi * 0.5 * t)
    
    samples *= envelope * breath
    
    # 归一化
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.95
    
    samples *= volume
    return _to_audio_clip(samples.astype(np.float32))


def sub_thud(duration: float = 0.6, volume: float = 0.95) -> AudioArrayClip:
    """
    机械停摆般的深沉"哐"击
    用于Veritia的压轴登场
    
    设计:相比普通的时钟咔嗒,加重低频和共鸣,
    像是"时钟坏掉/停止"的瞬间,机械的金属重击
    """
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    samples = np.zeros(n_samples)
    
    # 第1层:金属撞击的高频瞬态(像时钟咔嗒但更尖)
    layer1_samples = int(0.005 * SAMPLE_RATE)
    if layer1_samples > 0:
        l1_t = t[:layer1_samples]
        click = (
            np.sin(2 * np.pi * 1800 * l1_t) * 0.5 +
            np.sin(2 * np.pi * 2800 * l1_t) * 0.4 +
            np.random.randn(layer1_samples) * 0.2
        )
        click_env = np.exp(-400 * l1_t)
        samples[:layer1_samples] += click * click_env
    
    # 第2层:中频金属共鸣(关键:这一层让它"机械感"而不是"心跳感")
    # 用 detune 叠加产生金属的"嗡"
    body_freq1 = 180
    body_freq2 = 240
    body = (
        np.sin(2 * np.pi * body_freq1 * t) * 0.5 +
        np.sin(2 * np.pi * body_freq1 * 1.005 * t + 0.3) * 0.3 +  # detune
        np.sin(2 * np.pi * body_freq2 * t) * 0.4 +
        np.sin(2 * np.pi * body_freq2 * 1.005 * t + 0.5) * 0.25  # detune
    )
    body_env = np.exp(-4.0 * t / duration)
    body *= body_env
    samples += body * 0.5
    
    # 第3层:低频"重量"(给"哐"的份量,但不会过重)
    sub = np.sin(2 * np.pi * 70 * t) * 0.4
    sub += np.sin(2 * np.pi * 110 * t) * 0.25
    sub_env = np.exp(-2.5 * t / duration)
    samples += sub * sub_env * 0.5
    
    # 第4层:长尾共鸣(让最后一击有"余韵",连接到resonance)
    tail = np.sin(2 * np.pi * 220 * t + 0.7) * 0.2
    tail += np.sin(2 * np.pi * 330 * t + 1.4) * 0.15
    tail_env = np.exp(-1.5 * t / duration)
    samples += tail * tail_env * 0.4
    
    # 归一化
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.95
    
    samples *= volume
    
    return _to_audio_clip(samples.astype(np.float32))


def ending_thud(duration: float = 1.4, volume: float = 0.85) -> AudioArrayClip:
    """
    结尾的大钟"咚",作为视频的落幕信号 v2
    
    与 sub_thud(Veritia 用的)的区别:
    - 主频在 100-220Hz(让小喇叭能播出厚重感)
    - 极低频 50Hz 作为"感受层"
    - 更长时长(1.4s vs 0.6s)
    - 平滑指数衰减(无呼吸调制,避免产生第二个能量峰)
    - 没有金属高频瞬态(不要锐利感)
    
    比喻:Veritia 是锤子敲下,这个是教堂大钟的尾韵
    """
    n_samples = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    samples = np.zeros(n_samples)
    
    # ========== 第1层:钝接触瞬态(钟槌敲击的瞬间) ==========
    # 不要金属click,要"钝"的感觉
    contact_dur = 0.020  # 比 sub_thud 长,但比咔嗒长很多
    contact_samples = int(contact_dur * SAMPLE_RATE)
    if contact_samples > 0:
        ct = t[:contact_samples]
        # 600-900Hz 给"钝接触"的感觉,不要太尖锐
        contact = (
            np.sin(2 * np.pi * 600 * ct) * 0.4 +
            np.sin(2 * np.pi * 900 * ct + 0.3) * 0.25
        )
        contact_env = np.exp(-100 * ct)
        samples[:contact_samples] += contact * contact_env
    
    # ========== 第2层:中频"主体"(关键的厚重感来源) ==========
    # 这一层是钟"咚"的核心,主要在 150-330Hz
    # 用 detune 叠加产生厚度
    def add_detuned_layer(freq, amp, detune_cents=10):
        f_low = freq * (2 ** (-detune_cents / 1200))
        f_high = freq * (2 ** (detune_cents / 1200))
        return (
            np.sin(2 * np.pi * freq * t) * amp * 0.5 +
            np.sin(2 * np.pi * f_low * t + 0.3) * amp * 0.3 +
            np.sin(2 * np.pi * f_high * t + 0.7) * amp * 0.3
        )
    
    # 主体频率(钟的"咚"声主要在这里)
    body = np.zeros(n_samples)
    body += add_detuned_layer(110, 0.55)   # 低音区,厚重
    body += add_detuned_layer(165, 0.40)   # 五度
    body += add_detuned_layer(220, 0.30)   # 八度
    body += add_detuned_layer(330, 0.20)   # 十二度(给"光泽"但不刺耳)
    
    # ========== 第3层:深低频"重量"(只在好的设备上能感受到) ==========
    sub = np.sin(2 * np.pi * 55 * t) * 0.3
    sub += np.sin(2 * np.pi * 82 * t) * 0.2  # detune 八度
    
    # ========== 衰减包络:平滑的指数衰减(无第二峰) ==========
    # 用单一 exp 函数,衰减系数让 1.4 秒后基本消失
    # 系数 = ln(0.05) / -duration ≈ 3 / duration
    decay_coef = 3.0
    envelope = np.exp(-decay_coef * t / duration)
    
    body *= envelope
    sub *= envelope * 0.9  # 低频衰减略快一点点,避免在尾部"嗡"出来
    
    samples += body
    samples += sub
    
    # 注意:故意不加 breath/tremolo 调制 -- 那是"两声咚"的元凶
    
    # 归一化
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.95
    
    samples *= volume
    
    return _to_audio_clip(samples.astype(np.float32))
