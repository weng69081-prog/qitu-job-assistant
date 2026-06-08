#!/bin/bash
# 截图更新脚本
TOKEN="f4ce9760761d06f3a9c0d941b582ca61afe52c7cc560e36d24bfc0eee242f3fe"
BASE="http://localhost:5173"
OUTDIR="/Users/wendao/interview-agent/screenshots"

# 先设置 token
osascript -e "
tell application \"Safari\"
    activate
    if exists document 1 then
        set URL of document 1 to \"${BASE}/login\"
    else
        open location \"${BASE}/login\"
    end if
    delay 2
    do JavaScript \"localStorage.setItem('token', '${TOKEN}');\" in document 1
end tell
"

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

# 逐个截图
screenshot "/" "01-landing.png"
screenshot "/login" "02-auth.png"
screenshot "/dashboard" "03-dashboard.png"
screenshot "/career" "04-career-explore.png"
screenshot "/interview" "05-interview-sim.png"
screenshot "/exam-practice" "06-exam-practice.png"
screenshot "/delivery-assistant" "07-delivery-assistant.png"
screenshot "/settings" "08-settings.png"

echo "全部截图完成！"