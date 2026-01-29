"""最小版：纯 API + 规则 推荐的北京旅行助手。

用法：
    python main.py
"""

from __future__ import annotations

from utils import fetch_beijing_weather, recommend_attraction


def main():
    # 查询天气
    weather = fetch_beijing_weather()
    # 规则推荐
    place, reason = recommend_attraction(weather)

    # 直接打印结果（无需 LLM）
    print(
        f"北京天气：{weather.weather_desc}，{weather.temperature:.1f}℃，"
        f"风速 {weather.wind_speed:.1f} km/h（观测时间：{weather.observation_time}）。\n"
        f"推荐景点：{place}\n"
        f"推荐理由：{reason}"
    )


if __name__ == "__main__":
    main()
