"""旅行助手的工具函数。

负责天气 API 调用与基于规则的景点推荐，便于与 ``main.py`` 的流程调度分离。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
from datetime import datetime

import requests

# Open-Meteo 为免费且无需密钥的接口，可直接调用。
_OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
_BEIJING_LAT, _BEIJING_LON = 39.9042, 116.4074

# Weather code mapping: https://open-meteo.com/en/docs
_WEATHER_CODE_MAP: Dict[int, str] = {
    0: "晴朗",
    1: "多云（少量）",
    2: "多云（中量）",
    3: "阴天",
    45: "雾",
    48: "霜雾",
    51: "小毛毛雨",
    53: "中毛毛雨",
    55: "大毛毛雨",
    56: "轻度冻雨",
    57: "重度冻雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "轻冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "短时小阵雨",
    81: "短时中阵雨",
    82: "短时暴雨",
    85: "短时小阵雪",
    86: "短时大阵雪",
    95: "雷阵雨",
    96: "雷阵雨伴轻微冰雹",
    99: "雷阵雨伴强冰雹",
}


@dataclass
class WeatherInfo:
    temperature: float
    weather_code: int
    weather_desc: str
    wind_speed: float
    observation_time: str


def fetch_beijing_weather() -> WeatherInfo:
    """通过 Open-Meteo 查询北京当前天气。

    返回 ``WeatherInfo`` 数据类；失败时抛出 ``RuntimeError``。
    """

    # 构造无需密钥的请求参数
    params = {
        "latitude": _BEIJING_LAT,
        "longitude": _BEIJING_LON,
        "current_weather": "true",
        "hourly": "temperature_2m,weathercode,precipitation_probability",
        "timezone": "Asia/Shanghai",
    }

    try:
        resp = requests.get(_OPEN_METEO_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        cw = data.get("current_weather", {})
        code = int(cw.get("weathercode", -1))
        desc = _WEATHER_CODE_MAP.get(code, "天气代码未知")
        obs_time = cw.get("time", datetime.now().isoformat())

        return WeatherInfo(
            temperature=float(cw.get("temperature")),
            weather_code=code,
            weather_desc=desc,
            wind_speed=float(cw.get("windspeed", 0)),
            observation_time=obs_time,
        )
    except Exception as exc:  # noqa: BLE001 - surface nicely
        raise RuntimeError(f"天气查询失败: {exc}") from exc


def recommend_attraction(weather: WeatherInfo) -> Tuple[str, str]:
    """依据简单的天气规则返回 (景点, 推荐理由)。"""

    temp = weather.temperature
    desc = weather.weather_desc
    code = weather.weather_code

    # Rule set keeps recommendations deterministic and explainable.
    if code in {61, 63, 65, 80, 81, 82, 95, 96, 99}:  # rainy / thunder
        return (
            "中国国家博物馆",
            "下雨或雷阵雨适合室内行程，国家博物馆展品丰富且地铁直达，避雨且充实。",
        )

    if code in {71, 73, 75, 77, 85, 86}:  # snowy / sleet
        return (
            "798艺术区",
            "雪天适合慢逛室内展馆与咖啡馆，798 有大量室内空间且地面防滑。",
        )

    if temp >= 30:
        return (
            "颐和园",
            "高温时湖区、林荫多且可乘船，能在早晚避暑，游览强度可控。",
        )

    if temp <= 5:
        return (
            "前门大街与大栅栏",
            "气温偏低时选择步行商业街，随时能进店取暖和补给，行程灵活。",
        )

    if code in {0, 1, 2}:  # sunny / few clouds
        return (
            "景山公园 + 北海公园联游",
            "天气晴好，登景山可俯瞰中轴线，随后步行到北海划船或湖边散步。",
        )

    # Default for overcast/neutral days.
    return (
        "天坛公园",
        "阴天或微风时在开阔公园漫步最舒适，天坛有大片柏林且人流分散。",
    )
