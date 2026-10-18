# CLAUDE.md

Claude Code 在此 repo 啟動時會自動載入本檔與下方匯入的規則。

## 工作規則（完整載入）

@codex-skill/video-autopilot/SKILL.md

## 補充約定

- 回覆一律使用台灣繁體中文與台灣用語（影片、軟體、資訊、檔案、預設），除非另有要求。
- 先給結論，再給必要說明；以可直接執行的成品為優先。
- 參考文件放在 `codex-skill/video-autopilot/references/`，依任務路由按需讀取，不要一次全部載入。
- 個人化與媒體資料（`profiles/`、`config.py`、`assets/`、`videos/`、`_out/` 等）屬本機資料，不得提交。

## 推送前檢查

```bash
python scripts/public_skill_skeleton.py
python scripts/public_privacy_sanitizer.py --self-test --repository .
python tools/code-cleanup-helper/scripts/check_links.py . --config audit.config.json
python src/architecture_gate.py audit
python src/system_health.py --quick
```
