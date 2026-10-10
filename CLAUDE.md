# Claude Code 工作規則

## AI 生圖（OpenAI gpt-image）
- 程式：`tools/ai-image/generate.py`，金鑰只讀環境變數 `OPENAI_API_KEY`，不得要求使用者在對話中貼金鑰，也不得顯示金鑰內容。
- 輸出資料夾：`AI生圖/`。
- 一律先用 `--quality low` 出草稿給使用者挑選；使用者明確確認後，才用 `--quality high` 出最終版。未經確認不得直接跑 high。
