#!/bin/bash
# 截图脚本 v2 — 用 AppleScript UI 自动登录后截图
BASE="http://localhost:5173"
OUTDIR="/Users/wendao/interview-agent/screenshots"

# 1. 先打开登录页
osascript <<EOL
tell application "Safari"
    activate
    if exists document 1 then
        set URL of document 1 to "${BASE}/login"
    else
        open location "${BASE}/login"
    end if
    delay 2
end tell
EOL

sleep 2

# 2. 输入用户名和密码并登录
osascript <<EOL
tell application "System Events"
    tell process "Safari"
        set frontmost to true
        delay 1
        
        -- 找到登录页面的用户名输入框
        -- 使用 Tab 键导航到输入框
        keystroke tab
        delay 0.3
        keystroke "screenshot"
        delay 0.3
        keystroke tab
        delay 0.3
        keystroke "screenshot123"
        delay 0.3
        -- 按回车提交
        keystroke return
    end tell
end tell
EOL

sleep 3

# 截图函数
screenshot() {
    local url="$1"
    local out="$2"
    osascript -e "
tell application \"Safari\"
    set URL of document 1 to \"${BASE}${url}\"
    delay 2
end tell
"
    sleep 1
    screencapture -l $(osascript -e 'tell app "Safari" to id of window 1') "${OUTDIR}/${out}"
    echo "已截图: ${out}"
}

# 逐个截图（延迟高一点确保页面加载）
sleep 1
screenshot "/" "01-landing.png"
sleep 1
screenshot "/login" "02-auth.png"
sleep 1
screenshot "/dashboard" "03-dashboard.png"
sleep 1
screenshot "/career" "04-career-explore.png"
sleep 1
screenshot "/interview" "05-interview-sim.png"
sleep 1
screenshot "/exam-practice" "06-exam-practice.png"
sleep 1
screenshot "/delivery-assistant" "07-delivery-assistant.png"
sleep 1
screenshot "/settings" "08-settings.png"

echo "全部截图完成！"