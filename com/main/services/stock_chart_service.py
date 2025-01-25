import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class StockChartService:
    def __init__(self):
        pass

    @staticmethod
    def MACD(df, window_slow, window_fast, window_signal):
        macd = pd.DataFrame()
        macd['ema_slow'] = df['close'].ewm(span=window_slow).mean()
        macd['ema_fast'] = df['close'].ewm(span=window_fast).mean()
        macd['macd'] = macd['ema_slow'] - macd['ema_fast']
        macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
        macd['diff'] = macd['macd'] - macd['signal']
        macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
        macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
        return macd